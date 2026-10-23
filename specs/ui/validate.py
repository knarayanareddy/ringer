#!/usr/bin/env python3
"""Dependency-free workspace, structural, link, token, and contrast checks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
WORKSPACES = REPO_ROOT / "projects"
PROJECTS = {
    "accesshold": {"name": "AccessHold", "screens": 5, "platforms": {"responsive_web", "alexa_rich_card"}, "schema": "access-contract.schema.json", "example": "access-contract.example.json"},
    "curiolab": {"name": "CurioLab", "screens": 6, "platforms": {"fire_tv_1080p", "android_companion"}, "schema": "episode.schema.json", "example": "episode.example.json"},
    "nexttime": {"name": "NextTime", "screens": 5, "platforms": {"ios", "accessibility_text_sizes"}, "schema": "real-world-attempt.schema.json", "example": "real-world-attempt.example.json"},
    "harvestgrid": {"name": "HarvestGrid", "screens": 4, "platforms": {"responsive_web", "outdoor_mobile"}, "schema": "harvest-window.schema.json", "example": "harvest-window.example.json"},
    "roomsmith": {"name": "RoomSmith", "screens": 5, "platforms": {"fire_tv_1080p", "android_companion"}, "schema": "puzzle-graph.schema.json", "example": "puzzle-graph.example.json"},
}
REQUIRED_WORKSPACE_FILES = {"AGENTS.md", "README.md", "SPEC.md", "SPEC_TRACEABILITY.md", "SPEC_DEVIATIONS.md"}
REQUIRED_UI_FILES = {"PRODUCT.md", "DESIGN.md", "WIREFRAMES.md", "tokens.json", "wireframe.html", "theme.css"}
REQUIRED_SHARED_FILES = {"README.md", "FOUNDATIONS.md", "TOOLING.md", "index.html", "index.css", "wireframes.css", "wireframes.js"}
TOKEN_VARIABLES = {
    "canvas": "color.canvas",
    "surface": "color.surface",
    "surface-2": "color.surface_alt",
    "text": "color.text",
    "muted": "color.text_muted",
    "line": "color.border",
    "primary": "color.primary",
    "on-primary": "color.on_primary",
    "accent": "color.accent",
    "on-accent": "color.on_accent",
    "success": "color.success",
    "warning": "color.warning",
    "danger": "color.danger",
    "info": "color.info",
    "focus": "color.focus",
}
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
REQUIREMENT_ID_RE = re.compile(r"\b(?:FR|INT|NFR|SEC|AC)-[A-Z]+-[A-Z0-9-]+\b")


def project_ui(slug: str) -> Path:
    return WORKSPACES / slug / "ui"


def display(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT))


def load_json_without_duplicates(path: Path) -> dict:
    def no_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.references: list[tuple[str, str, str]] = []
        self.id_references: list[tuple[str, str]] = []
        self.buttons: list[dict[str, str | None]] = []
        self.wireframe_ids: list[str] = []
        self.h1_count = 0
        self.main_count = 0
        self.has_lang = False
        self.has_viewport = False
        self.has_doctype = False
        self.has_title = False
        self.icon_without_hidden = 0

    def handle_decl(self, decl: str) -> None:
        if decl.lower().strip() == "doctype html":
            self.has_doctype = True

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = dict(attrs_list)
        element_id = attrs.get("id")
        if element_id:
            self.ids.append(element_id)
        classes = set((attrs.get("class") or "").split())
        if tag == "section" and "wireframe" in classes and element_id:
            self.wireframe_ids.append(element_id)
        if tag == "html" and attrs.get("lang"):
            self.has_lang = True
        if tag == "meta" and attrs.get("name") == "viewport":
            self.has_viewport = True
        if tag == "title":
            self.has_title = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "main":
            self.main_count += 1
        if tag == "button":
            self.buttons.append(attrs)
        if tag == "svg" and "icon" in classes and attrs.get("aria-hidden") != "true":
            self.icon_without_hidden += 1
        for attr in ("href", "src"):
            value = attrs.get(attr)
            if value is not None:
                self.references.append((tag, attr, value))
        for attr in ("aria-labelledby", "aria-describedby"):
            value = attrs.get(attr)
            if value:
                self.id_references.extend((attr, item) for item in value.split())


def luminance(hex_color: str) -> float:
    values = [int(hex_color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in values]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(first: str, second: str) -> float:
    high, low = sorted((luminance(first), luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def token_value(tokens: dict, path: str) -> object:
    current: object = tokens
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            raise ValueError(f"Missing token path {path}")
        current = current[part]
    if not isinstance(current, dict) or "$value" not in current:
        raise ValueError(f"Token path {path} does not resolve to a token")
    return current["$value"]


def local_target(source: Path, reference: str) -> tuple[Path | None, str, bool]:
    """Return path, fragment, and whether this is an external reference."""
    parsed = urlsplit(reference)
    external = bool(parsed.scheme or parsed.netloc)
    if external:
        return None, parsed.fragment, True
    path = unquote(parsed.path)
    target = source if not path else (source.parent / path).resolve()
    return target, unquote(parsed.fragment), False


def validate_workspaces(errors: list[str], report: dict) -> None:
    report["workspaces"] = {}
    for slug, expected in PROJECTS.items():
        workspace = WORKSPACES / slug
        for name in sorted(REQUIRED_WORKSPACE_FILES):
            if not (workspace / name).is_file():
                errors.append(f"Missing workspace artifact {display(workspace / name)}")
        for name in sorted(REQUIRED_UI_FILES):
            if not (project_ui(slug) / name).is_file():
                errors.append(f"Missing project UI artifact {display(project_ui(slug) / name)}")
        for kind in ("schema", "example"):
            directory = "schemas" if kind == "schema" else "examples"
            path = workspace / directory / expected[kind]
            if not path.is_file():
                errors.append(f"Missing canonical {kind} {display(path)}")
                continue
            try:
                load_json_without_duplicates(path)
            except (OSError, json.JSONDecodeError, ValueError) as exc:
                errors.append(f"{display(path)}: invalid JSON: {exc}")
        spec_path = workspace / "SPEC.md"
        trace_path = workspace / "SPEC_TRACEABILITY.md"
        if not spec_path.exists() or not trace_path.exists():
            continue
        spec_ids = set(REQUIREMENT_ID_RE.findall(spec_path.read_text(encoding="utf-8")))
        trace_ids = set(REQUIREMENT_ID_RE.findall(trace_path.read_text(encoding="utf-8")))
        missing = sorted(spec_ids - trace_ids)
        extra = sorted(trace_ids - spec_ids)
        if missing or extra:
            errors.append(f"{display(trace_path)}: ID coverage mismatch; missing={missing}, extra={extra}")
        report["workspaces"][slug] = {"requirement_ids": len(spec_ids), "traceability_ids": len(trace_ids)}
    report["requirement_total"] = sum(item["requirement_ids"] for item in report["workspaces"].values())
    if report["requirement_total"] != 284:
        errors.append(f"Expected 284 canonical requirement/acceptance IDs, found {report['requirement_total']}")


def validate_tokens(errors: list[str], report: dict) -> None:
    report["contrast"] = {}
    for slug, expected in PROJECTS.items():
        path = project_ui(slug) / "tokens.json"
        try:
            tokens = load_json_without_duplicates(path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{display(path)}: unreadable token JSON: {exc}")
            continue
        meta = tokens.get("meta", {})
        if meta.get("project") != expected["name"]:
            errors.append(f"{display(path)}: meta.project does not match {expected['name']}")
        if set(meta.get("platforms", [])) != expected["platforms"]:
            errors.append(f"{display(path)}: platform set differs from the approved surface contract")
        for category in ("color", "typography", "spacing", "shape", "motion", "layout"):
            if category not in tokens:
                errors.append(f"{display(path)}: missing {category} token group")
        for category, group in tokens.items():
            if category == "meta":
                continue
            if not isinstance(group, dict):
                errors.append(f"{display(path)}: {category} must be an object")
                continue
            for name, token in group.items():
                if not isinstance(token, dict) or not token.get("$type") or "$value" not in token:
                    errors.append(f"{display(path)}: {category}.{name} lacks $type/$value")
                elif token["$type"] == "color" and not HEX_RE.match(str(token["$value"])):
                    errors.append(f"{display(path)}: {category}.{name} is not a six-digit hex color")
        theme_path = project_ui(slug) / "theme.css"
        theme = theme_path.read_text(encoding="utf-8") if theme_path.exists() else ""
        variables = dict(re.findall(r"--([\w-]+)\s*:\s*(#[0-9A-Fa-f]{6})", theme))
        for variable, token_path in TOKEN_VARIABLES.items():
            try:
                token_color = str(token_value(tokens, token_path)).lower()
            except ValueError as exc:
                errors.append(f"{display(path)}: {exc}")
                continue
            if variables.get(variable, "").lower() != token_color:
                errors.append(f"{display(theme_path)}: --{variable} must match {token_path} ({token_color})")
        pairs = meta.get("contrast_pairs", {})
        if len(pairs) < 10:
            errors.append(f"{display(path)}: expected at least 10 declared contrast pairs")
        project_results = {}
        for name, pair in pairs.items():
            try:
                foreground = str(token_value(tokens, pair["foreground"]))
                background = str(token_value(tokens, pair["background"]))
                minimum = float(pair["minimum"])
                if not HEX_RE.match(foreground) or not HEX_RE.match(background):
                    raise ValueError("contrast endpoints must be six-digit hex colors")
                ratio = contrast_ratio(foreground, background)
                project_results[name] = {
                    "foreground": foreground,
                    "background": background,
                    "ratio": round(ratio, 2),
                    "minimum": minimum,
                    "pass": ratio >= minimum,
                }
                if ratio < minimum:
                    errors.append(f"{display(path)}: {name} contrast {ratio:.2f}:1 is below {minimum}:1")
            except (KeyError, TypeError, ValueError) as exc:
                errors.append(f"{display(path)}: invalid contrast pair {name}: {exc}")
        report["contrast"][slug] = project_results


def validate_html(errors: list[str], report: dict) -> None:
    pages = [ROOT / "index.html", *(project_ui(slug) / "wireframe.html" for slug in PROJECTS)]
    parsed_pages: dict[Path, PageParser] = {}
    for page in pages:
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        parsed_pages[page.resolve()] = parser
        relative = display(page)
        duplicates = [item for item, count in Counter(parser.ids).items() if count > 1]
        if duplicates:
            errors.append(f"{relative}: duplicate IDs {duplicates}")
        for field, label in ((parser.has_doctype, "doctype"), (parser.has_lang, "html lang"), (parser.has_viewport, "viewport meta"), (parser.has_title, "title")):
            if not field:
                errors.append(f"{relative}: missing {label}")
        if parser.h1_count != 1 or parser.main_count != 1:
            errors.append(f"{relative}: expected exactly one h1 and one main")
        if parser.icon_without_hidden:
            errors.append(f"{relative}: {parser.icon_without_hidden} decorative SVG icons lack aria-hidden")
        for attrs in parser.buttons:
            if not attrs.get("type"):
                errors.append(f"{relative}: button lacks an explicit type")
            if "data-static" not in attrs and "disabled" not in attrs:
                errors.append(f"{relative}: non-disabled button is not marked as static demonstration content")
        for attr, target in parser.id_references:
            if target not in parser.ids:
                errors.append(f"{relative}: {attr} references missing ID {target}")
        if page.name == "wireframe.html":
            slug = page.parent.parent.name
            expected_count = PROJECTS[slug]["screens"]
            if len(parser.wireframe_ids) != expected_count:
                errors.append(f"{relative}: expected {expected_count} screens, found {len(parser.wireframe_ids)}")
            text = page.read_text(encoding="utf-8").lower()
            if "static review artifact" not in text or "fictional" not in text:
                errors.append(f"{relative}: missing static/fictional scope disclosure")
    for page, parser in parsed_pages.items():
        relative = display(page)
        for tag, attr, reference in parser.references:
            if not reference or reference == "#":
                errors.append(f"{relative}: empty {tag} {attr} reference")
                continue
            target, fragment, external = local_target(page, reference)
            if external:
                if tag in {"script", "img", "iframe", "source"} or (tag == "link" and attr == "href"):
                    errors.append(f"{relative}: external runtime dependency {reference}")
                continue
            assert target is not None
            if not target.exists():
                errors.append(f"{relative}: missing local target {reference}")
                continue
            if fragment:
                target_parser = parser if target == page else parsed_pages.get(target)
                if target_parser is None and target.suffix.lower() == ".html" and target in {p.resolve() for p in pages}:
                    target_parser = parsed_pages[target]
                if target_parser is not None and fragment not in target_parser.ids:
                    errors.append(f"{relative}: {reference} targets a missing fragment")
    report["html"] = {
        display(page): {
            "screens": len(parser.wireframe_ids),
            "ids": len(parser.ids),
            "references": len(parser.references),
            "buttons": len(parser.buttons),
        }
        for page, parser in parsed_pages.items()
    }
    report["screen_total"] = sum(item["screens"] for item in report["html"].values())


def validate_markdown(errors: list[str], report: dict) -> None:
    checked = 0
    for document in sorted(REPO_ROOT.glob("**/*.md")):
        if {"node_modules", ".git", ".venv"}.intersection(document.parts):
            continue
        text = document.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_RE.finditer(text):
            raw = match.group(1).strip()
            target_text = raw.split(maxsplit=1)[0].strip("<>")
            target, _fragment, external = local_target(document, target_text)
            if external or not target_text or target_text.startswith("#"):
                continue
            checked += 1
            assert target is not None
            if not target.exists():
                errors.append(f"{display(document)}: missing Markdown target {target_text}")
    report["markdown_local_links"] = checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, help="Write a deterministic JSON report")
    args = parser.parse_args()
    errors: list[str] = []
    report: dict = {"status": "running"}
    for name in sorted(REQUIRED_SHARED_FILES):
        if not (ROOT / name).is_file():
            errors.append(f"Missing shared artifact {name}")
    validate_workspaces(errors, report)
    validate_tokens(errors, report)
    validate_html(errors, report)
    validate_markdown(errors, report)
    report["status"] = "failed" if errors else "passed"
    report["errors"] = errors
    if args.report:
        destination = args.report if args.report.is_absolute() else ROOT / args.report
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if errors:
        print(f"UI static validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    contrast_count = sum(len(items) for items in report["contrast"].values())
    print(f"PASS: 5 agent workspaces and {report['requirement_total']} traceable requirement/acceptance IDs")
    print(f"PASS: 5 token files and {contrast_count} contrast pairs")
    print(f"PASS: 6 HTML pages, {report['screen_total']} screens, local links/fragments, and static-control contracts")
    print(f"PASS: {report['markdown_local_links']} local Markdown links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
