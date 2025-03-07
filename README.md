<p align="center">
  <img src="assets/logo.jpg"  height=360>
</p>


### <div align="center">  DropletVideo: A Dataset and Approach to Explore Integral Spatio-Temporal Consistent Video Generation <div> 
<div align="center">
  <a href="https://nju-pcalab.github.io/projects/dropletvideo/"><img src="https://img.shields.io/static/v1?label=DropletVideo-10M&message=Project&color=purple"></a> &ensp;
  <a href="https://arxiv.org/abs/2407.02371"><img src="https://img.shields.io/static/v1?label=Paper&message=Arxiv&color=red&logo=arxiv"></a> &ensp;
  <a href="https://huggingface.co/datasets/DropletX/DropletVideo-10M"><img src="https://img.shields.io/static/v1?label=Dataset&message=HuggingFace&color=yellow"></a>
</div>



English | [简体中文](README_zh-CN.md)
</div>

<br>

## ✈️ Introduction

**DropletVideo** is a project exploring high-order spatio-temporal consistency in image-to-video generation. It is trained on DropletVideo-10M. The model supports multi-resolution inputs, dynamic FPS control for motion intensity, and demonstrates potential for 3D consistency. The model supports multi-resolution inputs, dynamic FPS control for motion intensity, and demonstrates potential for 3D consistency. For further details, you can check our [project page](https://dropletx.github.io/) as well as the [technical report](https://huggingface.co/datasets/DropletX/DropletVideo-10M).


## 🔥 Features

1. Multi-resolution inputs， accommodating pixel values from 512x512x85（default 672x384x85） to 896x896x85（default 1120x640x85, and videos with different aspect ratios.
2. Dynamic FPS control for motion intensity.

<br>

## 🚀 Installation
**Follow the steps below to set up the environment for our project.**

Our tested System Environment:

```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2022 NVIDIA Corporation
Built on Wed_Sep_21_10:33:58_PDT_2022
Cuda compilation tools, release 11.8, V11.8.89
Build cuda_11.8.r11.8/compiler.31833905_0

NVIDIA A100-SXM4-80GB
Driver Version: 550.144.03 


```


    
1. (Optional) Create a conda environment and activate it:
    
    ```bash
    conda create -n DropletVideo python=3.8
    conda activate DropletVideo
    ```
    
2. Install the required dependencies:
    
    ```bash
    cd DropletVideo_inference
    pip install -r requirements.txt
    ```
    
   We provide a `requirements.txt` file that contains all necessary dependencies for easy installation.



3. The DropletVideo-5B checkpoints have been uploaded to [Huggingface](https://huggingface.co/DropletX/DropletVideo-5B).

   The distribution of internal model weights is as follows:
   
   The text_encoder as well as the tokenizer employs the google-t5 model weights(without training). The scheduler is the denoise strategy 
   during inference. The vae is the pixel-to-latent network for our project. The transformer contains our 5B transformer model weights. 

    ```
    DropletVideo-V1.0-weights/
    ├── configuration.json
    ├── LICENSE
    ├── model_index.json
    ├── scheduler
    │     └── scheduler_config.json
    ├── text_encoder
    │     ├── config.json
    │     ├── model-00001-of-00002.safetensors
    │     ├── model-00002-of-00002.safetensors
    │     └── model.safetensors.index.json
    ├── tokenizer
    │     ├── added_tokens.json
    │     ├── special_tokens_map.json
    │     ├── spiece.model
    │     └── tokenizer_config.json
    ├── transformer
    │     ├── config.json
    │     └── diffusion_pytorch_model.safetensors
    └── vae
          ├── config.json
          └── diffusion_pytorch_model.safetensors
    ```   


#### Notation:
   
   All the model weights are stored in safetensors. Satetensors is a file format designed for stroing tensor data, aiming to provide efficient
   and secure read and write operations. It is commonly used to store weights and parameters in machine learning models. Below are methods for reading
   safetensors. You can check the model_weights from the state_dict variable.
   
   ```
   from safetensors.torch import load_file
   state_dict = load_file(file_path)
   ```


<br>

## ⚡ Usage
Once the installation is complete, you can run the demo using the following command:

```bash
python inference.py --ckpt DropletVideo-V1.0-weights --ref_img_dir your_path_to_ref_img --FPS 4 --prompt yout_text_input
```

#### Example:
```bash
python inference.py --ckpt DropletVideo-V1.0-weights --ref_img_dir assets/752.jpg --FPS 4 --prompt "The video showcases a magnificent music hall, with the focal point being a black triangular piano in the center. The entire scene is elegant and rich in artistic atmosphere. The video begins with warm lighting that illuminates the ornate ceiling, followed by a lavish chandelier. These chandeliers are arranged in a circular pattern, with a soft white light emanating from the center. The wall decorations and carvings are exquisite, with the walls predominantly featuring gold and ivory white, creating a sense of solemnity and elegance. The camera moves from the left rear of the piano to the right, revealing every decorative detail of the music hall, including the second-floor gallery, ornate arched windows with decorations, and rows of empty seats facing the audience. As the camera pans, the piano's outline becomes more distinct, with the half-open lid revealing the smooth black keys that glow slightly under the spotlight. As the movement continues, the acoustic structure of the hall, such as the wooden floor and sound-absorbing walls, is gradually revealed, making the space more suitable for music performance. The video concludes with the camera stopping at the center, showcasing the entire hall, with the piano and background forming a beautiful artistic landscape. The hall is spacious, but its design and decoration convey a sense of solemnity and tranquility."
```


### Command Line Arguments

#### 1. required arguments
- `--ckpt`: Path to the model weights.
- `--ref_img_dir`: The input condition img path
- `--FPS`: The input condition FPS control the motion strength
- `--prompt`: The input text


#### 2. Other arguments
- `--width`: The width of the generated video
- `--height`: The height of the generated video
- `--video_length`: The frame num of the generated video
- `--num_inference_steps`: The denoise step for inference. Normally, the quality of the generated video will be better 
                           if the value is higher but with higher computation cost. Normally, we set it to 50.
- `--seed`: The random seed for the inference, different seeds will generate different results.
- `--guidance_scale`: The guidance scale of the denoise process. The value determines the relationship between the input 
                      prompt and the generated video. The higher value, the more relative. 

#### Notation:
DropletVideo can support any-resolution input.(But for this version we did not add the auto-padding function, the input width and height must be divided by 16)
The default width, height and video_length is set to 672, 384 and 85. This setting can generate videos in a single A100-40GB GPU card.
You can minimize these parameters during the debug process of the optimization.






## 🙏 Credits
This project leverages the following open-source frameworks. We appreciate their contributions and efforts in making this work possible.

- [**CogVideoX-Fun**](https://github.com/aigc-apps/CogVideoX-Fun) - Training Strategies
- [**CogVideoX**](https://github.com/THUDM/CogVideo) - VAE compression
- [**EasyAnimate**](https://github.com/aigc-apps/EasyAnimate) - I2V model configuration
- [**Open-Sora-Plan**](https://github.com/PKU-YuanGroup/Open-Sora-Plan) - Data processing
- [**Open-Sora**](https://github.com/hpcaitech/Open-Sora) - Extra control




<br>

## ☎️ Contact us
If you have any questions, comments, or suggestions, please contact us at [zrzsgsg@gmail.com](mailto:zrzsgsg@gmail.com).

<br>

## 📄 License
This project is released under the [Apache 2.0 license](resources/LICENSE).

