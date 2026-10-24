#!/usr/bin/env python3
"""Generate a navigable gift-idea catalogue from editorial rules, without fabricated products."""
from pathlib import Path
from html import escape
from itertools import product
from datetime import date
ROOT = Path(__file__).resolve().parent
BASE = "https://ki9177997007-rgb.github.io/podarochny-perepoloh/"
PEOPLE = [
("mame","маме","мамы","Полезный подарок, учитывающий привычки и интересы"),
("pape","папе","папы","Удобство и совместимость с уже имеющимися вещами"),
("drugu","другу","друга","Общие увлечения и уместность шутливого подарка"),
("podruge","подруге","подруги","Личные предпочтения, стиль и практичность"),
("kollege","коллеге","коллеги","Нейтральный характер и уместность в рабочих отношениях"),
("partneru","любимому человеку","любимого человека","Личные интересы и внимание к деталям"),
("podrostku","подростку","подростка","Возрастные ограничения, безопасность и актуальные интересы"),
("uchitelyu","учителю","учителя","Уместность, локальные правила и отсутствие чрезмерной стоимости")]
OCCASIONS = [
("den-rozhdeniya","на день рождения","День рождения","Подумайте о хобби человека и о том, что он давно хотел попробовать"),
("novyy-god","на Новый год","Новый год","Учитывайте сезон, срок доставки и праздничную упаковку"),
("8-marta","на 8 Марта","8 Марта","Ориентируйтесь на интересы человека, а не на гендерные стереотипы"),
("23-fevralya","на 23 Февраля","23 Февраля","Выбирайте по увлечениям, а не по формальным клише"),
("bez-povoda","без повода","Без повода","Лучше небольшая, но действительно полезная вещь"),
("godovshchina","на годовщину","Годовщина","Важны личный смысл и общие воспоминания")]
BUDGETS = [
("do-1000","до 1 000 ₽","Небольшой бюджет","Оценивайте качество материалов и доставку: итоговая стоимость может отличаться"),
("1000-3000","от 1 000 до 3 000 ₽","Средний бюджет","Сравните несколько вариантов по комплектации и гарантии"),
("3000-7000","от 3 000 до 7 000 ₽","Расширенный бюджет","Проверьте характеристики, гарантию и условия возврата"),
("ot-7000","от 7 000 ₽","Крупный бюджет","Проверяйте продавца, совместимость и официальную гарантию")]
IDEAS = [
("Термокружка","Герметичность крышки, объём, материал колбы, удобство мытья"),
("Настольная лампа","Регулировка яркости, питание, устойчивость и безопасность"),
("Настольная игра","Количество игроков, возрастные ограничения, время партии"),
("Набор для творчества","Комплектация, возраст, уровень подготовки и расходные материалы"),
("Наушники","Совместимость, посадка, автономность и гарантия"),
("Плед","Состав ткани, размер и уход"),
("Книга","Интересы читателя, язык, формат и наличие издания"),
("Органайзер","Размер, материал, удобство и назначение")]
def page(title, description, body, canonical):
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><meta name="description" content="{escape(description,quote=True)}"><link rel="canonical" href="{escape(canonical,quote=True)}"><style>body{{font:17px/1.65 system-ui;margin:0;background:#fffaf6;color:#211b36}}header,footer{{background:#211b36;color:white;padding:18px max(5%,calc((100% - 1050px)/2))}}header a,footer a{{color:white}}main{{max-width:1050px;margin:auto;padding:35px 20px 75px}}h1{{font-size:clamp(32px,5vw,52px);line-height:1.15}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:15px}}article{{background:white;border:1px solid #eae3e5;border-radius:18px;padding:20px}}article h2{{font-size:21px}}.muted{{color:#676078}}a{{color:#98375c}}.tag{{display:inline-block;background:#f3e7f1;border-radius:20px;padding:3px 12px;font-size:13px}}li{{margin:8px 0}}</style></head><body><header><a href="./">🎁 Подарочный переполох</a> · <a href="./katalog.html">Каталог</a></header><main>{body}</main><footer>Идеи для выбора, не магазин. Цены и наличие проверяйте у продавца. Партнёрские ссылки будут отмечены, если появятся.</footer></body></html>'''
paths = ["", "katalog.html", "podarki-dlya-uyuta.html", "podarki-lyubitelyam-tehniki.html", "podarki-dlya-tvorchestva.html", "kak-vybrat-podarok.html", "termokruzhka-ili-termos.html", "nakladnye-ili-vnutrikanalnye-naushniki.html", "nastolnaya-igra-ili-konstruktor.html", "provodnaya-ili-besprovodnaya-zaryadka.html"]

# Editorial product-category landing pages. No unverified brands, prices or reviews.
PRODUCTS = [
("termokruzhka","Термокружка","Для поездок, работы и прогулок","Герметичность крышки|Материал внутренней колбы|Удобство мытья","Уточните, будет ли кружка стоять в подстаканнике автомобиля.|Проверьте, можно ли мыть крышку и уплотнители отдельно.","termokruzhka-ili-termos.html"),
("termos","Термос","Для путешествий и долгих прогулок","Объём и масса|Тип пробки|Удобство наливания","Выбирайте объём под длительность поездок.|Проверьте возможность замены уплотнителей.","termokruzhka-ili-termos.html"),
("besprovodnye-naushniki","Беспроводные наушники","Для музыки и звонков","Посадка и размер|Совместимость с телефоном|Автономность с кейсом","Уточните предпочтительный форм-фактор.|Проверьте условия гарантии и возврата.","nakladnye-ili-vnutrikanalnye-naushniki.html"),
("nakladnye-naushniki","Накладные наушники","Для дома и рабочего стола","Прижим и масса|Тип подключения|Сменные амбушюры","Для длительного ношения важнее удобство, чем внешний вид.|Проверьте возможность проводного подключения.","nakladnye-ili-vnutrikanalnye-naushniki.html"),
("powerbank","Внешний аккумулятор","Для путешествий и повседневной зарядки","Ёмкость и масса|Мощность выхода|Поддерживаемые разъёмы","Сверьте требования телефона к зарядке.|Для авиаперелётов проверьте правила перевозчика.","provodnaya-ili-besprovodnaya-zaryadka.html"),
("besprovodnaya-zaryadka","Беспроводная зарядка","Для удобного рабочего места","Совместимость стандарта|Положение катушки|Блок питания в комплекте","Не каждый телефон поддерживает беспроводную зарядку.|Проверьте, нужен ли отдельный адаптер питания.","provodnaya-ili-besprovodnaya-zaryadka.html"),
("nastolnaya-lampa","Настольная лампа","Для чтения и рабочего места","Регулировка яркости|Устойчивость основания|Тип питания","Уточните размер рабочего стола.|Проверьте наличие мерцания по данным изготовителя."),
("pledy","Плед","Для домашнего уюта","Состав ткани|Размер|Условия стирки","Уточните предпочтения по материалам.|Для подарка важна простота ухода."),
("nastolnye-igry","Настольная игра","Для семейного и дружеского досуга","Число игроков|Длительность партии|Возрастные ограничения","Уточните, с кем получатель будет играть.|Проверьте язык правил и компонентов.","nastolnaya-igra-ili-konstruktor.html"),
("konstruktor","Конструктор","Для увлечённых сборкой","Возраст и сложность|Число деталей|Размер готовой модели","Выбирайте по интересующей тематике.|Проверьте, требуется ли дополнительный инструмент.","nastolnaya-igra-ili-konstruktor.html"),
("nabor-dlya-risovaniya","Набор для рисования","Для творчества и освоения хобби","Тип материалов|Комплектация|Уровень подготовки","Для новичка важнее понятная комплектация.|Проверьте совместимость бумаги и красок."),
("sketchbuk","Скетчбук","Для зарисовок и заметок","Плотность бумаги|Формат|Тип переплёта","Выбирайте бумагу под маркеры, карандаши или акварель.|Для поездок удобнее компактный формат."),
("organayzer-dlya-stola","Настольный органайзер","Для порядка на рабочем месте","Размер секций|Материал|Устойчивость","Измерьте свободное место на столе.|Учитывайте, какие предметы будут храниться."),
("ryukzak","Городской рюкзак","Для учёбы, работы и поездок","Объём и габариты|Отделение для ноутбука|Удобство лямок","Сверьте размер ноутбука с внутренним отсеком.|Проверьте материал и молнии."),
("butylka-dlya-vody","Бутылка для воды","Для спорта и прогулок","Материал|Герметичность|Удобство очистки","Проверьте, подходит ли бутылка для горячих напитков.|Выбирайте объём с учётом веса."),
("kniga","Книга в подарок","Для любителей чтения","Жанр и автор|Язык и перевод|Формат издания","Убедитесь, что книги ещё нет в библиотеке получателя.|Проверьте, предпочитает ли он бумагу или электронный формат."),
("elektronnaya-kniga","Электронная книга","Для частого чтения","Тип экрана|Поддержка форматов|Подсветка","Уточните, где человек чаще читает.|Проверьте доступность нужных форматов файлов."),
("kofemolka","Кофемолка","Для любителей кофе","Тип жерновов или ножей|Регулировка помола|Удобство чистки","Для разных способов заваривания важна регулировка помола.|Учитывайте шум и место на кухне."),
("french-press","Френч-пресс","Для приготовления напитков","Объём|Материал колбы|Разборка фильтра","Уточните количество порций.|Проверьте доступность запасных деталей."),
("multitul","Мультитул","Для бытовых мелких задач","Набор инструментов|Размер и масса|Качество фиксации","Сравните инструменты с реальными задачами.|Проверьте ограничения на перевозку."),
]
PRODUCT_LINKS = []
for item in PRODUCTS:
    slug,name,who,criteria,tips,*related = item
    filename = "tovar-"+slug+".html"
    checks = criteria.split("|")
    advice = tips.split("|")
    extra = ("<p>Также полезно: <a href='./"+related[0]+"'>сравнение вариантов</a>.</p>") if related else ""
    body = ("<p class='tag'>Гид по категории</p><h1>"+escape(name)+" в подарок</h1><p>"+escape(who)+". Разбираем, кому подходит эта категория и какие параметры проверить до заказа.</p>"
        +"<h2>На что смотреть при выборе</h2><div class='grid'>"
        +"".join("<article><h2>"+escape(c)+"</h2><p>Сравните этот параметр в карточках нескольких предложений. Не полагайтесь только на рекламное описание.</p></article>" for c in checks)
        +"</div><h2>Перед покупкой</h2><ul>"+"".join("<li>"+escape(t)+"</li>" for t in advice)+"</ul>"
        +"<h2>Где посмотреть предложения</h2><p>Ссылки на конкретные товары появятся после подключения проверенных партнёрских предложений. Пока используйте этот чек-лист для самостоятельного сравнения.</p>"
        +"<a data-partner-id='tovar-"+slug+"' hidden rel='sponsored nofollow noopener noreferrer'>Посмотреть предложение</a>"
        +extra+"<p><a href='./katalog.html'>← В каталог подарков</a></p><script defer src='./partners.js'></script>")
    (ROOT/filename).write_text(page(name+" в подарок | Подарочный переполох","Как выбрать "+name.lower()+": критерии, ограничения и практические советы без выдуманных цен и отзывов.",body,BASE+filename),encoding="utf-8")
    PRODUCT_LINKS.append((filename,name,who))
paths.extend(filename for filename,_,_ in PRODUCT_LINKS)

links=[]
for person,occasion,budget in product(PEOPLE,OCCASIONS,BUDGETS):
    ps,pt,pg,pc=person; os,ot,og,oc=occasion; bs,bt,bg,bc=budget
    slug=f"idei-{ps}-{os}-{bs}.html"
    title=f"Что подарить {pt} {ot}: идеи с бюджетом {bt}"
    desc=f"Идеи подарков {pt} {ot}, бюджет {bt}. Критерии выбора и советы без выдуманных цен и отзывов."
    chosen=IDEAS[(len(ps)+len(os)+len(bs))%len(IDEAS):]+IDEAS[:(len(ps)+len(os)+len(bs))%len(IDEAS)]
    cards="".join(f"<article><h2>{escape(name)}</h2><p>{escape(criteria)}</p><p class='muted'>Подходит только если отвечает интересам получателя.</p></article>" for name,criteria in chosen[:4])
    body=f"<p class='tag'>{escape(og)} · {escape(bg)}</p><h1>{escape(title)}</h1><p>{escape(pc)}. {escape(oc)}. {escape(bc)}.</p><h2>Что можно рассмотреть</h2><div class='grid'>{cards}</div><h2>Как выбрать</h2><ol><li>Уточните интересы и то, чем человек уже пользуется.</li><li>Сравните материалы, комплектацию и гарантию.</li><li>Проверьте актуальную стоимость с доставкой и условия возврата.</li></ol><p class='muted'>Это идеи категорий товаров, а не рейтинг конкретных моделей. Мы не заявляем о личном тестировании.</p><p><a href='./katalog.html'>← Все подборки</a></p>"
    (ROOT/slug).write_text(page(title+" | Подарочный переполох",desc,body,BASE+slug),encoding="utf-8")
    links.append((slug,title))
paths += [slug for slug,_ in links]
sections=[]
for ps,pt,_,_ in PEOPLE:
    sub=[(slug,title) for slug,title in links if slug.startswith("idei-"+ps+"-")]
    sections.append("<section data-group><h2>Для "+escape(pt)+"</h2><div class='grid'>"+"".join("<article data-gift data-person='"+ps+"' data-occasion='"+next(os for os,_,_,_ in OCCASIONS if '-'+os+'-' in slug)+"' data-budget='"+next(bs for bs,_,_,_ in BUDGETS if slug.endswith('-'+bs+'.html'))+"'><a href='./"+slug+"'>"+escape(title)+"</a></article>" for slug,title in sub)+"</div></section>")
filters = """<div class="filters"><label>Кому <select id="person"><option value="">Всем</option>""" + "".join(f'<option value="{ps}">{escape(pt)}</option>' for ps,pt,_,_ in PEOPLE) + """</select></label><label>Повод <select id="occasion"><option value="">Любой</option>""" + "".join(f'<option value="{os}">{escape(og)}</option>' for os,_,og,_ in OCCASIONS) + """</select></label><label>Бюджет <select id="budget"><option value="">Любой</option>""" + "".join(f'<option value="{bs}">{escape(bt)}</option>' for bs,bt,_,_ in BUDGETS) + """</select></label></div><p id="count" aria-live="polite"></p>"""
filter_script = """<style>.filters{display:flex;flex-wrap:wrap;gap:12px;margin:22px 0}.filters label{display:grid;gap:4px;font-weight:700}.filters select{padding:11px;border:1px solid #ded3df;border-radius:12px;background:white;font:inherit;max-width:270px}.grid article[hidden],section[hidden]{display:none}</style><script>(function(){const p=document.getElementById('person'),o=document.getElementById('occasion'),b=document.getElementById('budget'),cards=[...document.querySelectorAll('[data-gift]')];function apply(){let n=0;cards.forEach(c=>{const ok=(!p.value||c.dataset.person===p.value)&&(!o.value||c.dataset.occasion===o.value)&&(!b.value||c.dataset.budget===b.value);c.hidden=!ok;if(ok)n++});document.querySelectorAll('section[data-group]').forEach(s=>s.hidden=![...s.querySelectorAll('[data-gift]')].some(c=>!c.hidden));document.getElementById('count').textContent='Найдено подборок: '+n} [p,o,b].forEach(x=>x.addEventListener('change',apply));apply()})();</script>"""
product_section = "<section><h2>Гиды по товарам</h2><p>Отдельные страницы с критериями выбора. Партнёрские предложения добавим после подключения API.</p><div class='grid'>"+"".join("<article><h2><a href='./"+f+"'>"+escape(n)+"</a></h2><p>"+escape(w)+"</p></article>" for f,n,w in PRODUCT_LINKS)+"</div></section>"
catalog=page("Каталог подарков по получателю, поводу и бюджету | Подарочный переполох","Каталог идей подарков с навигацией по получателю, поводу и бюджету.","<h1>Каталог идей подарков</h1><p>Подберите получателя, повод и бюджет. Страницы предлагают критерии выбора, а не выдуманные товары и цены.</p>"+product_section+filters+"".join(sections)+filter_script,BASE+"katalog.html")
(ROOT/"katalog.html").write_text(catalog,encoding="utf-8")
(ROOT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{BASE}{p}</loc></url>\n' for p in paths)+'</urlset>\n',encoding="utf-8")
(ROOT/"robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: "+BASE+"sitemap.xml\n",encoding="utf-8")
print(f"Generated {len(links)} gift pages, {len(PRODUCT_LINKS)} product guides, catalogue, sitemap, robots.txt")
