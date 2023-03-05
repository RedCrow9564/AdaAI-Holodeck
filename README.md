# AdaAI_Holodeck
The Holodeck project created for the Ada-AI exhibition

# MVP
This program generates a demo for the Holodeck. That is, a movie is generated where is of the requesterd "styles" is displayed over some frames. A layout for each style may contain texts and images.
Images may be created offline or online, using DALL-E 2.

## Getting started
In order to run this demo, first we verify all Python dependencies are installed, using:

```
pip install -r requirements.txt
```

To be ablt to generate images using DALL-E 2, you are required to set your own OpenAI API key in an .env file. This file should look like:
```
OPENAI_API_KEY=YOUR_API_KEY
```

Make sure the 'MVP' folder is your current working directory. Then:
```
YOUR_PYTHON_PATH generate_video.py YOUR_OUTPUT_PATH YOUR_CONFIG_JSON_FILE
```

The demo video will appear in the output path you gave above.
