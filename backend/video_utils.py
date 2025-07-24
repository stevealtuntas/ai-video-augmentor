import os
import subprocess

def extract_frames(video_path: str, output_folder: str = "frames", fps: int = 1):
    """
    Extracts frames from a video file using FFmpeg.

    Args:
        video_path (str): The path to the input video file.
        output_folder (str, optional): The folder to save the extracted frames. Defaults to "frames".
        fps (int, optional): The number of frames to extract per second. Defaults to 1.
    """
    os.makedirs(output_folder, exist_ok=True)
    
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps={fps}",
        f"{output_folder}/frame_%04d.png"
    ]
    
    try:
        print(f"Executing FFmpeg command: {' '.join(command)}")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("FFmpeg output:", result.stdout)
        print(f"Frames extracted successfully to '{output_folder}'.")
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please ensure it is installed and in your PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error during FFmpeg execution: {e.stderr}") 

def create_video_from_frames(input_folder: str = "generated", output_path: str = "output/output.mp4", fps: int = 1):
    """
    Creates a video from a sequence of frames using FFmpeg.
    """
    import os
    import subprocess
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    input_pattern = os.path.join(input_folder, "frame_%04d.png")
    command = [
        "ffmpeg",
        "-framerate", str(fps),
        "-i", input_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    try:
        print(f"Executing FFmpeg command: {' '.join(command)}")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("FFmpeg output:", result.stdout)
        print(f"Video created successfully at '{output_path}'.")
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please ensure it is installed and in your PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error during FFmpeg execution: {e.stderr}") 