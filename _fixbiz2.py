h = open('static/biz/index.html', 'r', encoding='utf-8').read()

# 1. Remove the eyebrow/pill
old = '<div class="eyebrow"><span class="dot"></span> Vexio Business · сопровождение 360°</div>'
h = h.replace(old, '')
print('1. Eyebrow removed')

# 2. Change "Созвон на 40 минут" to "Короткий бриф на сайте"
old2 = '<h4>Созвон на 40 минут</h4>'
new2 = '<h4>Короткий бриф на сайте</h4>'
h = h.replace(old2, new2)
print('2. Step title changed')

# 3. Find footer social links and update
# The footer links use <a href="#"> with text like "Telegram", "VK", "YouTube"
old_footer = h[h.find('<footer'):h.find('</footer>')+9]

# Replace social links
h = h.replace('<a href="#">Telegram</a>', '<a href="https://t.me/vexiostudiocahnnel" target="_blank"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style="vertical-align:middle;margin-right:6px"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.14.18-.357.295-.6.295-.002 0-.003 0-.005 0l.213-3.054 5.56-5.022c.24-.213-.054-.334-.373-.121l-6.87 4.326-2.96-.924c-.64-.203-.658-.64.135-.954l11.566-4.458c.538-.196 1.006.128.832.94z"/></svg>Telegram</a>')
h = h.replace('<a href="#">VK</a>', '<a href="https://t.me/vexiostudiocahnnel" target="_blank"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style="vertical-align:middle;margin-right:6px"><path d="M15.684 0H8.316C3.724 0 0 3.724 0 8.316v7.368C0 20.276 3.724 24 8.316 24h7.368C20.276 24 24 20.276 24 15.684V8.316C24 3.724 20.276 0 15.684 0zm3.692 16.98h-2.014c-.398 0-.52-.316-1.234-1.04-.624-.604-1.202-1.022-1.402-.802-.244.27-.09.978-.09.978s.004.18-.09.28c-.1.1-.3.128-.498.128-2.56 0-5.48-1.886-6.816-4.814-.136-.298-.172-.54-.172-.54s-.01-.14.082-.204c.102-.07.33-.072.33-.072h2.012c.308 0 .422.144.53.34.59 1.084 1.1 2.078 1.91 2.632.158.108.3.05.406-.112.14-.224.104-1.632.104-1.632s.01-.41-.13-.596c-.112-.148-.322-.192-.414-.254-.066-.044-.04-.16.088-.244.218-.148.608-.16 1.068-.152.588.008.764.058 1.006.16.332.134.254.56.254.56s-.046 1.59.358 1.832c.312.19.1.044 1.75-1.862 1.22-1.418 1.1-1.038 1.1-1.038.182-.35.502-.504.502-.504h2.148s.518-.058.602.172c.082.228-.19.758-.882 1.634-1.164 1.472-1.296 1.338-.024 2.194 1.46.984 2.4 2.44 2.4 2.44s.068.166-.04.28c-.1.1-.34.088-.34.088z"/></svg>VK</a>')
h = h.replace('<a href="#">YouTube</a>', '<a href="https://t.me/vexiostudiocahnnel" target="_blank"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style="vertical-align:middle;margin-right:6px"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>YouTube</a>')
print('3. Footer icons updated')

# 4. Add form submit to admin
# The page has a "Оставить заявку" button. Let me add an onclick handler to submit to API
# Actually, let me add the same help-apply API call pattern
# The form is at #contact section - need to find it
contact_form = h.find('Оставить заявку')
if contact_form > 0:
    print('4. Form section found at', contact_form)
else:
    print('4. Form section NOT found')

# 5. Add Cody widget for /business page
widget_line = '<script src="/static/ai-widget.js"></script>'
h = h.replace('</body>', widget_line + '\n</body>')

open('static/biz/index.html', 'w', encoding='utf-8').write(h)
print('Done')
