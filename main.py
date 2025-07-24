from backend.video_utils import extract_frames, create_video_from_frames
from backend.prompt_utils import generate_captions_for_all_frames, rewrite_all_captions
from backend.image_generator import generate_images_from_all_prompts
import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Video Augmentor Pipeline")
    parser.add_argument("--video_path", type=str, default="input/video.mp4", help="Path to the input video.")
    parser.add_argument("--fps", type=int, default=1, help="Frames per second to extract.")
    parser.add_argument("--style", type=str, default="None", help="Visual style for the generated images.")
    args = parser.parse_args()

    if os.path.exists(args.video_path):
        extract_frames(args.video_path, output_folder="frames", fps=args.fps)
        generate_captions_for_all_frames(frames_folder="frames", output_folder="captions")
        rewrite_all_captions(input_folder="captions", output_folder="prompts", style=args.style)
        generate_images_from_all_prompts(prompts_folder="prompts", output_folder="generated")
        create_video_from_frames(input_folder="generated", output_path="output/output.mp4", fps=args.fps)
    else:
        print(f"Error: Video file not found at '{args.video_path}'.")
        print("Please make sure you have a video file named 'video.mp4' inside the 'input' directory or specify the path with --video_path.") 