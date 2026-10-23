import json
from pathlib import Path
from typing import Any

from .forecast import validate_harvest_window

ROOT = Path(__file__).resolve().parents[3]


def main() -> None:
    document: dict[str, Any] = json.loads(
        (ROOT / "examples" / "harvest-window.example.json").read_text()
    )
    issues = validate_harvest_window(document)
    if issues:
        raise ValueError(f"Invalid harvest-window fixture: {issues}")
    print(
        json.dumps(
            {
                "mode": "FIXTURE ONLY — no Ring, weather, CV, or coordinator connection",
                "forecast_status": document["status"],
                "model_kind": document["model"]["kind"],
                "human_readiness_review_required": document["visual_capability"][
                    "human_readiness_review_required"
                ],
                "internal_ripeness_inferred": document["visual_capability"][
                    "internal_ripeness_inferred"
                ],
                "food_safety_inferred": document["visual_capability"]["food_safety_inferred"],
                "notice": "Schema/semantic validation only; no operational forecast was generated.",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
