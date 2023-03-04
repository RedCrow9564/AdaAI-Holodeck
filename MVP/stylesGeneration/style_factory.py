from typing import Tuple
from enum import Enum
import os
import numpy as np
import cv2 as cv

class ImageStyle(Enum):
    Smiley1 = "Smiley1"
    

def create_smiley1_frames(style_components) -> np.array:
    smiley_path: str = os.path.join("resources", "Smiley.png")
    smiley = cv.imread(smiley_path)
    return smiley

_style_to_constructor = {
    ImageStyle.Smiley1.name: create_smiley1_frames
}

def create_frames_by_style(image_style: str, frame_shape: Tuple[int, int], style_components) -> np.array:
    frame = 255 * np.ones((frame_shape[1], frame_shape[0], 3), dtype=np.uint8)  # Start with empty frame
    
    for component_config in style_components:
        if component_config["type"] == "Image":
            src_frame: np.array = _style_to_constructor[image_style](style_components)
            target_corner = component_config["bounding_box"][:2]
            target_shape = component_config["bounding_box"][2:]
            component_image = cv.resize(src_frame, (target_shape[0], target_shape[1]), interpolation = cv.INTER_AREA)
            
            frame[target_corner[1]:target_corner[1] + target_shape[1],
                  target_corner[0]:target_corner[0] + target_shape[0], :] = component_image
            
        elif 5 == 5:
            # TODO: Make font configurable.
            font = cv.FONT_HERSHEY_SIMPLEX            
            frame = cv.putText(frame, component_config["text"], tuple(component_config["position"]), font, 
                               component_config["fontScale"], tuple(component_config["color"]), 
                               component_config["thickness"], cv.LINE_AA)
    return frame
