(function(){
var d=document;
var css=d.createElement('style');
css.textContent='#ai-widget{position:fixed;bottom:24px;right:24px;z-index:9999;font-family:Inter,sans-serif}#ai-pill{width:56px;height:56px;border-radius:50%;background:#7C3AED;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 24px rgba(124,58,237,0.4);transition:all .3s;overflow:hidden;padding:0;position:relative}#ai-pill img{width:32px;height:32px}#ai-pill:hover{transform:scale(1.08);box-shadow:0 6px 32px rgba(124,58,237,0.6)}.ai-tooltip{position:absolute;right:68px;bottom:14px;background:rgba(124,58,237,0.9);color:#fff;padding:8px 16px;border-radius:20px;font-size:13px;white-space:nowrap;opacity:0;transform:translateX(10px);transition:all .3s;pointer-events:none}.ai-tooltip.show{opacity:1;transform:translateX(0)}#ai-chat{display:none;position:absolute;bottom:68px;right:0;width:340px;height:480px;background:#111;border-radius:20px;border:1px solid rgba(255,255,255,0.1);flex-direction:column;overflow:hidden;box-shadow:0 8px 48px rgba(0,0,0,0.6)}#ai-chat.open{display:flex}#ai-header{padding:14px 18px;background:rgba(124,58,237,0.15);border-bottom:1px solid rgba(124,58,237,0.2);display:flex;justify-content:space-between;align-items:center}#ai-header span{font-weight:600;font-size:14px;color:#A78BFA}#ai-close{background:none;border:none;color:rgba(255,255,255,0.4);cursor:pointer;font-size:18px}#ai-messages{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:10px}.ai-msg{padding:10px 14px;border-radius:14px;font-size:13px;line-height:1.5;max-width:85%;word-wrap:break-word}.ai-user{align-self:flex-end;background:rgba(124,58,237,0.3);color:#F0EEF8}.ai-bot{align-self:flex-start;background:rgba(255,255,255,0.06);color:rgba(240,238,248,0.8)}#ai-input-wrap{padding:12px;border-top:1px solid rgba(255,255,255,0.06);display:flex;gap:8px}#ai-input{flex:1;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:10px 14px;color:#fff;font-size:13px;outline:none}#ai-input::placeholder{color:rgba(255,255,255,0.25)}#ai-send{background:#7C3AED;border:none;border-radius:10px;padding:10px 16px;color:#fff;cursor:pointer;font-size:13px;font-weight:600}.ai-typing{color:rgba(255,255,255,0.3);font-size:12px;padding:8px 14px}@media(max-width:400px){#ai-chat{width:290px;height:420px}}';
d.head.appendChild(css);

var w=d.createElement('div');w.id='ai-widget';
w.innerHTML='<div class="ai-tooltip" id="ai-tip">Спросите ИИ</div><button id="ai-pill"><img src="/static/ai.webp" alt="AI"></button><div id="ai-chat"><div id="ai-header"><span>Коди</span><button id="ai-close">×</button></div><div id="ai-messages"><div class="ai-msg ai-bot">Привет! Я Коди. Спрашивай о ценах, сроках, услугах Vexio.</div></div><div id="ai-input-wrap"><input id="ai-input" placeholder="Задай вопрос..."><button id="ai-send">→</button></div></div>';
d.body.appendChild(w);

var P=function(id){return d.getElementById(id)};
var pill=P('ai-pill'),chat=P('ai-chat'),close=P('ai-close'),input=P('ai-input'),send=P('ai-send'),msgs=P('ai-messages'),tip=P('ai-tip'),open=false;

function tipShow(){tip.classList.add('show');setTimeout(function(){tip.classList.remove('show')},2000)}
tipShow();setInterval(tipShow,15000);
pill.onclick=function(){open=!open;chat.className=open?'open':'';tip.classList.remove('show')};
close.onclick=function(){open=false;chat.className=''};
function add(t,c){var el=d.createElement('div');el.className='ai-msg '+c;el.textContent=t;msgs.appendChild(el);msgs.scrollTop=msgs.scrollHeight}
function wait(s){if(s){var el=d.createElement('div');el.className='ai-typing';el.id='t1';el.textContent='...';msgs.appendChild(el)}else{var x=P('t1');if(x)x.remove()}}

var rules=window.__AI_RULES__||[
{k:"цен,стои,сколько,прайс,бюджет,стоит,стоят,расценк,тариф",a:"Лендинг от 15 000 руб (3-7 дней). Интернет-магазин от 50 000 руб (14-30 дней). Корпоративный сайт от 80 000 руб. Telegram-бот от 20 000 руб. Точная цена после брифинга."},
{k:"срок,долго,дней,быстр,скоро,дедлайн,время,тайминг,как быстро,когда будет готов",a:"Лендинг 3-7 дней. Магазин 14-30 дней. Корпоративный от 21 дня. Буст: готовый сайт за 5 дней. Сроки фиксируем в договоре."},
{k:"сайт,веб,лендинг,магазин,портал,сделать,разработать,сделаете,создать",a:"Создаём сайты под ключ: лендинги, магазины, порталы, CRM. Полный цикл от дизайна до поддержки. Современный дизайн, адаптив под телефоны."},
{k:"бот,телеграм,telegram,чат,боты,автоматизация",a:"Telegram-боты с CRM (amoCRM, Битрикс24), онлайн-оплатой, AI-функциями. От простых информационных до комплексных решений."},
{k:"кейс,портфол,пример,работ,проект,портфолио,клиенты,наши работы",a:"6 проектов: MaxxMoto, Sotnur Glamping, Englify, Python Forge, СЦ Дружба, Выживальщик Опенспейса. Посмотри в разделе Работы на сайте."},
{k:"услуг,делаете,можете,функции,направления,чем занимаетесь,спектр",a:"Разработка сайтов, Telegram-ботов, CRM-систем, админ-панелей. Дизайн в Figma, вёрстка, бэкенд, SEO, поддержка 24/7."},
{k:"контакт,связь,написать,телефон,почта,обратиться,позвонить,связаться,как найти",a:"Telegram @vexiostudiocahnnel или заявка через форму на сайте. Отвечаем в течение 24 часов. Работаем по будням."},
{k:"технолог,стек,язык,инструмент,платформа,на чём,чем пишешь",a:"React, TypeScript, Python (Flask, FastAPI), Node.js, PostgreSQL, MongoDB, Redis, Docker. Современный и надёжный стек."},
{k:"гарант,поддерж,после,сопровожд,обслуживание,а если сломается,поломка",a:"Гарантия 30 дней на исправление багов. Помесячная техподдержка с SLA. Работаем по договору — вы защищены."},
{k:"оплат,рассроч,предоплат,этап,схема,как платить,способ",a:"Поэтапно: 30% старт, 30% после дизайна, 40% после сдачи. Договор. Карта и расчётный счёт."},
{k:"сео,поиск,яндекс,google,продвиж,оптимизаци,продвижение,раскрутк",a:"Базовая SEO на всех сайтах: Schema.org, Open Graph, sitemap, скорость. Расширенное SEO и контекстная реклама отдельно."},
{k:"дизайн,ui,ux,figma,фигма,прототип,макет,красивый,внешний вид",a:"Дизайн в Figma. Индивидуально, не шаблоны. Прототипирование, адаптив, анимации. Показываем макеты на каждом этапе."},
{k:"привет,здрав,хай,hello,hi,ку,прив,добрый,доброе,здаров,салют,день,вечер,утро",a:"Привет! Я Коди — AI-помощник Vexio Studio. Могу рассказать о ценах, сроках, кейсах, технологиях, дизайне, оплате. Что интересует?"},
{k:"спасиб,благодар,отличн,супер,круто,класс,помог,респект,красав,огонь,топ,красава",a:"Рады помочь! Оставьте заявку на сайте или пишите в Telegram @vexiostudiocahnnel. Будем на связи!"},
{k:"кто ты,представься,что умеешь,помощь,help,возможности,что можешь,расскажи о себе",a:"Я Коди — AI-ассистент Vexio Studio. Могу рассказать о: ценах, сроках, услугах, кейсах, технологиях, дизайне, оплате, гарантиях и SEO. Просто спроси!"},
{k:"работа,нанять,ваканси,карьер,сотрудничеств,трудоустройств",a:"Вакансии на странице https://vexiostudio.ru/hr/ — для сотрудничества пишите в Telegram @vexiostudiocahnnel."},
{k:"новости,news,блог,статьи,события,что нового",a:"IT-новости на https://vexiostudio.ru/news/ — технологии, стартапы, разработка. Каждый день."},
{k:"бизнес,business,развитие,аналитика,реклама,продвижение бизнеса",a:"Vexio Business — полное сопровождение: сайт, реклама, соцсети, аналитика. https://vexiostudio.ru/business/"},
{k:"разработчик,dev,партнёр,партнерство,70/30,семьдесят,процент разработчику",a:"Партнёрство для разработчиков: 70% с проекта — тебе. https://vexiostudio.ru/dev/"},
];

function match(q){var l=q.toLowerCase().replace(/[?!.,]/g,'');var found=[];for(var i=0;i<rules.length;i++){var r=rules[i];var ks=r.k.split(',');for(var j=0;j<ks.length;j++){if(l.indexOf(ks[j])>=0){found.push(r.a);break}}}return found.length?found.join('\n\n'):null}

async function ask(q){var r=match(q);if(r){add(r,'ai-bot');return}try{var res=await fetch('/api/ai-chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({q:q})});if(res.ok){var data=await res.json();if(data.reply){add(data.reply,'ai-bot');return}}}catch(e){}add('Спросите о ценах, сроках, услугах или кейсах Vexio. Что интересует?','ai-bot')}
send.onclick=function(){var q=input.value.trim();if(!q)return;add(q,'ai-user');input.value='';wait(true);ask(q).finally(function(){wait(false)})};
input.onkeydown=function(e){if(e.key==='Enter')send.click()};
})();
