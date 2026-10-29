# Qwen2.5-VL Image to Prompt for ComfyUI

[日本語版 README](README.ja.md)

Generate an English text-to-image prompt from an input image with the local [Qwen2.5-VL-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct) model. This repository contains one ComfyUI custom node and an example workflow that previews a trial image from the generated prompt. The custom node alone does not generate images.

## What it does

- Accepts a ComfyUI `IMAGE` and describes its visible content as a text-to-image prompt.
- Lets you edit the instruction, appended prompt, model ID, and maximum output length.
- Displays the resulting text in the node and exposes it as a `STRING` output for downstream nodes.
- Uses the first image when the input is a batch.

The default model is downloaded from Hugging Face on first use and cached by Transformers. Model weights are not included in this repository. A CUDA GPU is recommended; CPU inference is possible but slow and requires substantial memory. The model's own license and terms apply to its weights.

## Install

### ComfyUI Manager

Once this package has been published to the [Comfy Registry](https://registry.comfy.org/), search for **Qwen2.5-VL Image to Prompt** in ComfyUI Manager and install it. Restart ComfyUI after installation.

Until it is listed, install the repository using Manager's Git URL installation option if available in your Manager setup, or use the manual method below.

### Manual installation

From your ComfyUI installation directory:

```bash
cd custom_nodes
git clone https://github.com/magichan-lab/ComfyUI-Qwen2.5-VL-Image-to-Prompt.git
cd ComfyUI-Qwen2.5-VL-Image-to-Prompt
python -m pip install -r requirements.txt
```

Use the Python environment that runs ComfyUI for the `pip` command, then restart ComfyUI. ComfyUI supplies PyTorch and NumPy; this package's additional dependencies are in [`requirements.txt`](requirements.txt).

## Use the example workflow

1. Open [`workflows/qwen25vl_image_to_prompt.json`](workflows/qwen25vl_image_to_prompt.json) in ComfyUI.
2. In **Load Image**, choose an image from your ComfyUI input directory. The included `example.png` value is a placeholder, not a bundled image.
3. In **Load Checkpoint**, select an image-generation checkpoint from ComfyUI's `models/checkpoints` directory. The included `select_your_checkpoint.safetensors` value is a placeholder. This checkpoint is separate from the Qwen2.5-VL model selected by `model_id`.
4. Queue the workflow. Its `final_prompt` feeds the positive prompt, and **Preview Image** shows a trial image. Optionally enter unwanted elements in **Negative prompt (optional)**.
5. Compare the input and trial images, adjust the instruction or `append_prompt` in **Qwen2.5-VL Image to Prompt**, and queue again. Keep the **KSampler** seed set to `fixed` while comparing prompt changes.

The default instruction asks for visible details only. Review the generated prompt; image descriptions can be incomplete or inaccurate. The `model_id` field is intended for compatible Qwen2.5-VL checkpoints. The sample generates a 512 × 512 trial image. Adjust **Empty Latent Image** dimensions and **KSampler** settings for your image-generation checkpoint. **Preview Image** does not persist the image; add **Save Image** if you want to keep it.

## Repository layout

```text
.
├── __init__.py                 # ComfyUI node entry point
├── nodes.py                    # Node implementation
├── requirements.txt            # Dependencies installed by Manager
├── pyproject.toml              # Comfy Registry metadata
├── workflows/
│   └── qwen25vl_image_to_prompt.json
├── LICENSE
├── README.md
└── README.ja.md
```

The current node ID is `Qwen25VLImageToPrompt`. The previous `Krea2ImageToPrompt` ID remains as a compatibility alias so existing workflows can still load.

## Before publishing to ComfyUI Manager

1. Push these files to the root of [magichan-lab/ComfyUI-Qwen2.5-VL-Image-to-Prompt](https://github.com/magichan-lab/ComfyUI-Qwen2.5-VL-Image-to-Prompt).
2. Create a publisher at the [Comfy Registry](https://registry.comfy.org/) and replace `YOUR_PUBLISHER_ID` in `pyproject.toml` with its exact ID. Keep the package name `qwen25vl-image-to-prompt` if that Registry ID is available; Registry node names cannot be changed after creation.
3. Publish a version with `comfy node publish` or the Registry's supported GitHub Actions workflow. Manager uses the Registry to discover published nodes. See the [official publishing guide](https://docs.comfy.org/registry/publishing).

For a legacy Manager listing, follow the [Manager registration guide](https://docs.comfy.org/custom-nodes/backend/manager) and submit the repository URL to its `custom-node-list.json` by pull request. This repository is prepared for registration, but it is not yet registered or published.

## License

The custom node code and workflow are licensed under the [MIT License](LICENSE). Qwen2.5-VL model weights are distributed separately under their own terms.
