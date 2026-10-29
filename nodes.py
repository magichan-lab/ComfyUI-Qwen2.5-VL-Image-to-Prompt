import torch
import numpy as np
from PIL import Image

DEFAULT_INSTRUCTION = ("Describe this image as a detailed English text-to-image generation prompt. "
                       "Describe only visible details: subject, appearance, pose, clothing, environment, "
                       "composition, lighting, colors and style. Output only the prompt, no preface.")

class Qwen25VLImageToPrompt:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "image": ("IMAGE",),
            "instruction": ("STRING", {"multiline": True, "default": DEFAULT_INSTRUCTION}),
            "append_prompt": ("STRING", {"multiline": True, "default": "highly detailed, natural lighting"}),
            "model_id": ("STRING", {"default": "Qwen/Qwen2.5-VL-3B-Instruct"}),
            "max_new_tokens": ("INT", {"default": 256, "min": 32, "max": 1024, "step": 32}),
        }}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)
    FUNCTION = "run"
    CATEGORY = "Qwen2.5-VL/Image to Prompt"
    OUTPUT_NODE = True
    _model = None
    _processor = None
    _loaded_id = None

    def run(self, image, instruction, append_prompt, model_id, max_new_tokens):
        from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
        if self.__class__._loaded_id != model_id:
            self.__class__._model = None
            self.__class__._processor = None
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            self.__class__._processor = AutoProcessor.from_pretrained(model_id)
            self.__class__._model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                model_id, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else "cpu",
            ).eval()
            self.__class__._loaded_id = model_id
        processor = self.__class__._processor
        model = self.__class__._model
        rgb = (image[0].detach().cpu().numpy().clip(0, 1) * 255).astype(np.uint8)
        pil_image = Image.fromarray(rgb).convert("RGB")
        messages = [{"role": "user", "content": [
            {"type": "image", "image": pil_image},
            {"type": "text", "text": instruction},
        ]}]
        prompt = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = processor(text=[prompt], images=[pil_image], padding=True, return_tensors="pt")
        inputs = inputs.to(next(model.parameters()).device)
        with torch.inference_mode():
            generated = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        generated = generated[:, inputs.input_ids.shape[1]:]
        caption = processor.batch_decode(generated, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0].strip()
        suffix = append_prompt.strip()
        final = caption + (", " + suffix if suffix else "")
        return {"ui": {"text": [final]}, "result": (final,)}

NODE_CLASS_MAPPINGS = {
    "Qwen25VLImageToPrompt": Qwen25VLImageToPrompt,
    # Keep existing workflows loadable after the node is renamed.
    "Krea2ImageToPrompt": Qwen25VLImageToPrompt,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Qwen25VLImageToPrompt": "Qwen2.5-VL Image to Prompt",
    "Krea2ImageToPrompt": "Krea2 Image to Prompt (legacy)",
}
