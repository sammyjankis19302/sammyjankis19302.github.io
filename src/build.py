"""Build index.html, 404.html, sitemap.xml and robots.txt from src/content.py.

Run from the repository root:  python3 src/build.py
Needs nothing beyond the Python standard library.
"""
import hashlib
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import content as C  # noqa: E402

GITHUB_ICON = ('<svg class="icon" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path fill="currentColor" '
               'd="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>')

THEME_ICON = ('<svg class="icon moon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" '
              'd="M21 14.6A8.6 8.6 0 0 1 9.4 3a.6.6 0 0 0-.8-.7A9.8 9.8 0 1 0 21.7 15.4a.6.6 0 0 0-.7-.8z"/></svg>'
              '<svg class="icon sun" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" '
              'stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 1.8v2.6M12 19.6v2.6M1.8 12h2.6M19.6 12h2.6'
              'M4.8 4.8l1.8 1.8M17.4 17.4l1.8 1.8M4.8 19.2l1.8-1.8M17.4 6.6l1.8-1.8"/></g></svg>')


def webp_size(path):
    """Width and height of a WebP file, read from its header."""
    data = path.read_bytes()[:40]
    chunk = data[12:16]
    if chunk == b"VP8 ":
        w, h = struct.unpack("<HH", data[26:30])
        return w & 0x3FFF, h & 0x3FFF
    if chunk == b"VP8L":
        b = data[21:25]
        w = 1 + (((b[1] & 0x3F) << 8) | b[0])
        h = 1 + (((b[3] & 0x0F) << 10) | (b[2] << 2) | ((b[1] & 0xC0) >> 6))
        return w, h
    if chunk == b"VP8X":
        w = 1 + int.from_bytes(data[24:27], "little")
        h = 1 + int.from_bytes(data[27:30], "little")
        return w, h
    raise ValueError(f"not a WebP file: {path}")


