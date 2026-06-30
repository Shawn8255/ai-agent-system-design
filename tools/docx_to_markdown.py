from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from docx import Document
from docx.document import Document as DocumentType
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph


@dataclass(frozen=True)
class LanguageConfig:
    code: str
    source: Path
    output_dir: Path
    figure_prefix: str
    chapter1_prefix: str
    chapter2_prefix: str
    chapter3_prefix: str
    future_prefix: str


SECTION_FILES = {
    "front": "00-preface.md",
    "chapter1": "01-classical-computer-engineering.md",
    "chapter2": "02-llm-compute-engine.md",
    "chapter3": "03-agent-orchestrator.md",
    "future": "99-future-chapters.md",
}


def iter_blocks(document: DocumentType):
    for child in document.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, document)
        elif isinstance(child, CT_Tbl):
            yield Table(child, document)


def escape_cell(text: str) -> str:
    return text.replace("\n", "<br>").replace("|", r"\|").strip()


def table_to_markdown(table: Table) -> list[str]:
    rows = [[escape_cell(cell.text) for cell in row.cells] for row in table.rows]
    if len(rows) == 1 and len(rows[0]) == 1:
        return [f"> {rows[0][0]}"]

    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    header = rows[0]
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * width) + " |",
    ]
    for row in rows[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return lines


def image_extension(partname: str) -> str:
    suffix = Path(partname).suffix.lower()
    return suffix if suffix else ".png"


def paragraph_image_ids(paragraph: Paragraph) -> list[str]:
    return paragraph._p.xpath(".//a:blip/@r:embed")


def paragraph_to_markdown(
    paragraph: Paragraph,
    document: DocumentType,
    section: str,
    config: LanguageConfig,
    assets_dir: Path,
    image_counter: int,
) -> tuple[list[str], int]:
    lines: list[str] = []

    for rel_id in paragraph_image_ids(paragraph):
        image_counter += 1
        part = document.part.related_parts[rel_id]
        ext = image_extension(str(part.partname))
        image_name = f"figure-{image_counter:02d}{ext}"
        image_path = assets_dir / image_name
        image_path.write_bytes(part.blob)
        lines.append(f"![{config.figure_prefix} {image_counter}](assets/{image_name})")

    text = paragraph.text.strip()
    if not text:
        return lines, image_counter

    style = paragraph.style.name
    if style == "Heading 1":
        if section == "front":
            lines.append(f"## {text}")
        else:
            lines.append(f"# {normalize_heading(text, config)}")
    elif style == "Heading 2":
        lines.append(f"## {normalize_heading(text, config)}")
    elif style == "List Number":
        lines.append(f"1. {text}")
    else:
        lines.append(text)

    return lines, image_counter


def normalize_heading(text: str, config: LanguageConfig) -> str:
    if config.code == "en" and text == "1.8 Agent 与经典计算机工程的快速对应":
        return "1.8 Quick Mapping Between Agents and Classical Computer Engineering"
    return text


def detect_section(text: str, current: str, config: LanguageConfig) -> str:
    if text.startswith(config.chapter1_prefix):
        return "chapter1"
    if text.startswith(config.chapter2_prefix):
        return "chapter2"
    if text.startswith(config.chapter3_prefix):
        return "chapter3"
    if text.startswith(config.future_prefix):
        return "future"
    return current


def render_language(config: LanguageConfig) -> None:
    if config.output_dir.exists():
        shutil.rmtree(config.output_dir)
    assets_dir = config.output_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    document = Document(config.source)
    sections: dict[str, list[str]] = {name: [] for name in SECTION_FILES}
    section = "front"
    image_counter = 0
    seen_title = False

    for block in iter_blocks(document):
        block_lines: list[str]
        if isinstance(block, Paragraph):
            text = block.text.strip()
            if block.style.name == "Heading 1":
                section = detect_section(text, section, config)

            block_lines, image_counter = paragraph_to_markdown(
                block, document, section, config, assets_dir, image_counter
            )

            if section == "front" and text and block.style.name == "Normal":
                if not seen_title:
                    block_lines = [f"# {text}"]
                    seen_title = True
                elif re.match(r"^Working Draft", text):
                    block_lines = [f"*{text}*"]
                elif sections["front"] and sections["front"][-1].startswith("# "):
                    block_lines = [f"*{text}*"]
        else:
            block_lines = table_to_markdown(block)

        if block_lines:
            sections[section].extend(block_lines)
            sections[section].append("")

    for key, filename in SECTION_FILES.items():
        path = config.output_dir / filename
        content = "\n".join(sections[key]).rstrip() + "\n"
        path.write_text(content, encoding="utf-8")

    write_language_readme(config)


def write_language_readme(config: LanguageConfig) -> None:
    if config.code == "zh":
        title = "中文文档"
        intro = "本目录包含从中文 DOCX 源文件抽取出的 Markdown 版本。前三章保持原有含义，后续章节仅保留写作计划。"
        links = [
            ("前言、目录大纲与术语约定", SECTION_FILES["front"]),
            ("第 1 章 为什么 AI Agent 让我想到了经典计算机工程", SECTION_FILES["chapter1"]),
            ("第 2 章 LLM：一种新的 Compute Engine", SECTION_FILES["chapter2"]),
            ("第 3 章 Agent：为什么它更像 Orchestrator", SECTION_FILES["chapter3"]),
            ("后续章节写作计划", SECTION_FILES["future"]),
        ]
    else:
        title = "English Documentation"
        intro = "This directory contains the Markdown version extracted from the English DOCX source. Chapters 1-3 preserve the source meaning, and later chapters remain a plan only."
        links = [
            ("Preface, chapter plan and terminology", SECTION_FILES["front"]),
            ("Chapter 1. Why AI Agents Remind Me of Classical Computer Engineering", SECTION_FILES["chapter1"]),
            ("Chapter 2. LLM as a New Compute Engine", SECTION_FILES["chapter2"]),
            ("Chapter 3. Agent as an Orchestrator", SECTION_FILES["chapter3"]),
            ("Plan for the Remaining Chapters", SECTION_FILES["future"]),
        ]

    lines = [f"# {title}", "", intro, ""]
    for label, target in links:
        lines.append(f"- [{label}]({target})")
    lines.append("")
    (config.output_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    configs = [
        LanguageConfig(
            code="zh",
            source=root / "releases/docx/AI_Agent_System_Design_CN_Part1_Ch1-3_v0.2.docx",
            output_dir=root / "docs/zh",
            figure_prefix="图",
            chapter1_prefix="第 1 章",
            chapter2_prefix="第 2 章",
            chapter3_prefix="第 3 章",
            future_prefix="后续章节写作计划",
        ),
        LanguageConfig(
            code="en",
            source=root / "releases/docx/AI_Agent_System_Design_EN_Part1_Ch1-3_v0.2.docx",
            output_dir=root / "docs/en",
            figure_prefix="Figure",
            chapter1_prefix="Chapter 1.",
            chapter2_prefix="Chapter 2.",
            chapter3_prefix="Chapter 3.",
            future_prefix="Plan for the Remaining Chapters",
        ),
    ]

    for config in configs:
        render_language(config)


if __name__ == "__main__":
    main()
