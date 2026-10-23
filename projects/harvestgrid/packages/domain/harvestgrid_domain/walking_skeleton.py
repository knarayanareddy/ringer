import json
from copy import deepcopy
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

from harvestgrid_domain_matching import Candidate, HardConstraints, RankingFeatures

from .forecast import validate_harvest_window
from .operations import GleanWorkflow, RestrictedLocation
from .outcomes import CompletionEntry, RejectionReason, WeightEntry, WeightSource

ROOT = Path(__file__).resolve().parents[3]
T0 = datetime(2026, 10, 23, 12, 0, tzinfo=UTC)


def candidate(volunteer_id: str, score: float) -> Candidate:
    return Candidate(
        volunteer_id=volunteer_id,
        constraints=HardConstraints(
            owner_approval_current=True,
            coordinator_approval_current=True,
            trained_leader_available=True,
            volunteer_training_valid=True,
            equipment_satisfied=True,
            availability_intersects=True,
            recipient_capacity_sufficient=True,
            coordinator_no_recipient_plan_approved=False,
            unresolved_safety_blockers=0,
            address_reveal_policy_satisfied=True,
            insurance_waiver_satisfied=True,
        ),
        ranking=RankingFeatures(score, score, score, score, score),
    )


def main() -> None:
    document: dict[str, Any] = json.loads(
        (ROOT / "examples" / "harvest-window.example.json").read_text()
    )
    issues = validate_harvest_window(document)
    if issues:
        raise ValueError(f"Invalid harvest-window fixture: {issues}")

    workflow = GleanWorkflow.new(
        glean_id="glean-fixture",
        forecast_id=document["window_id"],
        owner_id="owner-fixture",
        coordinator_id="coordinator-fixture",
    )
    workflow.request_glean(actor_id="owner-fixture", expected_version=0, at=T0)
    workflow.confirm_readiness(
        actor_id="coordinator-fixture",
        expected_version=1,
        at=T0 + timedelta(minutes=1),
    )
    workflow.propose_assignments(
        actor_id="coordinator-fixture",
        candidates=[candidate("volunteer-a", 0.8), candidate("volunteer-b", 0.9)],
        required_count=1,
        expected_version=2,
        at=T0 + timedelta(minutes=2),
    )
    reveal_start = T0 + timedelta(minutes=10)
    reveal_end = T0 + timedelta(hours=2)
    workflow.approve_assignments(
        actor_id="coordinator-fixture",
        reveal_not_before=reveal_start,
        reveal_until=reveal_end,
        expected_version=3,
        at=T0 + timedelta(minutes=3),
    )
    selected = workflow.snapshot.proposed_assignments[0].volunteer_id
    workflow.confirm_assignment(actor_id=selected, expected_version=4, at=reveal_start)
    restricted = RestrictedLocation(
        "FIXTURE ONLY — not a residential address", "Fixture access note"
    )
    workflow.reveal_location(actor_id=selected, location=restricted, at=reveal_start)
    outcome_workflow = GleanWorkflow(deepcopy(workflow.snapshot))
    cancelled = workflow.cancel(
        actor_id="owner-fixture",
        reason="owner_consent_revoked",
        expected_version=5,
        at=T0 + timedelta(minutes=20),
    )
    try:
        workflow.reveal_location(
            actor_id=selected,
            location=restricted,
            at=T0 + timedelta(minutes=20),
        )
    except PermissionError:
        reveal_after_cancellation = False
    else:
        raise AssertionError("Cancelled workflow must not reveal a restricted location")

    entry = CompletionEntry(
        recipient_id="recipient-fixture",
        actual_harvested_at=T0 + timedelta(minutes=15),
        visible_fruit_count=40,
        weight=WeightEntry(
            gross_weight_kg=Decimal("10.0"),
            net_weight_kg=Decimal("8.5"),
            accepted_weight_kg=Decimal("8.0"),
            rejected_weight_kg=Decimal("0.5"),
            source=WeightSource.CALIBRATED_SCALE,
            scale_reference="fixture-scale-01",
            rejection_reasons=(RejectionReason.SPOILED,),
            evidence_sha256="a" * 64,
        ),
    )
    outcome_workflow.record_completion(
        actor_id=selected,
        entry=entry,
        expected_version=5,
        at=T0 + timedelta(minutes=20),
    )
    verified = outcome_workflow.verify_completion(
        actor_id="coordinator-fixture",
        forecast_document=document,
        expected_version=6,
        at=T0 + timedelta(minutes=25),
    )
    closed = outcome_workflow.close_outcome(
        actor_id="coordinator-fixture",
        expected_version=7,
        at=T0 + timedelta(minutes=30),
    )
    if verified.weight_record is None:
        raise AssertionError("Verified weight record is required")
    if verified.donation_receipt is None:
        raise AssertionError("Donation receipt is required")
    if verified.forecast_evaluation is None:
        raise AssertionError("Forecast evaluation is required")

    print(
        json.dumps(
            {
                "mode": (
                    "FIXTURE ONLY — no Ring, weather, CV, notification, database, "
                    "or coordinator connection"
                ),
                "forecast_status": document["status"],
                "model_kind": document["model"]["kind"],
                "human_readiness_review_required": document["visual_capability"][
                    "human_readiness_review_required"
                ],
                "internal_ripeness_inferred": document["visual_capability"][
                    "internal_ripeness_inferred"
                ],
                "food_safety_inferred": document["visual_capability"]["food_safety_inferred"],
                "selected_volunteer": selected,
                "workflow_state_after_revocation": cancelled.state.value,
                "assignment_count": len(cancelled.assignments),
                "location_reveal_before_cancellation": True,
                "location_reveal_after_cancellation": reveal_after_cancellation,
                "notification_adapter_connected": False,
                "durable_workflow_claimed": False,
                "outcome_workflow_state": closed.state.value,
                "verified_accepted_weight_kg": str(verified.weight_record.entry.accepted_weight_kg),
                "donation_receipt": verified.donation_receipt.as_non_sensitive_dict(),
                "visible_count_absolute_error": (
                    verified.forecast_evaluation.visible_count_absolute_error
                ),
                "forecast_evaluation_reasons": verified.forecast_evaluation.reason_codes,
                "automatic_model_promotion": (
                    verified.forecast_evaluation.automatic_model_promotion
                ),
                "notice": (
                    "Separate in-memory revocation and coordinator-verified outcome fixtures only; "
                    "no actual invitation, residential location, glean, donation, deletion job, "
                    "model promotion, or operational outcome is claimed."
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
