"""Render an offline preview that mirrors the Jekyll templates.

This does NOT replace Jekyll — GitHub Pages does the real build. It exists so
the design can be reviewed without installing Ruby, and so the front matter
shape gets validated before anything is pushed.
"""
import os, re, glob, html
import yaml, markdown

SITE = "/home/claude/site"
OUT = os.path.join(SITE, "_preview")
os.makedirs(OUT, exist_ok=True)

cfg = yaml.safe_load(open(os.path.join(SITE, "_config.yml")))


def load(path):
    raw = open(path).read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    fm = yaml.safe_load(m.group(1))
    fm["body"] = m.group(2)
    fm["slug"] = os.path.splitext(os.path.basename(path))[0]
    return fm


recipes = sorted(
    (load(p) for p in glob.glob(os.path.join(SITE, "_recipes", "*.md"))),
    key=lambda r: r["date"],
    reverse=True,
)

md = markdown.Markdown(extensions=["extra", "sane_lists"])


def spec(r, keys=(("serves", "serves"), ("time", "time"))):
    rows = "".join(
        f"<div><dt>{label}</dt><dd>{html.escape(str(r[key]))}</dd></div>"
        for key, label in keys
        if r.get(key)
    )
    return f'<dl class="spec">{rows}</dl>'


def frame(r, cls):
    if r.get("image") and os.path.exists(SITE + r["image"]):
        return f'<div class="{cls}"><img src="..{r["image"]}" alt=""></div>'
    return f'<div class="{cls}"></div>'


def shell(title, body):
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..500;1,6..72,300..500&family=Schibsted+Grotesk:wght@400;500&display=swap">
<link rel="stylesheet" href="../assets/css/main.css">
</head><body>
<header class="masthead wrap">
  <a class="masthead__name" href="index.html">{html.escape(cfg['title'])}</a>
  <nav class="masthead__nav">
    <a href="index.html">Recipes</a><a href="#">About</a><a href="#">Instagram</a>
  </nav>
</header>
<main>{body}</main>
<footer class="colophon wrap">
  <span>{html.escape(cfg['tagline'])} by {html.escape(cfg['author'])}</span>
  <span><a href="#">@{html.escape(str(cfg['instagram']))}</a></span>
</footer>
</body></html>"""


# ---- home -------------------------------------------------------------
lead, rest = recipes[0], recipes[1:]

plates = ""
for r in rest:
    plates += f"""<a class="plate" href="{r['slug']}.html">
    {frame(r, 'plate__frame')}
    <div class="plate__foot">
      <h2 class="plate__title">{html.escape(r['title'])}</h2>
      {spec(r)}
    </div></a>"""

home = f"""<p class="lede wrap">{html.escape(cfg['description'].strip())}</p>
<div class="wrap"><a class="hero" href="{lead['slug']}.html">
  {frame(lead, 'hero__frame')}
  <div class="hero__foot">
    <h1 class="hero__title">{html.escape(lead['title'])}</h1>
    {spec(lead)}
  </div></a></div>
<div class="gallery wrap">{plates}</div>"""

open(os.path.join(OUT, "index.html"), "w").write(shell(cfg["title"], home))


# ---- recipes ----------------------------------------------------------
def ingredients_html(items):
    out, open_ul = "", False
    for entry in items:
        if isinstance(entry, dict) and "group" in entry:
            if open_ul:
                out, open_ul = out + "</ul>", False
            out += f'<p class="ingredients__group">{html.escape(entry["group"])}</p><ul>'
            out += "".join(f"<li>{html.escape(str(i))}</li>" for i in entry["items"])
            out += "</ul>"
        else:
            if not open_ul:
                out, open_ul = out + "<ul>", True
            out += f"<li>{html.escape(str(entry))}</li>"
    return out + ("</ul>" if open_ul else "")


for r in recipes:
    meta = spec(r, (("serves", "serves"), ("time", "time")))
    cooked = f'<div><dt>cooked</dt><dd>{r["date"].strftime("%-d %B %Y")}</dd></div>'
    notes = (
        f'<section class="notes wrap"><h2>Notes</h2>{md.convert(r["notes"])}</section>'
        if r.get("notes")
        else ""
    )
    page = f"""<article class="recipe">
  <header class="recipe__head wrap">
    <h1 class="recipe__title">{html.escape(r['title'])}</h1>
    <p class="recipe__intro">{html.escape(r.get('intro',''))}</p>
  </header>
  <div class="wrap"><figure class="recipe__figure">{frame(r,'')[len('<div class="">'):-6] or ''}</figure></div>
  <div class="recipe__body wrap">
    <div class="ingredients">
      <h2>Ingredients</h2>
      {ingredients_html(r['ingredients'])}
      <dl class="spec spec--stack">{spec(r)[len('<dl class="spec">'):-5]}{cooked}</dl>
    </div>
    <div class="method"><h2>Method</h2>{md.reset().convert(r['body'])}</div>
  </div>
  {notes}
</article>"""
    open(os.path.join(OUT, f"{r['slug']}.html"), "w").write(shell(r["title"], page))

print(f"rendered {len(recipes) + 1} pages")
print("ingredient shapes ok:", [type(r["ingredients"][0]).__name__ for r in recipes])
