#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import gradio as gr

from videogen.dao.working_block_dao import WorkingBlockDAO
from videogen.pipeline.parse_script import parse_script_lines
from videogen.pipeline.utils import write_json
from videogen.schema.project_schema import ProjectStatus
from videogen.ui.shared import (
    PROJECT_ROOT,
    get_background_video_choices,
    get_bgm_choices,
    get_character_choices,
)


def _save_project_assets(
    project_name: str,
    size: str,
    default_character: str,
    show_character_overlay: bool,
    bgm_path: str,
    background_video_path: str,
    burn_subtitle: bool,
    blocks: list,
) -> str:
    project_dir = PROJECT_ROOT / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    script_dicts = [asdict(block) for block in blocks]

    project_payload = {
        "project_name": project_name,
        "size": size,
        "script": script_dicts,
        "project_status": ProjectStatus.CREATED.value,
        "show_character_overlay": bool(show_character_overlay),
        "bgm_path": bgm_path or None,
        "background_video": background_video_path,
        "burn_subtitle": burn_subtitle,
    }

    project_json_path = project_dir / f"{project_name}.json"
    write_json(project_json_path, project_payload)
    return str(project_json_path)


def _reset_project_blocks(project_name: str) -> None:
    dao = WorkingBlockDAO()
    existing = dao.get_all(project_name)
    for wb in existing:
        dao.delete(wb.id)


def create_project(
    project_name: str,
    size: str,
    default_character: str,
    show_character_overlay: bool,
    script_text: str,
    bgm_path: str,
    background_video_path: str,
    burn_subtitle: bool,
) -> str:
    project_name = (project_name or "").strip()
    if not project_name:
        return "❌ Project name cannot be empty"

    if not script_text or not script_text.strip():
        return "❌ Script text cannot be empty"

    bgm_path = (bgm_path or "").strip()
    background_video_path = (background_video_path or "").strip()
    if not background_video_path:
        return "❌ Background video is required"

    bg_video = Path(background_video_path)
    if not bg_video.is_absolute():
        bg_video = (Path.cwd() / bg_video).resolve()
    if not bg_video.exists():
        return f"❌ Background video not found: {bg_video}"

    try:
        blocks = parse_script_lines(
            script_text,
            default_character,
            size,
            background_video_path,
            show_character_overlay,
        )
    except ValueError as exc:
        return f"❌ {exc}"

    if not blocks:
        return "❌ No valid script lines parsed."

    _reset_project_blocks(project_name)

    project_json_path = _save_project_assets(
        project_name=project_name,
        size=size,
        default_character=default_character,
        show_character_overlay=show_character_overlay,
        bgm_path=bgm_path,
        background_video_path=background_video_path,
        burn_subtitle=burn_subtitle,
        blocks=blocks,
    )

    return (
        f"✅ 项目 `{project_name}` 已创建。\n\n"
        f"- project JSON: `{project_json_path}`"
    )


def build_create_project_page() -> None:
    character_choices = get_character_choices()
    default_character_value = character_choices[0][1] if character_choices else ""

    bgm_choices = get_bgm_choices()
    background_video_choices = get_background_video_choices()
    background_default = (
        background_video_choices[0][1] if background_video_choices else None
    )

    with gr.Column():
        gr.Markdown("### 🆕 Create Project\n为项目输入名称和脚本，背景视频为必选项。")

        project_name = gr.Textbox(
            label="Project Name",
            placeholder="e.g., tech_demo",
            max_lines=1,
            interactive=True,
        )

        with gr.Row():
            size = gr.Radio(
                label="Video Format",
                choices=["landscape", "tiktok"],
                value="tiktok",
            )

            default_character = gr.Dropdown(
                label="Default Character",
                choices=character_choices or [("Not Set", "")],
                value=default_character_value,
                allow_custom_value=True,
            )

        bgm_dropdown = gr.Dropdown(
            label="Background Music (BGM)",
            choices=bgm_choices,
            value=bgm_choices[0][1] if bgm_choices else "",
        )

        background_video_dropdown = gr.Dropdown(
            label="Background Video",
            choices=background_video_choices,
            value=background_default,
            interactive=bool(background_video_choices),
        )

        burn_subtitle = gr.Checkbox(
            label="Burn Subtitles to Final Video",
            value=True,
        )

        show_character_overlay = gr.Checkbox(
            label="显示角色人像（Character Overlay）",
            value=True,
        )

        script_text = gr.Textbox(
            label="Script Text",
            placeholder='"character": your line\nnext line...',
            lines=12,
        )

        status = gr.Markdown("")
        create_btn = gr.Button("Create Project", variant="primary")

    create_btn.click(
        fn=create_project,
        inputs=[
            project_name,
            size,
            default_character,
            show_character_overlay,
            script_text,
            bgm_dropdown,
            background_video_dropdown,
            burn_subtitle,
        ],
        outputs=[status],
    )
