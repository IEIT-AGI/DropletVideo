本教程以DropletVideo-1M为例，介绍如何去下载DropletVideo数据集，具体步骤如下
1. 申请[DropletVideo-1M](https://huggingface.co/datasets/DropletX/DropletVideo-1M)数据，并下载对应的csv文件
2. 运行extract_download_yt_ids.py脚本，提取待下载的YouTube ID（如youtube_id.txt）以及样本的相关信息(DropletVideo-1M.json)
   ```python
    python extract_download_yt_ids.py -csv_file csv_file_path -save_dir save_path
    ```
3. 执行download_video.sh脚本，下载YouTube ID对应的视频
    ```bash
   bash download_video.sh youtube_id.txt video_save_path
   ```
4. 执行generate_samples.py脚本，根据步骤3已下载的视频以及样本的信息，进一步生成样本
    ```python
    python generate_samples.py -video_dir video_save_path -droplet_json DropletVideo-1M.json -save_dir sample_save_path
    ```
   