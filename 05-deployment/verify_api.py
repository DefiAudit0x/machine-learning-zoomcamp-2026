"""Verify the HW05 API locally or in Docker using the official Q4/Q6 lead."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
LEAD = {
    "lead_source": "organic_search",
    "industry": "technology",
    "employment_status": "employed",
    "location": "europe",
    "number_of_courses_viewed": 4,
    "annual_income": 80304.0,
    "interaction_count": 7,
    "lead_score": 0.74,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:9696")
    parser.add_argument("--runtime", choices=["local_api", "docker"], required=True)
    args = parser.parse_args()
    base_url = args.base_url.rstrip("/")
    with urlopen(base_url + "/health", timeout=30) as response:
        health = json.load(response)
    assert health["status"] == "ok", health
    for key, filename in [("model_sha256", "pipeline.bin"), ("feature_defaults_sha256", "feature_defaults.json")]:
        expected = hashlib.sha256((ROOT / filename).read_bytes()).hexdigest()
        assert health[key] == expected, f"Mismatch for {filename}"
    request = Request(
        base_url + "/predict",
        data=json.dumps(LEAD).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=30) as response:
        prediction = json.load(response)
    assert set(prediction) == {"conversion_probability", "conversion"}, prediction
    assert isinstance(prediction["conversion_probability"], (int, float))
    assert 0 <= prediction["conversion_probability"] <= 1
    assert isinstance(prediction["conversion"], bool)
    result = {
        "runtime": args.runtime,
        "base_url": base_url,
        "health": health,
        "prediction": prediction,
        "answer_to_three_decimals": f"{prediction['conversion_probability']:.3f}",
        "all_checks_passed": True,
    }
    path = ROOT / f"{args.runtime}_result.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
