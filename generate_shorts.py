"""Build three short vertical videos for the site's own media directory."""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "media"
OUT.mkdir(exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SCENES = [
    [("ТЕРМОКРУЖКА ИЛИ ТЕРМОС?", "Что подарить любителю поездок?"),
     ("ТЕРМОКРУЖКА", "Для коротких поездок и прогулок"),
     ("ТЕРМОС", "Для долгого дня вне дома"),
     ("ВЫБИРАЙ ПО ЗАДАЧЕ", "Гид на сайте Подарочный переполох")],
    [("НАУШНИКИ В ПОДАРОК?", "Не выбирай только по коробке"),
     ("ПРОВЕРЬ ПОСАДКУ", "Вкладыши или накладные?"),
     ("ПРОВЕРЬ СОВМЕСТИМОСТЬ", "Телефон, подключение, зарядка"),
     ("ПОДРОБНЫЙ ГИД", "На сайте Подарочный переполох")],
    [("ПОДАРОК БЕЗ ПРОМАХА", "Три проверки перед заказом"),
     ("ИНТЕРЕСЫ", "Что человек использует каждый день?"),
     ("УДОБСТВО", "Размер, материал и совместимость"),
     ("УСЛОВИЯ", "Доставка, гарантия и возврат")]
]
def run(args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)
with tempfile.TemporaryDirectory() as td:
    temp = Path(td)
    for n, scenes in enumerate(SCENES, 1):
        parts = []
        for j, (headline, subtitle) in enumerate(scenes):
            h = temp / f"h{n}_{j}.txt"
            s = temp / f"s{n}_{j}.txt"
            h.write_text(headline, encoding="utf-8")
            s.write_text(subtitle, encoding="utf-8")
            part = temp / f"clip{n}_{j}.mp4"
            filters = (
                f"drawtext=fontfile={FONT}:textfile={h}:fontcolor=white:fontsize=28:"
                "x=(w-text_w)/2:y=330,"
                f"drawtext=fontfile={FONT}:textfile={s}:fontcolor=white:fontsize=19:"
                "x=(w-text_w)/2:y=510,"
                f"drawtext=fontfile={FONT}:text='ПОДАРОЧНЫЙ ПЕРЕПОЛОХ':"
                "fontcolor=white:fontsize=18:x=(w-text_w)/2:y=100"
            )
            run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                 "-i", "color=c=0x30213f:s=540x960:r=24:d=3",
                 "-vf", filters, "-c:v", "libx264", "-preset", "ultrafast",
                 "-pix_fmt", "yuv420p", "-an", str(part)])
            parts.append(part)
        concat = temp / f"list{n}.txt"
        concat.write_text("".join(f"file '{p}'\n" for p in parts), encoding="utf-8")
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
             "-i", str(concat), "-c", "copy", "-movflags", "+faststart",
             str(OUT / f"shorts_{n:02}.mp4")])
        print(f"Created {OUT / f'shorts_{n:02}.mp4'}")
