"""Free AI features: HF Inference API (chat) + local model (caption) + pollinations (image gen)"""
import requests
import time

# Try to load HF token, fallback gracefully
HF_TOKEN = None
HF_CHAT_URL = 'https://router.huggingface.co/v1/chat/completions'
HF_HEADERS = {}
try:
    from config import HF_TOKEN
    HF_HEADERS = {'Authorization': f'Bearer {HF_TOKEN}'}
except Exception:
    pass

CHAT_MODELS = {
    'Qwen/Qwen2.5-7B-Instruct': 32000,
    'meta-llama/Llama-3.1-8B-Instruct': 32000,
}
DEFAULT_CHAT_MODEL = 'Qwen/Qwen2.5-7B-Instruct'


def generate_text(prompt, system=None):
    """Text generation via HF, with pollinations.ai fallback"""
    if system is None:
        system = 'Ты — полезный AI-ассистент Vexio AI. Отвечай на русском языке. Будь кратким и по делу. Для математики используй $...$ для формул в тексте и $$...$$ для формул на отдельной строке.'

    # Try HF first
    try:
        messages = [
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': prompt}
        ]
        payload = {
            'model': DEFAULT_CHAT_MODEL,
            'messages': messages,
            'max_tokens': 500,
            'temperature': 0.7
        }
        resp = requests.post(HF_CHAT_URL, headers=HF_HEADERS, json=payload, timeout=15)
        if resp.status_code == 200:
            return resp.json()['choices'][0]['message']['content'].strip()
    except Exception:
        pass

    # Fallback to pollinations.ai
    from urllib.parse import quote
    full = (system + '\n\n' + prompt)[:2000]
    for attempt in range(2):
        try:
            r = requests.get('https://text.pollinations.ai/' + quote(full), timeout=120,
                           headers={'User-Agent': 'Mozilla/5.0'})
            if r.status_code == 200:
                return r.text.strip()
        except Exception:
            pass
        time.sleep(8)

    raise Exception('Все AI-сервисы недоступны. Попробуйте позже.')


def caption_image(image_bytes):
    """Describe image using the local MobileNetV2 raw ImageNet predictions"""
    from model import predict_raw
    result = predict_raw(image_bytes)
    return result


def generate_image(prompt, width=512, height=512):
    """Free image generation via pollinations.ai"""
    from urllib.parse import quote
    url = f'https://image.pollinations.ai/prompt/{quote(prompt)}?width={width}&height={height}&nologo=true'
    resp = requests.get(url, timeout=120, headers={'User-Agent': 'Mozilla/5.0'})
    if resp.status_code != 200:
        raise Exception(f'API error {resp.status_code}')
    return resp.content
