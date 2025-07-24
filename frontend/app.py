import streamlit as st
import os
import shutil
from backend.video_utils import extract_frames, create_video_from_frames
from backend.prompt_utils import generate_captions_for_all_frames, rewrite_all_captions
from backend.image_generator import generate_images_from_all_prompts

st.set_page_config(page_title="AI Video Augmentor", layout="centered")

# --- Header Section ---
# Uncomment the next line if you add a logo file later
# st.image("logo.png", width=120)
st.title("AI Video Augmentor")
st.markdown("Transform your videos with AI-generated visuals. Upload a video and watch each scene be reimagined!")

st.divider()

# --- Upload Section ---
st.subheader("Upload Your Video")
st.markdown("Accepted format: .mp4 | Max size: ~100MB (browser limit)")
col1, col2 = st.columns([2, 1])
with col1:
    video_file = st.file_uploader("Select an MP4 video", type=["mp4"])
with col2:
    fps = st.slider("Frames per second (FPS)", min_value=1, max_value=10, value=1)

style = st.selectbox(
    "Choose a visual style for AI-generated images:",
    ["None", "Cyberpunk", "Anime", "Oil Painting", "Pixel Art", "Vintage"]
)

if video_file is not None:
    os.makedirs("input", exist_ok=True)
    temp_input_path = "input/video.mp4"
    with open(temp_input_path, "wb") as f:
        f.write(video_file.read())
    st.success(f"Uploaded video saved as {temp_input_path}")
else:
    temp_input_path = "input/video.mp4" if os.path.exists("input/video.mp4") else None

st.divider()

# --- Processing Flow ---
if st.button("Start Processing"):
    if not temp_input_path or not os.path.exists(temp_input_path):
        st.error("Please upload a video first.")
    else:
        # Clean output folders
        for folder in ["frames", "captions", "prompts", "generated", "output"]:
            if os.path.exists(folder):
                shutil.rmtree(folder)
            os.makedirs(folder, exist_ok=True)
        steps = [
            ("Extracting frames", lambda: extract_frames(temp_input_path, output_folder="frames", fps=fps)),
            ("Generating captions", lambda: generate_captions_for_all_frames(frames_folder="frames", output_folder="captions")),
            ("Rewriting prompts", lambda: rewrite_all_captions(input_folder="captions", output_folder="prompts", style=style)),
            ("Generating AI images", lambda: generate_images_from_all_prompts(prompts_folder="prompts", output_folder="generated")),
            ("Creating final video", lambda: create_video_from_frames(input_folder="generated", output_path="output/output.mp4", fps=fps)),
        ]
        status_msgs = []
        for i, (desc, func) in enumerate(steps, 1):
            with st.spinner(f"Step {i}: {desc}..."):
                func()
            st.success(f"Step {i}: {desc} ✓")
            status_msgs.append(f"{desc} completed.")
        st.divider()
        if os.path.exists("output/output.mp4"):
            st.success("Video successfully processed!")
            st.video("output/output.mp4")
            with open("output/output.mp4", "rb") as f:
                st.download_button("Download Video", f, file_name="output.mp4", mime="video/mp4")
            st.divider()
            # --- Before & After Comparison ---
            st.header("Before & After Frame Comparison")
            original_frames = sorted([f for f in os.listdir("frames") if f.endswith(".png")])
            generated_frames = sorted([f for f in os.listdir("generated") if f.endswith(".png")])
            
            # Limit comparison to the first 5 frames to avoid clutter
            for i in range(min(5, len(original_frames))):
                st.subheader(f"Frame {i+1:04d}")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.image(os.path.join("frames", original_frames[i]), caption="Original")
                    caption_path = os.path.join("captions", original_frames[i].replace('.png', '.txt'))
                    if os.path.exists(caption_path):
                        with open(caption_path, 'r') as f:
                            st.text_area("Original Caption", f.read(), height=100, disabled=True)

                with col2:
                    st.image(os.path.join("generated", generated_frames[i]), caption="AI-Generated")
                    prompt_path = os.path.join("prompts", generated_frames[i].replace('.png', '.txt'))
                    if os.path.exists(prompt_path):
                        with open(prompt_path, 'r') as f:
                            st.text_area("Creative Prompt", f.read(), height=100, disabled=True)
                st.divider()

        else:
            st.error("Processing failed. No output video found.") 