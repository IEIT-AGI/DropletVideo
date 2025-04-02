import csv
from loguru import logger
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any


def parse_args() -> argparse.Namespace:
    """Parse command line arguments
    
    Returns:
        argparse.Namespace: Object containing parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Extract YouTube IDs for download")
    parser.add_argument("-csv_file",
                        type=str,
                        required=True,
                        help="Path to the input CSV file")
    parser.add_argument(
        "-save_dir",
        type=str,
        default='./',
        help="Directory to save output files (default: current directory)")
    return parser.parse_args()


def write_txt(file_path: Path, data: List[str]) -> None:
    """Write data to a text file
    
    Args:
        file_path: Path object for the output file
        data: List of strings to write
    """
    try:
        with file_path.open("w", encoding="utf-8") as f:
            f.writelines(f"{d}\n" for d in data)
        logger.success(f"Successfully wrote {len(data)} items to {file_path}")
    except IOError as e:
        logger.error(f"Failed to write to {file_path}: {e}")
        raise


def write_json(file_path: Path, data: Any) -> None:
    """Write data to a JSON file
    
    Args:
        file_path: Path object for the output file
        data: Data to be serialized
    """
    try:
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.success(f"Successfully wrote JSON to {file_path}")
    except (IOError, TypeError) as e:
        logger.error(f"Failed to write JSON to {file_path}: {e}")
        raise


def read_csv(csv_path: Path) -> Dict[str, List[dict]]:
    """Read CSV file and extract YouTube IDs with related data
    
    Args:
        csv_path: Path object for the input CSV file
        
    Returns:
        Dictionary with YouTube IDs as keys and lists of related data as values
    """
    dataset: Dict[str, List[dict]] = {}
    try:
        with csv_path.open('r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if "url" not in row:
                    logger.warning(
                        f"Missing 'url' column in CSV file {csv_path}")
                    continue

                url = row.pop("url")
                if not url.startswith('https://www.youtube.com/watch?v='):
                    logger.warning(f"Invalid YouTube URL format: {url}")
                    continue

                video_id = url.replace('https://www.youtube.com/watch?v=', "")
                if not video_id:
                    logger.warning(f"Empty video ID from URL: {url}")
                    continue

                dataset.setdefault(video_id, []).append(row)

        logger.info(
            f"Successfully processed {len(dataset)} unique YouTube IDs from {csv_path}"
        )
        return dataset
    except (IOError, csv.Error) as e:
        logger.error(f"Failed to read CSV file {csv_path}: {e}")
        raise


def main() -> None:
    args = parse_args()

    try:
        csv_path = Path(args.csv_file)
        save_dir = Path(args.save_dir)

        save_dir.mkdir(parents=True, exist_ok=True)

        dataset = read_csv(csv_path)

        if not dataset:
            logger.warning("No valid data found in CSV file")
            return

        txt_path = save_dir / 'youtube_id.txt'
        json_path = save_dir / f"{csv_path.stem}.json"

        # Write output files
        write_txt(txt_path, dataset.keys())
        write_json(json_path, dataset)

    except Exception as e:
        logger.critical(f"Program failed: {e}")
        raise


if __name__ == "__main__":
    main()
