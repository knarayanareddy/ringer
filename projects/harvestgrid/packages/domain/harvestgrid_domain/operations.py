from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal

from harvestgrid_domain_matching import Candidate, CandidateDecision, rank_eligible


class GleanState(StrEnum):
    OWNER_REVIEW_REQUIRED = "owner_review_required"
    COORDINATOR_REVIEW_REQUIRED = "coordinator_review_required"
    MATCHING = "matching"
    COORDINATOR_ASSIGNMENT_APPROVAL = "coordinator_assignment_approval"
    INVITED = "invited"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class AssignmentState(StrEnum):
    INVITED = "invited"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class VolunteerAssignment:
    volunteer_id: str
    state: AssignmentState
    reveal_not_before: datetime
    reveal_until: datetime


@dataclass(frozen=True)
class RestrictedLocation:
    exact_address: str
    access_notes: str


@dataclass(frozen=True)
class GleanAuditEvent:
    version: int
    actor_id: str
    action: str
    at: datetime
    reason: str = ""


@dataclass(frozen=True)
class GleanSnapshot:
    glean_id: str
    forecast_id: str
    owner_id: str
    coordinator_id: str
    state: GleanState = GleanState.OWNER_REVIEW_REQUIRED
    version: int = 0
    owner_approval_current: bool = False
    coordinator_readiness_confirmed: bool = False
    proposed_assignments: tuple[CandidateDecision, ...] = ()
    assignments: tuple[VolunteerAssignment, ...] = ()
    cancellation_reason: str | None = None
    audit: tuple[GleanAuditEvent, ...] = ()


def _aware_utc(value: datetime, field: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field} must include a timezone")
    return value.astimezone(UTC)


