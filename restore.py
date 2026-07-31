import os, io, numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(MODEL_DIR, exist_ok=True)


def colorize_image(image_bytes):
    """Colorize B&W: AI model if available, else smart CV2 colorization"""
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    arr = np.array(img)

    # Enhance contrast first
    img = ImageOps.autocontrast(img, cutoff=2)
    img = ImageEnhance.Sharpness(img).enhance(1.3)
    arr = np.array(img)

    # Try AI model
    caffemodel = os.path.join(MODEL_DIR, 'colorization_release_v2.caffemodel')
    if os.path.exists(caffemodel) and os.path.getsize(caffemodel) > 1000000:
        try:
            import cv2
            prototxt = os.path.join(MODEL_DIR, 'colorization_deploy_v2.prototxt')
            pts_npy = os.path.join(MODEL_DIR, 'pts_in_hull.npy')
            if os.path.exists(prototxt) and os.path.exists(pts_npy):
                bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
                net = cv2.dnn.readNetFromCaffe(prototxt, caffemodel)
                pts = np.load(pts_npy).transpose().reshape(2, 313, 1, 1)
                net.getLayer(net.getLayerId('class8_ab')).blobs = [pts.astype(np.float32)]
                net.getLayer(net.getLayerId('conv8_313_rh')).blobs = [np.zeros([1, 313], dtype=np.float32)]
                lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
                L = lab[:, :, 0]
                L_in = cv2.resize(L, (224, 224)).astype(np.float32) / 255.0 - 0.5
                net.setInput(cv2.dnn.blobFromImage(L_in))
                ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
                ab = cv2.resize(ab, (arr.shape[1], arr.shape[0]))
                result = np.concatenate((L[:, :, np.newaxis], ab), axis=2).astype(np.uint8)
                result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
                result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
                img_out = Image.fromarray(result)
                img_out = ImageEnhance.Color(img_out).enhance(1.2)
                buf = io.BytesIO()
                img_out.save(buf, format='PNG')
                buf.seek(0)
                return buf.getvalue()
        except Exception:
            pass

    # Smart fallback: adaptive colorization
    try:
        import cv2
        gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
        # CLAHE for better local contrast
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        # Try BONE colormap (warm tones)
        colored = cv2.applyColorMap(gray, cv2.COLORMAP_BONE)
        colored = cv2.cvtColor(colored, cv2.COLOR_BGR2RGB)
        img_out = Image.fromarray(colored)
        img_out = ImageEnhance.Color(img_out).enhance(1.3)
        img_out = ImageEnhance.Contrast(img_out).enhance(1.1)
        buf = io.BytesIO()
        img_out.save(buf, format='PNG')
        buf.seek(0)
        return buf.getvalue()
    except Exception:
        pass

    # Pillow fallback
    gray = img.convert('L')
    gray = ImageEnhance.Contrast(gray).enhance(1.5)
    gray = gray.filter(ImageFilter.SHARPEN)
    tinted = Image.merge('RGB', (
        gray.point(lambda x: min(255, x + 20)),
        gray.point(lambda x: min(255, x + 8)),
        gray.point(lambda x: max(0, x - 8)),
    ))
    buf = io.BytesIO()
    tinted.save(buf, format='PNG')
    buf.seek(0)
    return buf.getvalue()
