import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_IMAGE_API_URL = "https://api.openai.com/v1/images/generations"

def generate_image_from_prompt(prompt: str, output_path: str):
    """
    Generates an image from a prompt using OpenAI DALL-E 3 and saves it to output_path.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "quality": "standard"
    }
    response = requests.post(OPENAI_IMAGE_API_URL, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    image_url = result["data"][0]["url"]
    # Download the image
    img_response = requests.get(image_url)
    img_response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(img_response.content)
    print(f"Image saved to {output_path}")

def generate_images_from_all_prompts(prompts_folder: str = "prompts", output_folder: str = "generated"):
    """
    Generates images for all prompt .txt files in prompts_folder and saves them to output_folder.
    """
    os.makedirs(output_folder, exist_ok=True)
    prompt_files = sorted([f for f in os.listdir(prompts_folder) if f.lower().endswith(".txt")])
    for prompt_file in prompt_files:
        prompt_path = os.path.join(prompts_folder, prompt_file)
        with open(prompt_path, "r") as f:
            prompt = f.read().strip()
        base_name = os.path.splitext(prompt_file)[0]
        output_path = os.path.join(output_folder, f"{base_name}.png")
        generate_image_from_prompt(prompt, output_path) 