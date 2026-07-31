import io
from PIL import Image

_model = None

def _load():
    global _model
    if _model is None:
        from opennsfw2 import predict_image
        _model = predict_image
    return _model

def check_image(image_bytes, threshold=0.7):
    """Returns True if image is NSFW (score > threshold)"""
    try:
        predict = _load()
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        score = predict(img)
        return score > threshold, float(score)
    except Exception:
        return False, 0.0