class GleanWorkflow:
    """In-memory coordinator workflow; notification, storage, and deletion adapters are separate."""

    def __init__(self, snapshot: GleanSnapshot) -> None:
        identifiers = (
            snapshot.glean_id,
            snapshot.forecast_id,
            snapshot.owner_id,
            snapshot.coordinator_id,
        )
        if any(not identifier.strip() for identifier in identifiers):
            raise ValueError("Glean, forecast, owner, and coordinator IDs are required")
        if snapshot.version < 0 or snapshot.version != len(snapshot.audit):
            raise ValueError("Snapshot version must equal its audit length")
        self._snapshot = snapshot

    @classmethod
    def new(
        cls, *, glean_id: str, forecast_id: str, owner_id: str, coordinator_id: str
    ) -> GleanWorkflow:
        return cls(
            GleanSnapshot(
                glean_id=glean_id,
                forecast_id=forecast_id,
                owner_id=owner_id,
                coordinator_id=coordinator_id,
            )
        )

    @property
    def snapshot(self) -> GleanSnapshot:
        return self._snapshot

    def _require_version(self, expected_version: int) -> None:
        if expected_version != self._snapshot.version:
            raise ValueError("stale_glean_version")

    def _require_active(self) -> None:
        if self._snapshot.state is GleanState.CANCELLED:
            raise ValueError("cancelled_glean_is_immutable")

    def _require_actor(self, actor_id: str, expected: str) -> None:
        if actor_id != expected:
            raise PermissionError("actor_is_not_authorized")

    def _record(
        self,
        updated: GleanSnapshot,
        *,
        actor_id: str,
        action: str,
        at: datetime,
        reason: str = "",
    ) -> GleanSnapshot:
        timestamp = _aware_utc(at, "Transition timestamp")
        version = self._snapshot.version + 1
        event = GleanAuditEvent(version, actor_id, action, timestamp, reason)
        self._snapshot = replace(
            updated,
            version=version,
            audit=self._snapshot.audit + (event,),
        )
        return self._snapshot

    def request_glean(self, *, actor_id: str, expected_version: int, at: datetime) -> GleanSnapshot:
        self._require_actor(actor_id, self._snapshot.owner_id)
        self._require_active()
        if self._snapshot.owner_approval_current:
            return self._snapshot
        self._require_version(expected_version)
        if self._snapshot.state is not GleanState.OWNER_REVIEW_REQUIRED:
            raise ValueError("owner_approval_not_allowed_from_current_state")
        return self._record(
            replace(
                self._snapshot,
                state=GleanState.COORDINATOR_REVIEW_REQUIRED,
                owner_approval_current=True,
            ),
            actor_id=actor_id,
            action="owner_glean_approved",
            at=at,
        )

    def confirm_readiness(
        self, *, actor_id: str, expected_version: int, at: datetime
    ) -> GleanSnapshot:
        self._require_actor(actor_id, self._snapshot.coordinator_id)
        self._require_active()
        if self._snapshot.coordinator_readiness_confirmed:
            return self._snapshot
        self._require_version(expected_version)
        if (
            self._snapshot.state is not GleanState.COORDINATOR_REVIEW_REQUIRED
            or not self._snapshot.owner_approval_current
        ):
            raise ValueError("current_owner_approval_is_required_before_readiness")
        return self._record(
            replace(
                self._snapshot,
                state=GleanState.MATCHING,
                coordinator_readiness_confirmed=True,
            ),
            actor_id=actor_id,
            action="coordinator_readiness_confirmed",
            at=at,
        )

    def propose_assignments(
        self,
        *,
        actor_id: str,
        candidates: list[Candidate],
        required_count: int,
        expected_version: int,
        at: datetime,
    ) -> GleanSnapshot:
        self._require_actor(actor_id, self._snapshot.coordinator_id)
        self._require_active()
        self._require_version(expected_version)
        if self._snapshot.state is not GleanState.MATCHING:
            raise ValueError("matching_is_not_allowed_from_current_state")
        if not self._snapshot.owner_approval_current:
            raise PermissionError("current_owner_approval_is_required")
        if required_count < 1:
            raise ValueError("At least one eligible volunteer is required")
        eligible = rank_eligible(self._snapshot.glean_id, candidates)
        if len(eligible) < required_count:
            raise ValueError("Not enough eligible volunteers; no assignment was proposed")
        proposed = tuple(eligible[:required_count])
        return self._record(
            replace(
                self._snapshot,
                state=GleanState.COORDINATOR_ASSIGNMENT_APPROVAL,
                proposed_assignments=proposed,
            ),
            actor_id=actor_id,
            action="assignments_proposed",
            at=at,
        )

    def approve_assignments(
        self,
        *,
        actor_id: str,
        reveal_not_before: datetime,
        reveal_until: datetime,
        expected_version: int,
        at: datetime,
    ) -> GleanSnapshot:
        self._require_actor(actor_id, self._snapshot.coordinator_id)
        self._require_active()
        start = _aware_utc(reveal_not_before, "Reveal start")
        end = _aware_utc(reveal_until, "Reveal expiry")
        if start >= end:
            raise ValueError("Location reveal interval must be ordered")
        if self._snapshot.state in {GleanState.INVITED, GleanState.CONFIRMED}:
            existing = self._snapshot.assignments
            if all(
                assignment.reveal_not_before == start and assignment.reveal_until == end
                for assignment in existing
            ):
                return self._snapshot
            raise ValueError("Approved assignment reveal windows cannot be changed")
        self._require_version(expected_version)
        if self._snapshot.state is not GleanState.COORDINATOR_ASSIGNMENT_APPROVAL:
            raise ValueError("coordinator_assignment_approval_not_allowed_from_current_state")
        if not self._snapshot.owner_approval_current or not self._snapshot.proposed_assignments:
            raise PermissionError("Current owner approval and proposed assignments are required")
        assignments = tuple(
            VolunteerAssignment(decision.volunteer_id, AssignmentState.INVITED, start, end)
            for decision in self._snapshot.proposed_assignments
        )
        return self._record(
            replace(
                self._snapshot,
                state=GleanState.INVITED,
                assignments=assignments,
            ),
            actor_id=actor_id,
            action="coordinator_assignments_approved_and_invitation_recorded",
            at=at,
        )

    def confirm_assignment(
        self, *, actor_id: str, expected_version: int, at: datetime
    ) -> GleanSnapshot:
        self._require_active()
        assignment = next(
            (item for item in self._snapshot.assignments if item.volunteer_id == actor_id),
            None,
        )
        if assignment is None:
            raise PermissionError("volunteer_is_not_assigned")
        if assignment.state is AssignmentState.CONFIRMED:
            return self._snapshot
        self._require_version(expected_version)
        if self._snapshot.state not in {GleanState.INVITED, GleanState.CONFIRMED}:
            raise ValueError("assignment_confirmation_not_allowed_from_current_state")
        if not self._snapshot.owner_approval_current:
            raise PermissionError("current_owner_approval_is_required")
        assignments = tuple(
            replace(item, state=AssignmentState.CONFIRMED)
            if item.volunteer_id == actor_id
            else item
            for item in self._snapshot.assignments
        )
        return self._record(
            replace(
                self._snapshot,
                state=GleanState.CONFIRMED,
                assignments=assignments,
            ),
            actor_id=actor_id,
            action="volunteer_assignment_confirmed",
            at=at,
        )

    def reveal_location(
        self, *, actor_id: str, location: RestrictedLocation, at: datetime
    ) -> RestrictedLocation:
        timestamp = _aware_utc(at, "Location access timestamp")
        if (
            self._snapshot.state is not GleanState.CONFIRMED
            or not self._snapshot.owner_approval_current
        ):
            raise PermissionError("location_is_not_available_from_current_state")
        assignment = next(
            (
                item
                for item in self._snapshot.assignments
                if item.volunteer_id == actor_id and item.state is AssignmentState.CONFIRMED
            ),
            None,
        )
        if assignment is None:
            raise PermissionError("location_requires_an_assigned_confirmed_volunteer")
        if not assignment.reveal_not_before <= timestamp < assignment.reveal_until:
            raise PermissionError("location_reveal_window_is_inactive")
        if not location.exact_address.strip():
            raise ValueError("Restricted location is unavailable")
        return location

    def cancel(
        self,
        *,
        actor_id: str,
        reason: Literal["owner_consent_revoked", "coordinator_cancelled"],
        expected_version: int,
        at: datetime,
    ) -> GleanSnapshot:
        if reason not in {"owner_consent_revoked", "coordinator_cancelled"}:
            raise ValueError("Unknown cancellation reason")
        if actor_id not in {self._snapshot.owner_id, self._snapshot.coordinator_id}:
            raise PermissionError("actor_is_not_authorized")
        if reason == "owner_consent_revoked":
            self._require_actor(actor_id, self._snapshot.owner_id)
        else:
            self._require_actor(actor_id, self._snapshot.coordinator_id)
        if self._snapshot.state is GleanState.CANCELLED:
            if self._snapshot.cancellation_reason == reason:
                return self._snapshot
            raise ValueError("Cancellation reason is already committed")
        self._require_version(expected_version)
        assignments = tuple(
            replace(assignment, state=AssignmentState.CANCELLED)
            for assignment in self._snapshot.assignments
        )
        return self._record(
            replace(
                self._snapshot,
                state=GleanState.CANCELLED,
                owner_approval_current=(
                    False
                    if reason == "owner_consent_revoked"
                    else self._snapshot.owner_approval_current
                ),
                assignments=assignments,
                cancellation_reason=reason,
            ),
            actor_id=actor_id,
            action=reason,
            at=at,
            reason=reason,
        )
