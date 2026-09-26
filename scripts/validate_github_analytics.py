"""Validate generated GitHub analytics assets and their README references."""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
REQUIRED = {
    "github-activity.svg": "contributions in the last year",
    "github-languages-repo.svg": "top languages by repo",
    "github-languages-commit.svg": "top languages by code",
    "github-stats.svg": "stats",
    "github-commits-hourly.svg": "monthly contributions",
}
PLACEHOLDERS = ("placeholder", "fixture", "demo", "no language data available", "warming up")


def validate_asset(filename: str, expected_title: str) -> None:
    path = ASSETS / filename
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError(f"Required analytics asset is missing or empty: {path.relative_to(ROOT)}")

    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as error:
        raise ValueError(f"Invalid SVG XML in {filename}: {error}") from error

    if root.tag != "{http://www.w3.org/2000/svg}svg":
        raise ValueError(f"{filename} does not have an SVG root")
    if not (root.get("viewBox") or (root.get("width") and root.get("height"))):
        raise ValueError(f"{filename} has no intrinsic dimensions or viewBox")

    content = " ".join(root.itertext()).lower()
    if expected_title not in content:
        raise ValueError(f"{filename} does not contain its expected chart title")
    if any(value in content for value in PLACEHOLDERS):
        raise ValueError(f"{filename} contains placeholder/demo text")
    if any(value in content for value in ("rajat-wyrm", "rajat kumar", "rajatkumar7861913")):
        raise ValueError(f"{filename} contains data for another profile")

    elements = list(root.iter())
    if filename == "github-activity.svg":
        has_graph = sum(element.tag.endswith("path") for element in elements) >= 7
    elif filename in ("github-languages-repo.svg", "github-languages-commit.svg"):
        has_graph = any(element.tag.endswith("circle") and element.get("stroke-dasharray") for element in elements)
        has_graph = has_graph and "%" in content
    elif filename == "github-stats.svg":
        numeric_values = [
            element.text or ""
            for element in elements
            if element.tag.endswith("text") and re.fullmatch(r"\s*\d[\d,]*\s*", element.text or "")
        ]
        has_graph = len(numeric_values) >= 1 and sum(element.tag.endswith("rect") for element in elements) >= 6
    else:
        bars = [element for element in elements if element.tag.endswith("rect") and element.get("rx") == "3"]
        has_graph = len(bars) == 12 and all(float(bar.get("height", "0")) >= 0 for bar in bars)
    if not has_graph:
        raise ValueError(f"{filename} is missing its expected chart/statistics content")


def validate_readme() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    local_assets = re.findall(r'<img\b[^>]*\bsrc="(\./assets/[^\"]+)"', readme)
    for reference in local_assets:
        path = ROOT / reference[2:]
        if not path.is_file():
            raise ValueError(f"README.md references a missing local asset: {reference}")
    for filename in REQUIRED:
        reference = f"./assets/{filename}"
        if reference not in readme:
            raise ValueError(f"README.md does not reference {reference}")
    activity_position = readme.find("GITHUB ACTIVITY")
    last_asset_position = readme.find("./assets/github-commits-hourly.svg")
    flow_position = readme.find("Contribution Flow")
    if min(activity_position, last_asset_position, flow_position) < 0 or not activity_position < last_asset_position < flow_position:
        raise ValueError("README.md must place Contribution Flow below the complete analytics dashboard")
    if re.search(r"LANGUAGE UNIVERSE|rajat-wyrm|Rajat Kumar|localhost|/mnt/data|C:\\Users", readme, re.IGNORECASE):
        raise ValueError("README.md contains a forbidden legacy section, profile, or path")


def main() -> int:
    try:
        for filename, title in REQUIRED.items():
            validate_asset(filename, title)
        validate_readme()
    except (OSError, ValueError) as error:
        print(f"analytics validation failed: {error}", file=sys.stderr)
        return 1
    print(f"validated {len(REQUIRED)} GitHub analytics SVGs and README references")
    return 0


if __name__ == "__main__":
    sys.exit(main())