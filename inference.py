
import json
import os

import numpy as np
import torch

from diffusers import DDIMScheduler
from transformers import T5EncoderModel
from transformer import DropletVideoTransformer3DModel
from vae import AutoencoderKLDropletVideo
from pipeline import DropletVideo_Pipeline_Inpaint
from PIL import Image
from utils import get_image_to_video_latent, save_videos_grid
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Simple example of a inference script.")
    parser.add_argument(
        "--width", type=int, default=672, help="The width of the output video"
    )
    parser.add_argument(
        "--height", type=int, default=384, help="The height of the output video"
    )
    parser.add_argument(
        "--video_length", type=int, default=85, help="The length of the output video"
    )
    parser.add_argument(
        "--FPS", type=int, default=16, help="The FPS input control of the output video"
    )
    parser.add_argument(
        "--num_inference_steps", type=int, default=50, help="The denoise steps"
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="The random seed"
    )
    parser.add_argument(
        "--guidance_scale", type=float, default=6.0, help="The guidance scale"
    )

    parser.add_argument(
        "--ckpt",
        type=str,
        default="DropletVideo-V1.0-weights",
        required=True,
        help="Path to the DropletVideo-5B model weights.",
    )

    parser.add_argument(
        "--prompt",
        type=str,
        default="The video showcases a magnificent music hall, with the focal point being a black triangular piano in the center. The entire scene is elegant and rich in artistic atmosphere. The video begins with warm lighting that illuminates the ornate ceiling, followed by a lavish chandelier. These chandeliers are arranged in a circular pattern, with a soft white light emanating from the center. The wall decorations and carvings are exquisite, with the walls predominantly featuring gold and ivory white, creating a sense of solemnity and elegance. The camera moves from the left rear of the piano to the right, revealing every decorative detail of the music hall, including the second-floor gallery, ornate arched windows with decorations, and rows of empty seats facing the audience. As the camera pans, the piano's outline becomes more distinct, with the half-open lid revealing the smooth black keys that glow slightly under the spotlight. As the movement continues, the acoustic structure of the hall, such as the wooden floor and sound-absorbing walls, is gradually revealed, making the space more suitable for music performance. The video concludes with the camera stopping at the center, showcasing the entire hall, with the piano and background forming a beautiful artistic landscape. The hall is spacious, but its design and decoration convey a sense of solemnity and tranquility.",
        required=True
    )

    parser.add_argument(
        "--ref_img_dir",
        type=str,
        default="assets/752.jpg",
        required=True,
        help="the reference image dir",
    )
    args = parser.parse_args()
    return args



def main():
    args = parse_args()
    sample_width = args.width
    sample_height = args.height

    sample_size         = [sample_height, sample_width]
    video_length        = args.video_length
    weight_dtype            = torch.bfloat16
    validation_image_end    = None
    FPS = args.FPS
    guidance_scale          = args.guidance_scale
    seed                    = args.seed
    num_inference_steps     = args.num_inference_steps

    model_name          = args.ckpt

    prompt = args.prompt
    ref_img_dir = args.ref_img_dir

    transformer = DropletVideoTransformer3DModel.from_pretrained_2d(
        model_name,
        subfolder="transformer",
    ).to(weight_dtype)


    vae = AutoencoderKLDropletVideo.from_pretrained(
        model_name,
        subfolder="vae"
    ).to(weight_dtype)

    text_encoder = T5EncoderModel.from_pretrained(
        model_name, subfolder="text_encoder", torch_dtype=weight_dtype
    )

    scheduler = DDIMScheduler.from_pretrained(
        model_name,
        subfolder="scheduler"
    )

    pipeline = DropletVideo_Pipeline_Inpaint.from_pretrained(
        model_name,
        vae=vae,
        text_encoder=text_encoder,
        transformer=transformer,
        scheduler=scheduler,
        torch_dtype=weight_dtype
    )

    low_gpu_memory_mode = False
    if low_gpu_memory_mode:
        pipeline.enable_sequential_cpu_offload()
    else:
        pipeline.enable_model_cpu_offload()




    generator = torch.Generator(device="cuda").manual_seed(seed)
    prompt = prompt + " " + "The video is of high quality, and the view is very clear. High quality, masterpiece, best quality, highres, ultra-detailed, fantastic."
    negative_prompt         = "The video is low quality, blurry, distortion. "
    video_length = int((video_length - 1) // vae.config.temporal_compression_ratio * vae.config.temporal_compression_ratio) + 1 if video_length != 1 else 1
    input_video, input_video_mask, clip_image = get_image_to_video_latent(ref_img_dir, validation_image_end, video_length=video_length, sample_size=sample_size)
    os.makedirs("samples", exist_ok=True)
    save_path = os.path.join("samples", ref_img_dir.split("/")[-1].replace(".jpg", f"_FPS{FPS}.mp4"))
    with torch.no_grad():
        sample = pipeline(
            prompt,
            num_frames = video_length,
            negative_prompt = negative_prompt,
            height      = sample_size[0],
            width       = sample_size[1],
            generator   = generator,
            guidance_scale = guidance_scale,
            num_inference_steps = num_inference_steps,
            max_sequence_length = 400,
            video        = input_video,
            mask_video   = input_video_mask,
            fps = [FPS]
        ).videos


        save_videos_grid(sample, save_path, fps=8)

    print("over")


if __name__ == "__main__":
    main()


















