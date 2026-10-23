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
paths = ["", "katalog.html", "podarki-dlya-uyuta.html", "podarki-lyubitelyam-tehniki.html", "podarki-dlya-tvorchestva.html"]
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
    sections.append("<section><h2>Для "+escape(pt)+"</h2><div class='grid'>"+"".join("<article><a href='./"+slug+"'>"+escape(title)+"</a></article>" for slug,title in sub)+"</div></section>")
catalog=page("Каталог подарков по получателю, поводу и бюджету | Подарочный переполох","Каталог идей подарков с навигацией по получателю, поводу и бюджету.","<h1>Каталог идей подарков</h1><p>Подберите получателя, повод и бюджет. Страницы предлагают критерии выбора, а не выдуманные товары и цены.</p>"+"".join(sections),BASE+"katalog.html")
(ROOT/"katalog.html").write_text(catalog,encoding="utf-8")
(ROOT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{BASE}{p}</loc></url>\n' for p in paths)+'</urlset>\n',encoding="utf-8")
(ROOT/"robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: "+BASE+"sitemap.xml\n",encoding="utf-8")
print(f"Generated {len(links)} gift pages and catalogue, sitemap, robots.txt")
