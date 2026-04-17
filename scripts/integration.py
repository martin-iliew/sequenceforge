from __future__ import annotations

import re
from pathlib import Path

from models import (
    InspectionReport,
    IntegrationApplyResult,
    IntegrationBlueprint,
    SequenceJob,
)
from project_setup import load_project_setup
from prompt_profile import PromptProfile, build_prompt_profile

CANVAS_MARKER = "sequenceforge-canvas"
STYLE_MARKER = "sequenceforge-style"
ANIMATION_MARKER = "sequenceforge-animation"


def build_integration_blueprint(job: SequenceJob, report: InspectionReport) -> IntegrationBlueprint:
    setup = load_project_setup(job.project_root)
    profile = build_prompt_profile(job, setup) if setup else None
    target_file = report.target_candidates[0].path
    style_file = _resolve_style_file(report, target_file)
    frame_count = _resolve_frame_count(job.frames_dest)
    canvas_markup = _build_canvas_markup(job, report)
    style_snippet = _build_style_snippet(job, report)
    helper_code = _build_helper_code(job)
    animation_code = _build_animation_code(job, report, frame_count, profile)

    notes = list(report.notes)
    notes.append(f"Insert the canvas into {target_file.as_posix()} near the requested section.")
    if report.animation_pattern == "module":
        if report.gsap_registration_file is not None:
            notes.append(f"Extend the existing animation module at {report.gsap_registration_file.as_posix()}.")
    else:
        if report.gsap_registration_file is not None:
            notes.append(f"Append the sequence to the existing GSAP block in {report.gsap_registration_file.as_posix()}.")
        else:
            notes.append("No GSAP registration file was found; add the sequence near the target section entrypoint.")
    if profile is not None:
        notes.append(f"Prompt profile: {profile.image_direction}. Motion profile: {profile.video_direction}.")

    return IntegrationBlueprint(
        framework=report.framework,
        animation_host_strategy=report.animation_pattern,
        target_file=target_file,
        animation_file=report.gsap_registration_file or target_file,
        style_file=style_file,
        frame_count=frame_count,
        canvas_markup=canvas_markup,
        style_snippet=style_snippet,
        animation_code=animation_code,
        helper_code=helper_code,
        notes=notes,
    )


def apply_integration(
    job: SequenceJob,
    report: InspectionReport,
    blueprint: IntegrationBlueprint | None = None,
) -> IntegrationApplyResult:
    blueprint = blueprint or build_integration_blueprint(job, report)
    changed_files: list[str] = []

    if _write_canvas_markup(blueprint.target_file, blueprint.canvas_markup):
        changed_files.append(str(blueprint.target_file))

    style_target = _resolve_style_target(blueprint, report)
    if style_target is not None and _write_style(style_target, blueprint.style_snippet, report):
        style_path = style_target if isinstance(style_target, Path) else blueprint.target_file
        style_str = str(style_path)
        if style_str not in changed_files:
            changed_files.append(style_str)

    if _write_animation(job, report, blueprint):
        animation_str = str(blueprint.animation_file)
        if animation_str not in changed_files:
            changed_files.append(animation_str)

    return IntegrationApplyResult(blueprint=blueprint, changed_files=changed_files)


def _resolve_style_file(report: InspectionReport, target_file: Path) -> Path | None:
    if report.style_strategy == "tailwind":
        return None
    if report.style_strategy == "scoped":
        return target_file

    if target_file.suffix == ".html":
        match = re.search(
            r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\'](.+?)["\']',
            target_file.read_text(encoding="utf-8"),
            re.IGNORECASE,
        )
        if match:
            href = match.group(1)
            candidate = (target_file.parent / href).resolve()
            if candidate.exists():
                return candidate

    sibling_css = target_file.with_suffix(".css")
    return sibling_css if sibling_css.exists() else None


def _resolve_frame_count(frames_dest: Path) -> int:
    frames = sorted(Path(frames_dest).glob("frame_*.png"))
    return len(frames) if frames else 147


def _build_canvas_markup(job: SequenceJob, report: InspectionReport) -> str:
    if report.framework in {"react", "react-next"}:
        classes = (
            "pointer-events-none fixed left-1/2 top-1/2 z-10 h-auto max-h-[80vh] "
            "max-w-[80vw] -translate-x-1/2 -translate-y-1/2"
        )
        return (
            f'<canvas id="{job.canvas_id}" width={{1158}} height={{770}} '
            f'className="{classes}" />'
        )
    if report.framework in {"vue", "vue-nuxt", "svelte", "sveltekit"}:
        return f'<canvas id="{job.canvas_id}" width="1158" height="770" class="sequence-canvas" />'
    return f'<canvas id="{job.canvas_id}" width="1158" height="770"></canvas>'


