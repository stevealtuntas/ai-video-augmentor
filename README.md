# AI Video Augmentor

## Overview

**AI Video Augmentor** is a professional tool that takes a user-uploaded video, extracts its frames, describes each scene using AI, creatively modifies those prompts, generates new images, and finally compiles them into a fully transformed video. This pipeline enables creative video augmentation and AI-powered storytelling.

---

## How It Works (Pipeline)

1. **Input video** (`input/video.mp4`)
2. **Extracted frames** (`frames/`)
3. **Captions** (scene descriptions, `captions/`)
4. **Creative prompts** (rewritten, `prompts/`)
5. **AI images** (generated, `generated/`)
6. **Final video** (`output/output.mp4`)

---

## Technologies Used

- Python 3.11
- FFmpeg
- OpenAI GPT-4 Vision & DALL·E 3 API
- Streamlit (optional, for web UI)
- Docker & Devcontainer
- Cursor.dev (for development)

---

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```
2. **Add your OpenAI API key:**
   - Create a `.env` file in the root with:
     ```
     OPENAI_API_KEY=sk-your-key-here
     ```
3. **Run in Docker/Devcontainer (recommended):**
   - Open in Cursor.dev or VS Code
   - Select "Reopen in Container"
   - All dependencies will be installed automatically

   **OR**

   **Run locally with Python venv:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run the pipeline:**
   ```bash
   python main.py
   ```

---

## Folder Structure

- `input/` – Place your input video as `video.mp4` here
- `frames/` – Extracted frames from the input video
- `captions/` – AI-generated scene descriptions for each frame
- `prompts/` – Creatively rewritten prompts for each frame
- `generated/` – AI-generated images based on the creative prompts
- `output/` – Final output video (`output.mp4`)

---

## How to Use

1. Place your video file as `input/video.mp4`.
2. Run:
   ```bash
   python main.py
   ```
3. Find your transformed video at `output/output.mp4`.

---

## Sample Output

*Add before/after screenshots or a .gif here to showcase the transformation!*

---

## License

MIT License

---

## Contributing

- Pull requests are welcome!
- For major changes, please open an issue first to discuss what you would like to change.
- For questions or issues, open an issue on GitHub. 