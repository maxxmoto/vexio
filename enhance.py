import io
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


def enhance_image(image_bytes, sharpen=1.5, contrast=1.2, color=1.1, brightness=1.05, upscale=2, denoise=True, auto_levels=True):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    orig_size = img.size

    # Auto-levels: stretch histogram for better contrast
    if auto_levels:
        img = ImageOps.autocontrast(img, cutoff=1)

    # Denoise: median filter + slight blur
    if denoise:
        img = img.filter(ImageFilter.MedianFilter(3))
        img = img.filter(ImageFilter.SMOOTH_MORE)

    # Detail enhancement: unsharp mask
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    # Color, contrast, brightness, sharpness
    if abs(sharpen - 1.0) > 0.01:
        img = ImageEnhance.Sharpness(img).enhance(sharpen)
    if abs(contrast - 1.0) > 0.01:
        img = ImageEnhance.Contrast(img).enhance(contrast)
    if abs(color - 1.0) > 0.01:
        img = ImageEnhance.Color(img).enhance(color)
    if abs(brightness - 1.0) > 0.01:
        img = ImageEnhance.Brightness(img).enhance(brightness)

    # Upscale with high-quality Lanczos
    if upscale > 1:
        new_w = img.width * upscale
        new_h = img.height * upscale
        img = img.resize((new_w, new_h), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format='PNG', optimize=True)
    buf.seek(0)
    return buf.getvalue(), orig_size, img.size
