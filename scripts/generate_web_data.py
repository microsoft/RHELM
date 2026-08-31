#!/usr/bin/env python3
"""Generate the static data asset used by the RHELM website explorer."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
QA_DIR = ROOT / "data" / "QA_final"
OUTPUT = ROOT / "web" / "static" / "data" / "explorer-data.json"
SAMPLES_PER_PERSONA_AND_TYPE = 3


def persona_from_path(path: Path) -> str:
    prefix = "low_score_qa_"
    suffix = "_all_validated"
    name = path.stem
    if not name.startswith(prefix) or not name.endswith(suffix):
        raise ValueError(f"Unexpected QA filename: {path.name}")
    return name[len(prefix) : -len(suffix)].replace("_", " ")


def select_evenly(items: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    """Select deterministic samples spanning an ordered group."""
    if len(items) <= limit:
        return items
    if limit == 1:
        return [items[len(items) // 2]]

    positions = [round(index * (len(items) - 1) / (limit - 1)) for index in range(limit)]
    return [items[position] for position in positions]


def count_files(directory: Path, patterns: tuple[str, ...]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for persona_dir in sorted(path for path in directory.iterdir() if path.is_dir()):
        counts[persona_dir.name.replace("_", " ")] = sum(
            1 for pattern in patterns for _ in persona_dir.glob(pattern)
        )
    return counts


def main() -> None:
    records: list[dict[str, Any]] = []
    type_counts: Counter[str] = Counter()
    characteristic_counts: Counter[str] = Counter()
    persona_qa_counts: Counter[str] = Counter()
    grouped_samples: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)

    for qa_path in sorted(QA_DIR.glob("*.jsonl")):
        persona = persona_from_path(qa_path)
        with qa_path.open(encoding="utf-8") as qa_file:
            for line_number, line in enumerate(qa_file, start=1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(f"Invalid JSON in {qa_path}:{line_number}") from error

                question_type = record["question_type"].lower()
                type_counts[question_type] += 1
                persona_qa_counts[persona] += 1
                characteristic_counts.update(record.get("characteristics", []))

                sample = {
                    "id": record["id"],
                    "persona": persona,
                    "type": question_type,
                    "questionDate": record["question_date"],
                    "question": record["question"],
                    "answer": record["answer"],
                    "evidence": record.get("supporting_evidence", []),
                    "characteristics": record.get("characteristics", []),
                }
                records.append(sample)
                grouped_samples[(persona, question_type)].append(sample)

    conversation_counts = count_files(ROOT / "data" / "conversations", ("*.json",))
    email_counts = count_files(ROOT / "data" / "emails", ("*.txt",))
    attachment_counts = count_files(ROOT / "data" / "attachments", ("*.md", "*.html"))

    personas = []
    for persona in sorted(persona_qa_counts):
        personas.append(
            {
                "name": persona,
                "qaPairs": persona_qa_counts[persona],
                "conversations": conversation_counts.get(persona, 0),
                "emails": email_counts.get(persona, 0),
                "attachments": attachment_counts.get(persona, 0),
            }
        )

    samples: list[dict[str, Any]] = []
    for group_key in sorted(grouped_samples):
        samples.extend(
            select_evenly(grouped_samples[group_key], SAMPLES_PER_PERSONA_AND_TYPE)
        )

    sources = {
        "conversations": sum(conversation_counts.values()),
        "emails": sum(email_counts.values()),
        "attachments": sum(attachment_counts.values()),
    }
    payload = {
        "summary": {
            "personas": len(personas),
            "qaPairs": len(records),
            "memorySources": sum(sources.values()),
            "questionTypes": len(type_counts),
        },
        "sources": sources,
        "questionTypes": [
            {"type": question_type, "count": count}
            for question_type, count in sorted(
                type_counts.items(), key=lambda item: (-item[1], item[0])
            )
        ],
        "characteristics": [
            {"name": name, "count": count}
            for name, count in characteristic_counts.most_common()
        ],
        "personas": personas,
        "samples": samples,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote {OUTPUT.relative_to(ROOT)} with {len(samples)} samples "
        f"from {len(records)} QA pairs."
    )


if __name__ == "__main__":
    main()
