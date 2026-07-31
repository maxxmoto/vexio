import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings('ignore')

_reader = None

def get_reader():
    global _reader
    if _reader is None:
        import easyocr
        _reader = easyocr.Reader(['ru', 'en'], gpu=False, verbose=False)
    return _reader

def recognize_text(image_bytes, lang='ru+en'):
    reader = get_reader()
    import numpy as np
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img_array = np.array(img)
    results = reader.readtext(img_array)
    text_parts = []
    for bbox, text, conf in results:
        text_parts.append(text)
    return {
        'text': '\n'.join(text_parts),
        'confidence': round(sum(r[2] for r in results) / len(results) * 100, 1) if results else 0,
        'blocks': [{'text': r[1], 'confidence': round(r[2] * 100, 1)} for r in results]
    }
