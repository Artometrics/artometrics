from __future__ import annotations

import numpy as np
import torch
from PIL import Image

FASHION_VOCAB = [
    "gown",
    "evening gown",
    "cocktail dress",
    "halter gown",
    "feather gown",
    "nude gown",
    "black dress",
    "white dress",
    "high low skirt",
    "skirt",
    "leopard skirt",
    "suede skirt",
    "leather skirt",
    "suit",
    "yellow suit",
    "cream coat",
    "teal suit",
    "trench coat",
    "bodysuit",
    "corset",
    "corset top",
    "tube top",
    "mesh dress",
    "neoprene gown",
    "velvet dress",
    "black velvet",
    "beaded dress",
    "feathers",
    "beading",
    "wedding dress",
    "red carpet",
    "runway",
    "fashion week",
    "music video set",
    "stage performance",
    "concert tour",
    "talk show",
    "press event",
    "awards show",
    "oscars",
    "grammys",
    "golden globes",
    "emmys",
    "naacp awards",
    "peoples choice awards",
    "hollywood bowl",
    "superbowl",
    "coachella",
]

_model = None
_preprocess = None
_tokenizer = None
_text_features = None
_device = None


def _load():
    global _model, _preprocess, _tokenizer, _text_features, _device
    if _model is not None:
        return
    import open_clip

    from .config import CLIP_MODEL, CLIP_PRETRAINED

    _device = "mps" if torch.backends.mps.is_available() else "cpu"
    _model, _, _preprocess = open_clip.create_model_and_transforms(
        CLIP_MODEL, pretrained=CLIP_PRETRAINED
    )
    _tokenizer = open_clip.get_tokenizer(CLIP_MODEL)
    _model = _model.to(_device).eval()
    prompts = [f"a photo of a {t}" for t in FASHION_VOCAB]
    with torch.no_grad():
        tokens = _tokenizer(prompts).to(_device)
        _text_features = _model.encode_text(tokens)
        _text_features /= _text_features.norm(dim=-1, keepdim=True)


def encode_image(path) -> np.ndarray:
    _load()
    with Image.open(path) as im:
        im = im.convert("RGB")
        t = _preprocess(im).unsqueeze(0).to(_device)
    with torch.no_grad():
        feat = _model.encode_image(t)
        feat /= feat.norm(dim=-1, keepdim=True)
    return feat.cpu().numpy().astype(np.float16).reshape(-1)


def zero_shot_tags(path, top_k: int = 8, min_score: float = 0.18) -> tuple[list[str], dict[str, float]]:
    _load()
    with Image.open(path) as im:
        im = im.convert("RGB")
        t = _preprocess(im).unsqueeze(0).to(_device)
    with torch.no_grad():
        img_feat = _model.encode_image(t)
        img_feat /= img_feat.norm(dim=-1, keepdim=True)
        logits = (100.0 * img_feat @ _text_features.T).softmax(dim=-1).cpu().numpy()[0]
    ranked = sorted(
        zip(FASHION_VOCAB, logits.tolist()),
        key=lambda x: x[1],
        reverse=True,
    )
    tags = [t for t, s in ranked[:top_k] if s >= min_score]
    scores = {t: round(float(s), 4) for t, s in ranked[:top_k]}
    return tags, scores


def text_image_similarity(text: str, image_embedding: np.ndarray) -> float:
    _load()
    with torch.no_grad():
        tokens = _tokenizer([text]).to(_device)
        text_feat = _model.encode_text(tokens)
        text_feat /= text_feat.norm(dim=-1, keepdim=True)
    img = torch.from_numpy(image_embedding.astype(np.float32)).to(_device)
    img /= img.norm()
    sim = float((img @ text_feat.T).cpu().item())
    return sim
