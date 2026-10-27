"""HW05 Q3: verify and load the official frozen model, then predict one lead."""
from __future__ import annotations

import hashlib
import json
import pickle
from pathlib import Path

from model import normalize_record

ROOT = Path(__file__).resolve().parent
EXPECTED_SHA256 = "1646bbdcd38d4f044da6b630c5b332c93a314245a8c21929011c42de51f629f1"
LEAD = {
    "lead_source": "paid_ads",
    "industry": "technology",
    "employment_status": "employed",
    "location": "north_america",
    "number_of_courses_viewed": 2,
    "annual_income": 79276.0,
    "interaction_count": 4,
    "lead_score": 0.41,
}


def main() -> None:
    artifact = (ROOT / "pipeline.bin").read_bytes()
    checksum = hashlib.sha256(artifact).hexdigest()
    assert checksum == EXPECTED_SHA256, "Model artifact checksum mismatch"
    pipeline = pickle.loads(artifact)
    probability = float(pipeline.predict_proba([normalize_record(LEAD)])[0, 1])
    assert 0 <= probability <= 1
    result = {
        "model_sha256": checksum,
        "conversion_probability": probability,
        "answer_to_three_decimals": f"{probability:.3f}",
    }
    (ROOT / "q3_result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
