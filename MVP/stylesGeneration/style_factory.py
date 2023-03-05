from typing import Tuple
from enum import Enum
import os
from tqdm import tqdm
import requests
import numpy as np
import cv2 as cv
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class ImageStyle(Enum):
    Smiley1 = "Smiley1"
    Cats_using_DALL_E_2 = "Cats_using_DALL_E_2"
    

def create_smiley1_frames(component_config) -> np.array:
    smiley_path: str = os.path.join("resources", "Smiley.png")
    smiley = cv.imread(smiley_path)
    return smiley

def apply_openai_interface(component_config) -> np.array:
    image = np.zeros((256, 256, 3), dtype=np.uint8)
    try:
        prompt = component_config["prompt"]
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="256x256")
        image_url = response['data'][0]['url']
        
        response = requests.get(image_url)
        image_path = os.path.join("resources", f"{prompt}.png")
        if response.status_code:
            fp = open(image_path, 'wb')
            fp.write(response.content)
            fp.close()
            
        image = cv.imread(image_path)
    
    except openai.error.OpenAIError as e:
        print(e.http_status)
        print(e.error)
    
    return image

_style_to_constructor = {
    ImageStyle.Smiley1.name: create_smiley1_frames,
    ImageStyle.Cats_using_DALL_E_2.name: apply_openai_interface
}

def create_frames_by_style(image_style: str, frame_shape: Tuple[int, int], style_components) -> np.array:
    frame = 255 * np.ones((frame_shape[1], frame_shape[0], 3), dtype=np.uint8)  # Start with empty frame
    
    pbar = tqdm(style_components, ncols=100)
    for k, component_config in enumerate(pbar):
        component_type = component_config["type"]
        pbar.set_description(f"Generating component no. {k + 1}: {component_type}")
        
        if component_type == "Image":
            src_frame: np.array = _style_to_constructor[image_style](component_config)
            target_corner = component_config["bounding_box"][:2]
            target_shape = component_config["bounding_box"][2:]
            component_image = cv.resize(src_frame, (target_shape[0], target_shape[1]), interpolation = cv.INTER_AREA)
            
            frame[target_corner[1]:target_corner[1] + target_shape[1],
                  target_corner[0]:target_corner[0] + target_shape[0], :] = component_image
            
        elif component_type == "Text":
            # TODO: Make font configurable.
            font = cv.FONT_HERSHEY_SIMPLEX            
            frame = cv.putText(frame, component_config["text"], tuple(component_config["position"]), font, 
                               component_config["fontScale"], tuple(component_config["color"]), 
                               component_config["thickness"], cv.LINE_AA)
    return frame
