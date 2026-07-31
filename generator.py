import requests, random, time, re

API_URL = 'https://image.pollinations.ai/prompt'

# All terms use root-word matching (substring check in lowercase)
BLOCKED = [
    # === ДЕТИ / CHILDREN ===
    'ребен','ребён','дети','детск','младен','малыш','несовершеннолет','малолет',
    'школьник','школьниц','подрост','teen','child','kid','minor','underage',
    'baby','infant','toddler','loli','shota','ясли','детсад',

    # === ПОРНО / PORN ===
    'порн','эротик','интим','обнаж','раздет','голый','голая','нагот','ню',
    'nsfw','xxx','adult','explicit','nude','nudit','naked','undress','topless',
    'fetish','bdsm','hentai','линжери','бель','бикин','стринг','трус','лифчик',
    'бюстгальтер','нижн','соблазнит','откровен','сексуализ',

    # === СЕКС / SEX ===
    'секс','полов','оральн','анальн','группов','орги','инцест','зоофил',
    'некрофил','совокуплен','койтус','пенетрац','фаллос','вагин','влагалищ',
    'член','пенис','клитор','груд','соск','ягодиц','анус','попа','задниц',
    'сперм','оргазм','возбужден','эрекц','конч','презерватив','лубрикант',

    # === МАТ / OBSCENITY ===
    'хуй','пизд','ебат','ебал','ебан','ебёт','ебл','ёбан','уеб','заеб','выеб',
    'бля','бляд','сука','пидор','пидар','гандон','мудак','залуп','хер','хрен',
    'елда','манда','курв','шлюх','проститут','дроч','ахуе','охуе','наху',
    'поху','ебуч','срал','срать','жоп','говн','говё','членосос','минет',
    'отсос','куни','глот','раком','трахан','перепихон','врот',

    # === НАСИЛИЕ / VIOLENCE ===
    'убий','убийств','убит','умерщв','смерт','мёртв','мертв','труп',
    'покойник','похорон','кладбищ','гроб','казн','расстрел','обезглав',
    'расчлен','пытк','истязан','насили','жесток','кров','кровав',
    'gore','violen','murder','kill','execut','torture','corpse','dead','death',
    'wound','injur','bleed','massacr','slaughter','behead','dismember',

    # === СУИЦИД / SUICIDE ===
    'самоубий','суицид','суицидальн','самоповрежд','селфхарм','selfharm',
    'suicide','вешат','повес','петл','ядо','отрав','передоз',

    # === ТЕРРОРИЗМ / TERRORISM ===
    'террор','экстремизм','радикал','игил','isis','алькаид','alqaeda',
    'неонаци','нацизм','свастик','whitepower','kkk','куклус','джихад',
    'талиб','боевик','шахид',

    # === ПОЛИТИКА / POLITICS ===
    'политик','президент','премьер','парламент','депутат','выбор','митинг',
    'протест','революц','переворот','пропаганд','агитац','парти','путин',
    'зеленск','трамп','байден','лукашенк','лозунг','транспарант','флаг',
    'герб','гимн','голосован',

    # === РАСИЗМ / RACISM ===
    'расизм','расов','дискриминац','ксенофоб','антисемит','геноцид',
    'hatеspeech','racism','нацист','фашист','черножоп','черномаз',
    'жид','хач','чурк','узкоглаз',

    # === НАРКОТИКИ / DRUGS ===
    'наркот','героин','кокаин','амфетамин','метамфетамин','мефедрон',
    'экстази','лсд','марихуан','каннабис','опиум','морфин','метадон',
    'drug','cocaine','heroin','meth','mdma','lsd','weed','cannabis',

    # === ОРУЖИЕ / WEAPONS ===
    'бомб','взрывчат','оруж','автомат','винтовк','пистолет','пулемёт',
    'пулемет','гранат','мин','ракет','взрыв','артиллер','танк','снаряд',
    'grenade','gun','rifle','pistol','weapon','explosiv','bomb',

    # === ПРЕСТУПЛЕНИЯ / CRIME ===
    'мошеннич','подделк','фальшив','кража','ограблен','взлом','хакерств',
    'вымогательств','шантаж','контрабанд','торговл','похищен','заложник',
    'kidnapping','humantraffick','counterfeit','moneylaundering',

    # === ОПАСНЫЕ / HAZARDOUS ===
    'яд','токсин','цианид','кислот','опасное','отравляющ','радиоактив',

    # === КУЛЬТЫ / CULTS ===
    'сатанизм','оккульт','жертвоприношен','секта','культ',

    # === АЛКОГОЛЬ / КУРЕНИЕ ===
    'алкогол','водк','коньяк','виски','пив','вин','сигарет','курени',
    'табак','кальян','вейп','похмел','запой',

    # === АЗАРТ / GAMBLING ===
    'казин','гемблинг','gambl','игровой автомат','букмекер','тотализатор',

    # === DEEPFAKE / PRIVACY ===
    'дипфейк','deepfake','revengeporn','скрыт','voyeur','подгляд','утечк',

    # === ПРОЧЕЕ ===
    'ампутац','внутренност','вскрыт','рабств','пленник',
    'разжиган','ненавист','оскорблен',
]
# Deduplicate and lowercase
BLOCKED = list(set([b.lower() for b in BLOCKED]))


def moderate(prompt):
    low = prompt.lower().replace(' ', '').replace('-', '').replace('_', '')
    for word in BLOCKED:
        if word in low:
            return True
    return False


def generate_image(prompt, width=512, height=512):
    if moderate(prompt):
        raise ValueError('BLOCKED')

    from urllib.parse import quote
    prompt = prompt.strip()[:500]

    has_cyrillic = bool(re.search(r'[а-яА-Я]', prompt))
    if has_cyrillic:
        try:
            t = requests.get(f'https://text.pollinations.ai/{quote("Translate to English, short image prompt only: " + prompt)}',
                           timeout=30, headers={'User-Agent': 'Mozilla/5.0'})
            if t.status_code == 200 and t.text.strip():
                prompt = t.text.strip()[:300]
        except Exception:
            pass

    if 'realistic' not in prompt.lower() and 'photo' not in prompt.lower() and '4k' not in prompt.lower():
        prompt += ', high quality'

    for attempt in range(3):
        seed = random.randint(1, 999999)
        url = f'{API_URL}{quote(prompt)}?width={width}&height={height}&seed={seed}&nologo=true'
        try:
            resp = requests.get(url, timeout=120, headers={'User-Agent': 'Mozilla/5.0'})
            if resp.status_code == 200 and len(resp.content) > 3000:
                return resp.content
        except Exception:
            pass
        time.sleep(5 if attempt < 2 else 0)
    raise Exception('Не удалось сгенерировать. Попробуйте другой запрос.')