def _build_style_snippet(job: SequenceJob, report: InspectionReport) -> str:
    if report.style_strategy == "tailwind":
        return (
            "Use Tailwind utilities directly on the canvas: "
            "pointer-events-none fixed left-1/2 top-1/2 z-10 h-auto max-h-[80vh] "
            "max-w-[80vw] -translate-x-1/2 -translate-y-1/2"
        )

    selector = f"#{job.canvas_id}" if report.framework == "vanilla" else ".sequence-canvas"
    return "\n".join(
        [
            f"{selector} {{",
            "  position: fixed;",
            "  left: 50%;",
            "  top: 50%;",
            "  transform: translate(-50%, -50%);",
            "  max-width: 80vw;",
            "  max-height: 80vh;",
            "}",
        ]
    )


def _build_helper_code(job: SequenceJob) -> str:
    return f"""
function imageSequence(config) {{
  const playhead = {{ frame: 0 }};
  const canvas = gsap.utils.toArray(config.canvas)[0];
  const context = canvas.getContext("2d");
  const images = config.urls.map((url, index) => {{
    const image = new Image();
    image.src = url;
    if (index === 0) {{
      image.onload = render;
    }}
    return image;
  }});
  let currentFrame = -1;

  function render() {{
    const frame = Math.round(playhead.frame);
    if (frame === currentFrame) {{
      return;
    }}
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.drawImage(images[frame], 0, 0);
    currentFrame = frame;
  }}

  return gsap.to(playhead, {{
    frame: images.length - 1,
    ease: "none",
    duration: images.length / {job.fps},
    onUpdate: render,
    scrollTrigger: config.scrollTrigger
  }});
}}
""".strip()


def _build_animation_code(
    job: SequenceJob,
    report: InspectionReport,
    frame_count: int,
    profile: PromptProfile | None = None,
) -> str:
    trigger_selector = _infer_trigger_selector(report)
    frame_path = f"{report.frames_url_base}/frame_${{String(index + 1).padStart(6, '0')}}.png"
    scrub = True if profile is None else profile.scrub
    pin = True if profile is None else profile.pin_section
    lines = [
        f"const frameCount = {frame_count};",
        f"const urls = Array.from({{ length: frameCount }}, (_, index) => `{frame_path}`);",
        "",
        "imageSequence({",
        f'  canvas: "#{job.canvas_id}",',
        "  urls,",
        "  scrollTrigger: {",
        f'    trigger: "{trigger_selector}",',
        '    start: "top top",',
        '    end: "+=1800",',
        f"    scrub: {'true' if scrub else 'false'},",
        f"    pin: {'true' if pin else 'false'}",
        "  }",
        "});",
    ]

    if report.animation_pattern == "module":
        return "\n".join(
            [
                "export function initImageSequenceSection() {",
                "  // ScrollTrigger-driven image sequence",
                *[f"  {line}" if line else "" for line in lines],
                "}",
            ]
        )
    return "\n".join(lines)


def _infer_trigger_selector(report: InspectionReport) -> str:
    target_text = report.target_candidates[0].path.read_text(encoding="utf-8")
    if 'id="hero"' in target_text or "id='hero'" in target_text:
        return "#hero"
    return "section"


def _resolve_style_target(
    blueprint: IntegrationBlueprint,
    report: InspectionReport,
) -> Path | str | None:
    if report.style_strategy == "tailwind":
        return None
    if blueprint.style_file is not None:
        return blueprint.style_file
    if blueprint.target_file.suffix == ".html":
        return "inline-head-style"
    return None


def _write_canvas_markup(target_file: Path, canvas_markup: str) -> bool:
    content = target_file.read_text(encoding="utf-8")
    if CANVAS_MARKER in content or canvas_markup in content:
        return False

    updated = None
    section_match = re.search(r"(<section[^>]*id=[\"']hero[\"'][^>]*>)", content, re.IGNORECASE)
    if section_match:
        insertion = f"{section_match.group(1)}\n        <!-- {CANVAS_MARKER} -->\n        {canvas_markup}"
        updated = content[: section_match.start()] + insertion + content[section_match.end() :]
    else:
        body_match = re.search(r"<body[^>]*>", content, re.IGNORECASE)
        if body_match:
            insertion = f"{body_match.group(0)}\n    <!-- {CANVAS_MARKER} -->\n    {canvas_markup}"
            updated = content[: body_match.start()] + insertion + content[body_match.end() :]

    if updated is None:
        return False

    target_file.write_text(updated, encoding="utf-8")
    return True


