from manim import config, logger
from IPython.display import Video
import logging
import os

def show_scene(scene_or_class, quality="medium", **kwargs):
    """
    Renders a Manim Scene and displays the resulting video inline in Jupyter.
    Supports simplified Binder paths and standard CLI-style Manim output.
    """
    quality_settings = {
        "low":    {"pixel_height": 270,  "pixel_width": 480,  "frame_rate": 15},
        "medium": {"pixel_height": 540,  "pixel_width": 960,  "frame_rate": 30},
        "high":   {"pixel_height": 1080, "pixel_width": 1920, "frame_rate": 60},
        "4k":     {"pixel_height": 2160, "pixel_width": 3840, "frame_rate": 60},
    }

    if quality not in quality_settings:
        raise ValueError(f"Unknown quality level: {quality}")

    for key, value in quality_settings[quality].items():
        setattr(config, key, value)

    config.verbosity = "WARNING"
    logger.setLevel(logging.WARNING)

    scene = scene_or_class(**kwargs) if isinstance(scene_or_class, type) else scene_or_class
    scene.render()

    # Try simplified Binder path first
    scene_name = scene.__class__.__name__
    simple_dir = f"media/videos/{config.pixel_height}p{config.frame_rate}"
    simple_path = os.path.join(simple_dir, f"{scene_name}.mp4")

    if os.path.exists(simple_path):
        return Video(simple_path, embed=True)

    # Fallback to full CLI-style folder structure
    fallback_path = os.path.join(
        config.media_dir,
        "videos",
        scene.renderer.file_writer.folder_name,
        scene.renderer.file_writer.render_dir,
        f"{scene_name}.mp4"
    )

    if os.path.exists(fallback_path):
        return Video(fallback_path, embed=True)

    raise FileNotFoundError(f"Could not find rendered video at:\n- {simple_path}\n- {fallback_path}")