#!/usr/bin/python3
import argparse
import logging
import json
from typing import List, Tuple

import numpy as np
import cv2 as cv

from stylesGeneration.style_factory import create_frames_by_style


def save_video(video_out_path: str, frames, fps):
    """
    Writes frames to an mp4 video file
    :param file_path: Path to output video, must end with .mp4
    :param frames: List of PIL.Image objects
    :param fps: Desired frame rate
    """

    h = frames[0][0].shape[0]
    w = frames[0][0].shape[1]
    writer = cv.VideoWriter(video_out_path, cv.VideoWriter_fourcc(*"mp4v"), 
                            fps, (w, h))

    for frame, repeats in frames:
        for _ in range(repeats):
            writer.write(frame)
    writer.release()
    

def handle_argsparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_video_path", type=str, help="The path to the output video file.")
    parser.add_argument("video_config", type=str, help="The path to the IO config file.")
    args = parser.parse_args()
    return args


def generate_frames(video_config) -> List[Tuple[np.array, int]]:
    frame_shape = (video_config["frame_width"], video_config["frame_height"])
    
    frames = list()
    for k, style_config in enumerate(video_config["Styles"]):
        style_name: str = style_config["name"]
        frames_count: int = style_config["frames_count"]
        components_layout = style_config["components_layout"]
        logging.info(f"Generating style no. {k + 1}: {style_name}")
        
        style_frames = create_frames_by_style(style_name, frame_shape, components_layout)
        frames.append((style_frames, frames_count))
        
    return frames


def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    
    args = handle_argsparse()
    with open(args.video_config) as paths_json:
        video_config = json.load(paths_json)
        logging.info(f"Starting holodeck demo generation")
        out_frames = generate_frames(video_config)
        fps = video_config["fps"]
    
    video_out = args.output_video_path
    logging.info("Saving holodeck demo...")
    save_video(video_out, out_frames, fps=fps)
    logging.info(f"Demo saved in {video_out}")

if __name__ == "__main__":
    main()