def _write_style(style_target: Path | str, style_snippet: str, report: InspectionReport) -> bool:
    if style_target == "inline-head-style":
        return False

    path = style_target
    content = path.read_text(encoding="utf-8")
    if STYLE_MARKER in content or style_snippet in content:
        return False

    block = f"\n/* {STYLE_MARKER} */\n{style_snippet}\n"
    if report.style_strategy == "scoped" and path.suffix in {".vue", ".svelte"}:
        updated = re.sub(r"</style>", block + "</style>", content, count=1, flags=re.IGNORECASE)
        path.write_text(updated, encoding="utf-8")
        return True

    path.write_text(content.rstrip() + block, encoding="utf-8")
    return True


def _write_animation(job: SequenceJob, report: InspectionReport, blueprint: IntegrationBlueprint) -> bool:
    path = blueprint.animation_file
    content = path.read_text(encoding="utf-8")
    if ANIMATION_MARKER in content or "initImageSequenceSection()" in content or "function imageSequence(config)" in content:
        return False

    block = (
        f"\n\n// {ANIMATION_MARKER}\n"
        f"{blueprint.helper_code}\n\n"
        f"{blueprint.animation_code}\n"
    )

    if path.suffix in {".vue", ".svelte"}:
        updated = _inject_component_animation(content, report.framework, blueprint)
        path.write_text(updated, encoding="utf-8")
        return updated != content

    if blueprint.animation_host_strategy == "module":
        updated = _inject_module_sequence_call(content)
        updated += block
        path.write_text(updated, encoding="utf-8")
        return True

    updated = _inject_inline_sequence_call(content, blueprint.animation_code)
    if updated != content:
        updated = updated + f"\n\n// {ANIMATION_MARKER}\n{blueprint.helper_code}\n"
        path.write_text(updated, encoding="utf-8")
        return True

    path.write_text(content + block, encoding="utf-8")
    return True


def _inject_module_sequence_call(content: str) -> str:
    pattern = re.compile(r"(export function \w+\(\)\s*\{)")
    match = pattern.search(content)
    if not match:
        return content

    start = match.end()
    end = _find_matching_brace(content, content.index("{", match.start()))
    body = content[start:end]
    if "initImageSequenceSection();" in body:
        return content

    body = body.rstrip() + "\n  initImageSequenceSection();\n"
    return content[:start] + body + content[end:]


def _inject_inline_sequence_call(content: str, animation_code: str) -> str:
    marker = 'document.addEventListener("DOMContentLoaded", () => {'
    start = content.find(marker)
    if start == -1:
        return content

    brace_index = content.find("{", start)
    end = _find_matching_brace(content, brace_index)
    body = content[brace_index + 1:end]
    if "imageSequence({" in body:
        return content

    injection = "\n  // ScrollTrigger-driven image sequence\n"
    injection += "\n".join(f"  {line}" if line else "" for line in animation_code.splitlines())
    injection += "\n"
    new_body = body.rstrip() + injection
    return content[: brace_index + 1] + new_body + content[end:]


def _find_matching_brace(content: str, open_index: int) -> int:
    depth = 0
    for index in range(open_index, len(content)):
        char = content[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("Could not find matching brace")


def _inject_component_animation(
    content: str,
    framework: str,
    blueprint: IntegrationBlueprint,
) -> str:
    script_match = re.search(r"<script[^>]*>(.*?)</script>", content, re.DOTALL | re.IGNORECASE)
    if not script_match:
        return content

    script_body = script_match.group(1)
    if "function imageSequence(config)" in script_body:
        return content

    if framework in {"vue", "vue-nuxt"}:
        script_body = _ensure_import(script_body, "import { onMounted } from \"vue\";")
    else:
        script_body = _ensure_import(script_body, "import { onMount } from \"svelte\";")
    script_body = _ensure_import(script_body, "import { ScrollTrigger } from \"gsap/ScrollTrigger\";")

    component_hook = "onMounted" if framework in {"vue", "vue-nuxt"} else "onMount"
    body_block = "\n".join(f"  {line}" if line else "" for line in blueprint.animation_code.splitlines())
    script_addition = (
        f"\n\n// {ANIMATION_MARKER}\n"
        "gsap.registerPlugin(ScrollTrigger);\n\n"
        f"{blueprint.helper_code}\n\n"
        f"{component_hook}(() => {{\n{body_block}\n}});\n"
    )
    updated_script = script_body.rstrip() + script_addition + "\n"
    return content[: script_match.start(1)] + updated_script + content[script_match.end(1) :]


def _ensure_import(script_body: str, statement: str) -> str:
    if statement in script_body:
        return script_body
    return statement + "\n" + script_body.lstrip("\n")
