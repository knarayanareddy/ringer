import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from .minimization import validate_minimized_attempt
from .models import (
    AttemptEvaluationInput,
    CriterionEvidence,
    CriterionResult,
    Situation,
    SkillState,
)
from .review import AttemptReviewService, BreakdownReviewDecision
from .rubric import evaluate_authentic_attempt, rubric_from_mapping
from .skills import update_skill_from_authentic_attempt
from .transcripts import (
    CaptureMode,
    SourceTranscript,
    Speaker,
    TranscriptMinimizationService,
    TranscriptTurn,
)

ROOT = Path(__file__).resolve().parents[3]


def main() -> None:
    document: dict[str, Any] = json.loads(
        (ROOT / "examples" / "real-world-attempt.example.json").read_text()
    )
    rubric_document = json.loads((ROOT / "packages" / "rubrics" / "rubric_v1.json").read_text())
    issues = validate_minimized_attempt(document)
    if issues:
        raise ValueError(f"Invalid minimized fixture: {issues}")

    rubric = rubric_from_mapping(rubric_document)
    criteria = {
        item["criterion_id"]: CriterionEvidence(
            result=CriterionResult(item["result"]),
            evidence_present=bool(item["self_evidence_excerpt"]),
        )
        for item in document["outcome"]["criteria"]
    }
    outcome = evaluate_authentic_attempt(
        rubric,
        AttemptEvaluationInput(
            situation=Situation(document["context"]["situation"]),
            criteria=criteria,
            asr_confidence=document["processing"]["asr_confidence"],
            minimization_complete=document["processing"]["redaction_status"] == "minimized",
            interaction_ended=True,
        ),
    )
    initial_skill = SkillState()
    unchanged_skill = update_skill_from_authentic_attempt(
        initial_skill,
        CriterionResult.SATISFIED,
        confirmed_authentic_attempt=document["status"] == "confirmed",
    )
    minimization_service = TranscriptMinimizationService()
    source = SourceTranscript(
        reference="fixture-bee-recording-walking-001",
        learner_id=document["learner_id"],
        recorded_at=datetime(2026, 10, 22, 15, 0, tzinfo=UTC),
        capture_mode=CaptureMode.CONSENTED_CONVERSATION,
        situation=Situation.REPAIR,
        turns=(
            TranscriptTurn(
                Speaker.LEARNER,
                "Ik wil een afspraak voor de reparatie.",
                0,
                1200,
                0.91,
            ),
            TranscriptTurn(
                Speaker.OTHER,
                "Fixture other-speaker text that must be excluded.",
                1200,
                2400,
                0.93,
            ),
        ),
        consent_attested=True,
        all_participants_consented=True,
        revoked=False,
        retention_policy_present=True,
    )
    minimized = minimization_service.minimize(
        source, minimized_at=source.recorded_at + timedelta(hours=1)
    )
    duplicate_safe = minimization_service.minimize(source) is minimized
    reviewed_service = AttemptReviewService(document, rubric)
    reviewed_service.review_breakdown(
        actor_learner_id=document["learner_id"],
        expected_version=document["version"],
        breakdown_id=document["breakdowns"][0]["breakdown_id"],
        decision=BreakdownReviewDecision.CONFIRMED,
        reviewed_at=datetime(2026, 10, 22, 16, 0, tzinfo=UTC),
    )
    reviewed = reviewed_service.confirm_attempt(
        actor_learner_id=document["learner_id"],
        expected_version=document["version"] + 1,
        reviewed_at=datetime(2026, 10, 22, 16, 0, tzinfo=UTC),
    )
    print(
        json.dumps(
            {
                "mode": "FIXTURE ONLY — no Bee, AWS, or iOS connection",
                "rubric_version": rubric.version,
                "minimization_status": minimized.status,
                "minimized_self_excerpts": len(minimized.self_excerpts),
                "other_speaker_transcript_retained": minimized.other_speaker_transcript_retained,
                "duplicate_source_safe": duplicate_safe,
                "outcome": outcome.status.value,
                "confirmation_required": outcome.confirmation_required,
                "reason_codes": outcome.reason_codes,
                "authentic_skill_update": unchanged_skill != initial_skill,
                "notice": (
                    "No authentic progress is inferred from this unconfirmed fixture attempt."
                ),
                "reviewed_status": reviewed.document["status"],
                "reviewed_outcome": reviewed.document["outcome"]["status"],
                "reviewed_skill_updates": reviewed.skill_updates,
                "reviewed_confirmation_beta": reviewed.skill_states["confirmation"].beta,
                "reviewed_notice": (
                    "A separate fixture-only reviewed copy updates the confirmed "
                    "breakdown once; no real learner or persistent learner store is involved."
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
