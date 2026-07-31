import os, io
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from PIL import Image

import warnings
warnings.filterwarnings('ignore')

_session = None

def get_session():
    global _session
    if _session is None:
        from rembg.session_factory import new_session
        _session = new_session('u2net')
    return _session

def remove_background(image_bytes, output_format='PNG'):
    from rembg import remove
    session = get_session()
    input_img = Image.open(io.BytesIO(image_bytes))
    output_img = remove(input_img, session=session)
    buf = io.BytesIO()
    output_img.save(buf, format=output_format)
    buf.seek(0)
    return buf.getvalue()
