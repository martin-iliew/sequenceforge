from __future__ import annotations

from dataclasses import dataclass

from models import SequenceJob


QUESTION_PAYLOAD = [
    {
        "key": "framework",
        "label": "Framework",
        "question": "React or Vue?",
        "options": ["React", "Vue"],
    },
    {
        "key": "visual_tone",
        "label": "Visual tone",
        "question": "Clean/minimal, Bold/editorial, Warm/organic, or Tech/precise?",
        "options": ["Clean/minimal", "Bold/editorial", "Warm/organic", "Tech/precise"],
    },
    {
        "key": "motion_intensity",
        "label": "Motion intensity",
        "question": "Subtle, Moderate, Bold, or Cinematic?",
        "options": ["Subtle", "Moderate", "Bold", "Cinematic"],
    },
    {
        "key": "motion_appetite",
        "label": "Motion appetite",
        "question": "Restrained, Expressive, or Showcase?",
        "options": ["Restrained", "Expressive", "Showcase"],
    },
    {
        "key": "motion_no_go",
        "label": "Motion no-go",
        "question": "Any banned motion patterns, accessibility concerns, or things to avoid?",
        "options": [
            "Avoid jitter or shake",
            "Avoid flashing or rapid contrast changes",
            "Avoid large parallax or aggressive pinning",
            "No specific bans",
        ],
    },
    {
        "key": "must_have_motion",
        "label": "Must-have motion",
        "question": "Any specific motion ask such as text reveal, pinned section, image sequence, or hide-on-scroll nav?",
        "options": [
            "Pinned section and image sequence",
            "Image sequence without pinning",
            "Text reveal support",
            "Hide-on-scroll nav support",
        ],
    },
    {
        "key": "color_direction",
        "label": "Color direction",
        "question": "Brand colors as-is, Warm it up, Cool it down, or Dark mode leaning?",
        "options": ["Brand colors as-is", "Warm it up", "Cool it down", "Dark mode leaning"],
    },
    {
        "key": "constraints",
        "label": "Constraints",
        "question": "Any layout, accessibility, or performance constraints?",
        "options": [
            "Keep it lightweight on mobile",
            "Accessibility first, reduce motion risk",
            "Preserve existing layout exactly",
            "No special constraints",
        ],
    },
]


@dataclass(slots=True)
class PromptProfile:
    framework_hint: str
    image_direction: str
    video_direction: str
    video_constraints: str
    scrub: bool
    pin_section: bool


def build_question_payload() -> list[dict]:
    return QUESTION_PAYLOAD.copy()


def build_prompt_profile(job: SequenceJob, setup: dict) -> PromptProfile:
    visual_tone = str(setup.get("visual_tone", "Clean/minimal"))
    color_direction = str(setup.get("color_direction", "Brand colors as-is"))
    motion_intensity = str(setup.get("motion_intensity", "Moderate"))
    motion_appetite = str(setup.get("motion_appetite", "Restrained"))
    must_have_motion = str(setup.get("must_have_motion", "Image sequence without pinning"))
    motion_no_go = str(setup.get("motion_no_go", "No specific bans"))
    constraints = str(setup.get("constraints", "No special constraints"))

    image_parts = [_visual_tone_text(visual_tone), _color_direction_text(color_direction)]
    video_parts = [_motion_intensity_text(motion_intensity), _motion_appetite_text(motion_appetite)]
    video_constraints = ", ".join(
        part for part in [motion_no_go, constraints, "preserve orientation continuity and lighting continuity"] if part
    )

    pin_section = "pinned" in must_have_motion.lower() or motion_appetite.lower() == "showcase"
    scrub = "image sequence" in must_have_motion.lower() or motion_intensity.lower() in {"bold", "cinematic"}

    return PromptProfile(
        framework_hint=str(setup.get("framework", "")) or "React",
        image_direction=", ".join(part for part in image_parts if part),
        video_direction=", ".join(part for part in video_parts if part),
        video_constraints=video_constraints,
        scrub=scrub,
        pin_section=pin_section,
    )


def _visual_tone_text(value: str) -> str:
    mapping = {
        "Clean/minimal": "clean minimal composition with disciplined negative space",
        "Bold/editorial": "bold editorial framing with premium contrast and confident composition",
        "Warm/organic": "warm organic atmosphere with tactile materials and softer transitions",
        "Tech/precise": "tech-precise framing with crisp geometry and exacting detail",
    }
    return mapping.get(value, value)


def _color_direction_text(value: str) -> str:
    mapping = {
        "Brand colors as-is": "keep the established brand color balance intact",
        "Warm it up": "push the palette slightly warmer while keeping the scene believable",
        "Cool it down": "lean the palette cooler and more steel-toned without losing realism",
        "Dark mode leaning": "bias the palette toward darker tonal values and richer shadows",
    }
    return mapping.get(value, value)


def _motion_intensity_text(value: str) -> str:
    mapping = {
        "Subtle": "subtle motion with restrained camera travel",
        "Moderate": "moderate motion with smooth controlled progression",
        "Bold": "bold motion with stronger visual progression but stable physics",
        "Cinematic": "cinematic motion with high-end camera intent and deliberate pacing",
    }
    return mapping.get(value, value)


def _motion_appetite_text(value: str) -> str:
    mapping = {
        "Restrained": "restrained motion that supports content before spectacle",
        "Expressive": "expressive motion that noticeably shapes the section rhythm",
        "Showcase": "showcase motion that acts as the primary storytelling device",
    }
    return mapping.get(value, value)
