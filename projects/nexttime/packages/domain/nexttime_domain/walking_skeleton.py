import json
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
from .rubric import evaluate_authentic_attempt, rubric_from_mapping
from .skills import update_skill_from_authentic_attempt

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
    print(
        json.dumps(
            {
                "mode": "FIXTURE ONLY — no Bee, AWS, or iOS connection",
                "rubric_version": rubric.version,
                "outcome": outcome.status.value,
                "confirmation_required": outcome.confirmation_required,
                "reason_codes": outcome.reason_codes,
                "authentic_skill_update": unchanged_skill != initial_skill,
                "notice": (
                    "No authentic progress is inferred from this unconfirmed fixture attempt."
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
