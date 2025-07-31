from manim import config, logger
from IPython.display import Video
import logging
import os

def show_scene(scene, **kwargs):
    scene = scene(**kwargs)
    scene.render()
    scene_name = scene.__class__.__name__
    f"media/videos/{config.pixel_height}p{config.frame_rate}"
    simple_path = os.path.join(f"media/videos/{config.pixel_height}p{config.frame_rate}", f"{scene_name}.mp4")
    return Video(simple_path, embed=True, width=320)