def stamp(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()[:10]


class Figures:
    """Numbers the figures in the order they appear on the page."""

    def __init__(self):
        self.n = 0

    def next(self):
        self.n += 1
        return self.n


FIG = Figures()


def img(key, alt, cls="", eager=False):
    w, h = webp_size(ROOT / f"assets/img/{key}.webp")
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="assets/img/{key}.webp" width="{w}" height="{h}" alt="{alt}" {loading} decoding="async">'


def figure(key, alt, caption, kind="plot", numbered=True, fit=None):
    no = f'<span class="fig-no">Fig. {FIG.next()}</span> ' if numbered else ""
    cls = f"fig fig--{kind}" + (f" fit-{fit}" if fit else "")
    return (f'<figure class="{cls}"><a class="fig-frame" href="assets/img/{key}.webp">{img(key, alt)}</a>'
            f"<figcaption>{no}{caption}</figcaption></figure>")


def repo_link(name):
    url = f"{C.GITHUB}/{name}"
    return (f'<p class="repo">Code and write-up: <a href="{url}">{GITHUB_ICON}'
            f'<span>sammyjankis19302/{name}</span></a></p>')


def when_span(w):
    return f'<span class="when">{w}</span>' if w else ""


def paras(items, cls=""):
    c = f' class="{cls}"' if cls else ""
    return "".join(f"<p{c}>{p}</p>" for p in items)


def head(title, description, canonical, extra=""):
    css = f"assets/site.css?v={stamp('assets/site.css')}"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="author" content="{C.NAME}">
<link rel="canonical" href="{canonical}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#F5F7F9" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0E2233" media="(prefers-color-scheme: dark)">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" href="assets/fonts/b612-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/source-serif-4-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{css}">
<script>try{{var t=localStorage.getItem('theme');if(t==='dark'||t==='light')document.documentElement.dataset.theme=t}}catch(e){{}}</script>
{extra}</head>"""


def header(home=False):
    nav = "".join(f'<li><a href="{"" if home else "./"}#{i}">{label}</a></li>' for i, label in C.NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap top-inner">
    <a class="top-name" href="./">{C.NAME}</a>
    <nav class="top-nav" aria-label="Sections"><ul>{nav}</ul></nav>
    <button class="theme" type="button" aria-label="Switch to dark theme">{THEME_ICON}</button>
  </div>
</header>"""


def build_index():
    js = f"assets/site.js?v={stamp('assets/site.js')}"
    person = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": C.NAME,
        "givenName": "Uday Kiran",
        "familyName": "Akula",
        "alternateName": ["Uday Kiran Akula", "Uday Kiran"],
        "url": C.BASE_URL,
        "image": C.BASE_URL + "assets/img/portrait.jpg",
        "email": "mailto:" + C.EMAIL,
        "description": C.DESCRIPTION,
        "jobTitle": "Aerospace engineering student",
        "affiliation": {
            "@type": "CollegeOrUniversity",
            "name": "RV College of Engineering",
            "alternateName": "RVCE",
            "address": {"@type": "PostalAddress", "addressLocality": "Bengaluru", "addressCountry": "IN"},
        },
        "knowsAbout": ["Aerospace engineering", "Computational fluid dynamics", "Numerical methods",
                       "Hypersonic aerothermodynamics", "Gas dynamics", "Finite-difference methods"],
        "sameAs": [C.GITHUB, C.LINKEDIN],
    }
    social = f"""<meta property="og:type" content="profile">
<meta property="og:site_name" content="{C.NAME}">
<meta property="og:title" content="{C.NAME}">
<meta property="og:description" content="Aerospace engineering at RV College of Engineering, Bengaluru: computational fluid dynamics, numerical methods, and projects published in full.">
<meta property="og:url" content="{C.BASE_URL}">
<meta property="og:image" content="{C.BASE_URL}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Akula Uday Kiran, aerospace engineering, RV College of Engineering, beside streamlines around an aerofoil">
<meta property="profile:first_name" content="Uday Kiran">
<meta property="profile:last_name" content="Akula">
<meta name="twitter:card" content="summary_large_image">
<link rel="me" href="{C.GITHUB}">
<link rel="me" href="{C.LINKEDIN}">
<script type="application/ld+json">{json.dumps(person, ensure_ascii=False)}</script>
"""
    out = [head(C.TITLE, C.DESCRIPTION, C.BASE_URL, social), "<body>", header(home=True), '<main id="main">']

    # ---- hero
    spec = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in C.SPEC)
    fig_no = FIG.next()
    out.append(f"""
<section class="hero" aria-labelledby="name">
  <div class="wrap hero-grid">
    <div class="hero-text">
      <h1 id="name">Akula <span class="nowrap">Uday Kiran</span></h1>
      <p class="lede">{C.LEDE}</p>
      <ul class="hero-links">
        <li><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></li>
        <li><a href="{C.LINKEDIN}">LinkedIn</a></li>
        <li><a href="{C.GITHUB}">GitHub</a></li>
        <li><a href="{C.CV}">CV (PDF)</a></li>
      </ul>
      <dl class="spec">{spec}</dl>
    </div>
    <figure class="fig flowfig">
      <div class="flow-frame">
        <canvas id="flow" role="img" aria-label="Tracers flowing past an aerofoil, coloured by their speed"></canvas>
        <noscript><img src="assets/img/flow-static.webp" alt="Streamlines around an aerofoil, coloured by speed"></noscript>
      </div>
      <div class="flow-controls">
        <label for="aoa">Angle of attack</label>
        <input type="range" id="aoa" min="-4" max="14" step="0.5" value="6">
        <output id="aoa-out" for="aoa">6.0°</output>
        <span class="cl">Lift coefficient <output id="cl-out" aria-live="off">1.14</output></span>
      </div>
      <figcaption><span class="fig-no">Fig. {fig_no}</span> {C.FLOW_CAPTION}</figcaption>
    </figure>
  </div>
</section>""")

    # ---- experience
    entries = []
    for e in C.EXPERIENCE:
        people = f'<p class="people">{e["people"]}</p>' if e["people"] else ""
        results = ("<ul class=\"results\">" + "".join(f"<li>{r}</li>" for r in e["results"]) + "</ul>") if e["results"] else ""
        repo = repo_link(e["repo"]) if e.get("repo") else ""
        if "figure" in e:
            vis = figure(*e["figure"], kind="plot")
        else:
            vis = figure(*e["photo"], kind="photo", numbered=False)
        entries.append(f"""
<article class="entry">
  <h3 class="entry-title">{e["title"]}</h3>
  <div class="entry-meta"><p class="org">{e["org"]}</p><p class="role">{e["role"]}</p>{people}</div>
  <div class="entry-body">{paras(e["body"])}{results}{repo}{vis}</div>
</article>""")
    out.append(f"""
<section class="block" id="experience" aria-labelledby="h-experience">
  <div class="wrap">
    <h2 id="h-experience">Experience</h2>{"".join(entries)}
  </div>
</section>""")

    # ---- projects
    lead = []
    for p in C.PROJECTS_LEAD:
        guide = f'<p>{p["guide"]}</p>' if p["guide"] else ""
        lead.append(f"""
<article class="project lead">
  <div class="project-text">
    <h3>{p["title"]}</h3>
    <div class="meta"><p>{p["context"]}</p>{guide}</div>
    {paras(p["body"])}{repo_link(p["repo"])}
  </div>
  {figure(*p["figure"], kind="plot")}
</article>""")
    more = []
    fits = {"fig-leo": "cover", "fig-deaer": "contain", "fig-prop": "cover", "fig-ecs": "cover"}
    for p in C.PROJECTS_MORE:
        guide = f'<p>{p["guide"]}</p>' if p["guide"] else ""
        key = p["figure"][0]
        kind = "photo" if fits.get(key) == "cover" else "plot"
        more.append(f"""
<article class="project small">
  {figure(*p["figure"], kind=kind, fit=fits.get(key))}
  <h3>{p["title"]}</h3>
  <div class="meta"><p>{p["context"]}</p>{guide}</div>
  {paras(p["body"])}{repo_link(p["repo"])}
</article>""")
    out.append(f"""
<section class="block" id="projects" aria-labelledby="h-projects">
  <div class="wrap">
    <h2 id="h-projects">Projects</h2>
    <p class="intro">{C.PROJECTS_INTRO}</p>{"".join(lead)}
    <div class="more-grid">{"".join(more)}
    </div>
    <p class="others">{C.OTHER_WORK}</p>
  </div>
</section>""")

    # ---- path
    years = []
    for name, span, theme, items in C.YEARS:
        lis = "".join(f'<li>{when_span(w)}{t}</li>' for w, t in items)
        years.append(f'<li class="year"><h3>{name}</h3><p class="span">{span}</p>'
                     f'<p class="year-theme">{theme}</p><ul>{lis}</ul></li>')
    out.append(f"""
<section class="block" id="path" aria-labelledby="h-path">
  <div class="wrap">
    <h2 id="h-path">{C.PATH_TITLE}</h2>
    <div class="path-grid">
      <figure class="portrait">{img("portrait", "Portrait of Akula Uday Kiran")}</figure>
      <div class="path-text">{paras(C.PATH_TEXT)}<p class="beyond">{C.PATH_BEYOND}</p></div>
    </div>
    <ol class="years" aria-label="Year by year">{"".join(years)}</ol>
  </div>
</section>""")

    # ---- awards
    def award_list(items):
        return "".join(f'<li><span class="when">{w}</span><span class="what">{t}</span></li>' for w, t in items)
    photos = "".join(figure(k, a, c, kind="photo", numbered=False) for k, a, c in C.AWARD_PHOTOS)
    out.append(f"""
<section class="block" id="awards" aria-labelledby="h-awards">
  <div class="wrap">
    <h2 id="h-awards">Awards and certificates</h2>
    <div class="awards-grid">
      <div>
        <h3 class="awards-sub">Awards</h3>
        <ul class="awards">{award_list(C.AWARDS)}</ul>
        <h3 class="awards-sub">Competitions and certificates</h3>
        <ul class="awards">{award_list(C.COMPETITIONS)}</ul>
      </div>
      <div class="award-photos">{photos}</div>
    </div>
  </div>
</section>""")

    # ---- tools
    tools = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in C.TOOLS)
    out.append(f"""
<section class="block" id="tools" aria-labelledby="h-tools">
  <div class="wrap">
    <h2 id="h-tools">Coursework and tools</h2>
    <dl class="tools"><div><dt>Selected coursework</dt><dd>{C.COURSEWORK}<span class="note">{C.COURSEWORK_NOTE}</span></dd></div>{tools}</dl>
  </div>
</section>
</main>""")

    # ---- contact
    out.append(f"""
<footer class="contact" id="contact" aria-labelledby="h-contact">
  <div class="wrap">
    <h2 id="h-contact">Contact</h2>
    <p>{C.CONTACT_TEXT}</p>
    <p class="email"><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
    <p class="colophon">Plain HTML, CSS and JavaScript, with no trackers. Set in B612, the typeface designed for
    Airbus cockpit displays, and Source Serif&nbsp;4. Updated {C.UPDATED_TEXT}.
    <a href="{C.GITHUB}/sammyjankis19302.github.io">Source</a>.</p>
  </div>
</footer>
<script src="{js}" defer></script>
</body>
</html>
""")
    return "\n".join(out)


def build_404():
    return f"""{head("Page not found – " + C.NAME, "This page does not exist.", C.BASE_URL + "404.html",
                 '<meta name="robots" content="noindex">' + chr(10))}
<body>
{header()}
<main id="main" class="notfound">
  <div class="wrap">
    <h1>This page does not exist</h1>
    <p>The address may be mistyped, or the page may have moved. <a href="./">Go to the home page</a>
    to find {C.NAME}’s projects and contact details.</p>
  </div>
</main>
<script src="assets/site.js?v={stamp('assets/site.js')}" defer></script>
</body>
</html>
"""


def main():
    (ROOT / "index.html").write_text(build_index(), encoding="utf-8")
    (ROOT / "404.html").write_text(build_404(), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{C.BASE_URL}</loc><lastmod>{C.UPDATED}</lastmod></url>\n"
        "</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {C.BASE_URL}sitemap.xml\n", encoding="utf-8")
    print(f"built index.html ({FIG.n} numbered figures), 404.html, sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
