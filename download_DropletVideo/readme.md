This tutorial uses DropletVideo-1M as an example to demonstrate how to download the DropletVideo dataset. The specific steps are as follows:

1. Request access to [DropletVideo-1M](https://huggingface.co/datasets/DropletX/DropletVideo-1M) and download the corresponding CSV file.
2. Run the extract_download_yt_ids.py script to extract YouTube IDs for download (e.g., youtube_id.txt) and sample-related information (DropletVideo-1M.json):
    ```python
    python extract_download_yt_ids.py -csv_file csv_file_path -save_dir save_path
    ```
3. Run the download_video.sh script to download videos corresponding to the YouTube IDs:
   ```bash
   bash download_video.sh youtube_id.txt video_save_path
   ```

4. Run the generate_samples.py script to generate samples based on the videos and sample information:
    ```python
    python generate_samples.py -video_dir video_save_path -droplet_json DropletVideo-1M.json -save_dir sample_save_path
    ```
