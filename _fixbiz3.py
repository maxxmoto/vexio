h = open('static/biz/index.html', 'r', encoding='utf-8').read()

# 1. Replace manager name references
h = h.replace('Персональный менеджер', 'Степан')
h = h.replace('персональный менеджер', 'Степан')
# Also any "менеджер" in general context
if 'Степан, персональный' not in h:
    pass  # already done

# 2. Add favicon
h = h.replace('<head>', '<head>\n  <link rel="icon" href="/static/ai.webp" type="image/webp">')

# 3. Change 2021 to 2025
h = h.replace('2021', '2025')

# 4. Add Beta badge to "Ведение соцсетей" section
old_soc = 'Ведение соцсетей'
new_soc = 'Ведение соцсетей<span style="position:absolute;top:-8px;right:-8px;background:#7C3AED;color:#fff;font-size:10px;font-weight:700;padding:2px 8px;border-radius:6px;text-transform:uppercase;letter-spacing:.05em">Beta</span>'
h = h.replace(old_soc, new_soc)

# 5. Change "созвона" to "сообщения"
h = h.replace('созвона', 'сообщения')
h = h.replace('Созвона', 'Сообщения')
h = h.replace('Созвон', 'Сообщение')

# 6. Add Cody widget
if 'ai-widget.js' not in h:
    h = h.replace('</body>', '<script src="/static/ai-widget.js"></script>\n</body>')

open('static/biz/index.html', 'w', encoding='utf-8').write(h)
print('All biz fixes applied')
