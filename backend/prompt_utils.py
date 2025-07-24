import os
import base64
import requests
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

SYSTEM_PROMPT = (
    "Describe this image in a single, vivid, highly detailed English sentence that clearly explains the scene. "
    "Think of it as a prompt for an image generator."
)

def generate_caption_for_image(image_path: str) -> str:
    """
    Generates a descriptive caption for the given image using OpenAI GPT-4 Vision API.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

    with open(image_path, "rb") as img_file:
        img_b64 = base64.b64encode(img_file.read()).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
                ]
            }
        ],
        "max_tokens": 100
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"].strip()

def generate_captions_for_all_frames(frames_folder: str = "frames", output_folder: str = "captions"):
    """
    Generates captions for all PNG frames in the frames_folder and saves them as .txt files in output_folder.
    """
    os.makedirs(output_folder, exist_ok=True)
    frame_files = sorted([f for f in os.listdir(frames_folder) if f.lower().endswith(".png")])
    for frame_file in frame_files:
        frame_path = os.path.join(frames_folder, frame_file)
        caption = generate_caption_for_image(frame_path)
        base_name = os.path.splitext(frame_file)[0]
        caption_path = os.path.join(output_folder, f"{base_name}.txt")
        with open(caption_path, "w") as f:
            f.write(caption + "\n")
        print(f"Caption for {frame_file} saved to {caption_path}")

def rewrite_caption_to_prompt(original_caption: str, style: Optional[str] = None) -> str:
    """
    Uses OpenAI GPT-4 to creatively rewrite the original caption into a new AI prompt.
    The new prompt should change 70–90% of the content while keeping the overall visual structure relatable.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

    system_message = (
        "Rewrite the following image description into a creative and vivid AI prompt. "
        "Change 70–90% of the content while keeping the overall visual structure relatable."
    )

    if style and style != "None":
        system_message += f" Make it fit the {style} style."

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": original_caption}
        ],
        "max_tokens": 100
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"].strip()

def rewrite_all_captions(input_folder: str = "captions", output_folder: str = "prompts", style: Optional[str] = None):
    """
    Reads all .txt files in input_folder, rewrites each caption, and saves to output_folder.
    """
    os.makedirs(output_folder, exist_ok=True)
    caption_files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith(".txt")])
    for caption_file in caption_files:
        caption_path = os.path.join(input_folder, caption_file)
        with open(caption_path, "r") as f:
            original_caption = f.read().strip()
        new_prompt = rewrite_caption_to_prompt(original_caption, style=style)
        prompt_path = os.path.join(output_folder, caption_file)
        with open(prompt_path, "w") as f:
            f.write(new_prompt + "\n")
        print(f"Prompt for {caption_file} saved to {prompt_path}") 