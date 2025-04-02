import json
from glob import glob
from pathlib import Path
from typing import Dict, List, Any, Tuple
from moviepy import VideoFileClip
from loguru import logger
import ast
import argparse
from rich.progress import Progress, TimeRemainingColumn, TimeElapsedColumn, BarColumn, MofNCompleteColumn, TextColumn
from tqdm import tqdm


def read_json(file_path: Path) -> Dict:
    """Read JSON file with proper error handling."""
    logger.info(f"Reading {file_path}")
    try:
        with file_path.open('r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Failed to read JSON file {file_path}: {e}")
        raise


def write_json(file_path: Path, data: Any) -> None:
    """Write data to JSON file with error handling."""
    try:
        with file_path.open('w') as f:
            json.dump(data, f, indent=4)
        logger.success(f"Successfully wrote JSON to {file_path}")
    except (IOError, TypeError) as e:
        logger.error(f"Failed to write JSON to {file_path}: {e}")
        raise


def frame_to_timestamp(frame_number: int, fps: float) -> str:
    """Convert frame number to HH:MM:SS.ff format."""
    total_seconds = frame_number / fps
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{seconds:05.2f}"


def convert_timestamp(framestamp: Tuple[int, int],
                      fps: float) -> Tuple[str, str]:
    """Convert frame range to start and end timestamps."""
    return (frame_to_timestamp(framestamp[0],
                               fps), frame_to_timestamp(framestamp[1], fps))


def process_single_video(video_path: Path, video_infos: List[Dict],
                         save_dir: Path, video_id: str) -> List[Dict]:
    """
    Process a single video file to extract clips based on provided segments.
    
    Args:
        video_path: Path to the video file
        video_infos: List of dictionaries containing clip information
        save_dir: Directory to save extracted clips
        video_id: Identifier for the video
        
    Returns:
        List of dictionaries containing processed clip information
    """
    samples = []

    try:
        with VideoFileClip(str(video_path)) as video_data:
            for v_info in tqdm(video_infos,
                               desc=f"Processing segments",
                               leave=False):
                try:
                    # Validate and extract parameters
                    fps = ast.literal_eval(v_info.get("fps", "0"))
                    framestamp = ast.literal_eval(
                        v_info.get("framestamp", "(0,0)"))
                    quality_score = ast.literal_eval(
                        v_info.get('quality_score', "0"))

                    # Convert frame numbers to timestamps
                    start_time, end_time = convert_timestamp(framestamp, fps)

                    # Generate output filename
                    clip_name = (f"{video_id}--"
                                 f"{framestamp[0]:06d}_{framestamp[1]:06d}-"
                                 f"{quality_score}")
                    output_path = save_dir / f"{clip_name}.mp4"

                    # Process and save the clip
                    with video_data.subclipped(start_time, end_time) as clip:
                        clip.write_videofile(str(output_path),
                                             logger=None,
                                             threads=8,
                                             preset="fast")

                    samples.append({clip_name: v_info})

                except (ValueError, KeyError) as e:
                    logger.warning(f"Skipping invalid segment {v_info}: {e}")
                except Exception as e:
                    logger.error(f"Failed to process segment {v_info}: {e}")

    except Exception as e:
        logger.error(f"Failed to process video {video_path}: {e}")
        raise

    return samples


def parse_args() -> argparse.Namespace:
    """Parse and validate command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate training samples from videos")
    parser.add_argument("-video_dir",
                        type=str,
                        required=True,
                        help="Directory containing video files")
    parser.add_argument("-droplet_json",
                        type=str,
                        required=True,
                        help="Path to the droplet JSON file")
    parser.add_argument(
        "-save_dir",
        type=str,
        default='./',
        help="Directory to save output samples (default: current directory)")
    return parser.parse_args()


def main() -> None:
    """Main processing function."""
    args = parse_args()

    try:
        # Convert paths to Path objects
        video_dir = Path(args.video_dir)
        droplet_json = Path(args.droplet_json)
        save_dir = Path(args.save_dir)

        # Create output directory
        save_video_path = save_dir / "videos"
        save_video_path.mkdir(parents=True, exist_ok=True)

        # Get JSON prefix for output filename
        prefix = droplet_json.stem

        # Load dataset
        dataset = read_json(droplet_json)

        # Process video files
        samples = []
        video_files = glob(str(video_dir / "**" / "*.mp4"), recursive=True)

        progress = Progress(TextColumn("[bold blue]{task.description}"),
                            BarColumn(bar_width=None),
                            MofNCompleteColumn(),
                            "[progress.percentage]{task.percentage:>3.0f}%",
                            TimeElapsedColumn(),
                            TimeRemainingColumn(),
                            refresh_per_second=10,
                            expand=True)

        with progress:
            main_task = progress.add_task("[cyan]Processing videos...",
                                          total=len(video_files),
                                          visible=True)

            for video_file in video_files:
                video_path = Path(video_file)
                video_id = video_path.stem

                progress.console.log(f"Processing: {video_id}")

                if video_id in dataset:
                    try:
                        video_samples = process_single_video(
                            video_path, dataset[video_id], save_video_path,
                            video_id)
                        samples.extend(video_samples)
                    except Exception as e:
                        logger.error(
                            f"Skipping video {video_id} due to error: {e}")
                else:
                    logger.warning(f"Video ID {video_id} not found in dataset")

                progress.update(main_task, advance=1, refresh=True)

            # Save results
            output_json = save_dir / f"{prefix}-dataset.json"
            write_json(output_json, samples)
            progress.console.print(
                f"[green]✓ Successfully saved to {output_json}")

    except Exception as e:
        logger.critical(f"Processing failed: {e}")
        raise


if __name__ == "__main__":
    main()
