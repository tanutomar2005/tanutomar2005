"""Generate local GitHub profile assets from live GitHub API data."""
from __future__ import annotations

import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
USER = os.environ.get("GITHUB_USERNAME", "tanutomar2005")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
API = "https://api.github.com"
COLORS = {"bg": "#03050B", "panel": "#070B16", "panel2": "#0A1020", "cyan": "#00E5FF", "purple": "#8B5CF6", "pink": "#FF4ECD", "green": "#76B900", "text": "#F6F8FF", "muted": "#9BA8C7"}


def api(path: str, *, method: str = "GET", body: dict | None = None) -> dict | list:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "tanutomar2005-profile-generator"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    request = urllib.request.Request(API + path, headers=headers, method=method)
    if body is not None:
        request.data = json.dumps(body).encode()
        request.headers["Content-Type"] = "application/json"
    last_error = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                return json.load(response)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as error:
            last_error = error
            if isinstance(error, urllib.error.HTTPError) and error.code in (401, 403, 404):
                break
            time.sleep(2 ** attempt)
    raise RuntimeError(f"GitHub API request failed: {path}: {last_error}")


def svg_start(width: int, height: int, title: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">Generated for Tanu Tomar's GitHub profile.</desc>
<defs><linearGradient id="accent" x1="0" x2="1"><stop stop-color="{COLORS['cyan']}"/><stop offset=".52" stop-color="{COLORS['purple']}"/><stop offset="1" stop-color="{COLORS['pink']}"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<rect width="{width}" height="{height}" rx="18" fill="{COLORS['bg']}" stroke="#172342"/><rect x="1" y="1" width="{width-2}" height="5" rx="3" fill="url(#accent)"/></svg>'''


def text(x: int, y: int, value: str, size: int = 14, fill: str | None = None, weight: str = "400", anchor: str = "start") -> str:
    return f'<text x="{x}" y="{y}" fill="{fill or COLORS["text"]}" font-family="ui-monospace, SFMono-Regular, Consolas, monospace" font-size="{size}px" font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>'


def write(name: str, content: str) -> None:
    path = ASSETS / name
    path.write_text(content, encoding="utf-8")


def generate_clock() -> None:
    skills = [("HTML", 0, COLORS["cyan"]), ("CSS", 1, COLORS["purple"]), ("JavaScript", 2, COLORS["pink"]), ("React", 3, COLORS["cyan"]), ("Node.js", 4, COLORS["green"]), ("SQL", 5, COLORS["purple"]), ("PostgreSQL", 6, COLORS["cyan"]), ("Java", 7, COLORS["pink"]), ("C Basics", 8, COLORS["purple"]), ("DSA", 9, COLORS["cyan"]), ("Git & GitHub", 10, COLORS["green"]), ("REST APIs", 11, COLORS["pink"])]
    now = datetime.now(timezone.utc)
    hour_angle = ((now.hour % 12) + now.minute / 60 + now.second / 3600) * 30
    minute_angle = (now.minute + now.second / 60) * 6
    second_angle = (now.second + now.microsecond / 1_000_000) * 6
    marks = []
    for minute in range(60):
        angle = math.radians(minute * 6)
        outer = 246
        inner = 234 if minute % 5 else 226
        x1, y1 = 450 + math.sin(angle) * inner, 357 - math.cos(angle) * inner
        x2, y2 = 450 + math.sin(angle) * outer, 357 - math.cos(angle) * outer
        marks.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{COLORS["cyan"]}" stroke-width="{3 if minute % 5 == 0 else 1}" opacity="{1 if minute % 5 == 0 else .45}"/>')
    labels = []
    for label, hour, color in skills:
        angle = math.radians(hour * 30)
        x, y = 450 + math.sin(angle) * 194, 357 - math.cos(angle) * 194
        labels.append(text(round(x), round(y), label, 14, color, "700", "middle"))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="700" viewBox="0 0 900 700" role="img" aria-labelledby="title desc"><title id="title">Tanu Tomar animated skill clock</title><desc id="desc">A futuristic analog clock with HTML, CSS, JavaScript, React, Node.js, PostgreSQL, SQL, Java, and C Basics around the dial.</desc>
<defs><radialGradient id="bg"><stop stop-color="#111A35"/><stop offset="1" stop-color="{COLORS["bg"]}"/></radialGradient><linearGradient id="neon"><stop stop-color="{COLORS["cyan"]}"/><stop offset=".5" stop-color="{COLORS["purple"]}"/><stop offset="1" stop-color="{COLORS["pink"]}"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="5" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<rect width="900" height="700" rx="24" fill="url(#bg)" stroke="#172342"/><text x="450" y="48" text-anchor="middle" fill="{COLORS["text"]}" font-family="ui-monospace,monospace" font-weight="700" font-size="25" letter-spacing="5">SKILL CLOCK</text><text x="450" y="74" text-anchor="middle" fill="{COLORS["cyan"]}" font-family="ui-monospace,monospace" font-size="11" letter-spacing="3">TANU TOMAR / DEVELOPER ORBIT</text>
<g fill="none" transform="translate(0 0)"><circle cx="450" cy="357" r="274" stroke="{COLORS["cyan"]}" opacity=".16" stroke-width="2"/><circle cx="450" cy="357" r="264" stroke="url(#neon)" stroke-width="4" stroke-dasharray="16 12" opacity=".85"><animateTransform attributeName="transform" type="rotate" from="0 450 357" to="360 450 357" dur="24s" repeatCount="indefinite"/></circle><circle cx="450" cy="357" r="256" stroke="{COLORS["purple"]}" stroke-width="1" stroke-dasharray="3 11" opacity=".8"><animateTransform attributeName="transform" type="rotate" from="360 450 357" to="0 450 357" dur="16s" repeatCount="indefinite"/></circle><circle cx="450" cy="357" r="218" fill="#060A17" stroke="{COLORS["cyan"]}" stroke-width="3"/><circle cx="450" cy="357" r="205" stroke="#25355F" stroke-width="1"/></g>
<g>{''.join(marks)}</g><g>{''.join(labels)}</g>
<g stroke-linecap="round"><line x1="450" y1="357" x2="450" y2="250" stroke="{COLORS["purple"]}" stroke-width="9" opacity=".28" filter="url(#glow)" transform="rotate({hour_angle:.3f} 450 357)"/><line x1="450" y1="357" x2="450" y2="250" stroke="{COLORS["purple"]}" stroke-width="6" transform="rotate({hour_angle:.3f} 450 357)"><animateTransform attributeName="transform" type="rotate" from="{hour_angle:.3f} 450 357" to="{hour_angle + 360:.3f} 450 357" dur="43200s" repeatCount="indefinite"/></line><line x1="450" y1="357" x2="450" y2="215" stroke="{COLORS["cyan"]}" stroke-width="8" opacity=".25" filter="url(#glow)" transform="rotate({minute_angle:.3f} 450 357)"/><line x1="450" y1="357" x2="450" y2="215" stroke="{COLORS["cyan"]}" stroke-width="5" transform="rotate({minute_angle:.3f} 450 357)"><animateTransform attributeName="transform" type="rotate" from="{minute_angle:.3f} 450 357" to="{minute_angle + 360:.3f} 450 357" dur="3600s" repeatCount="indefinite"/></line><line x1="450" y1="357" x2="450" y2="190" stroke="{COLORS["pink"]}" stroke-width="3" transform="rotate({second_angle:.3f} 450 357)"><animateTransform attributeName="transform" type="rotate" from="{second_angle:.3f} 450 357" to="{second_angle + 360:.3f} 450 357" dur="60s" repeatCount="indefinite"/></line></g>
<circle cx="450" cy="357" r="15" fill="{COLORS["bg"]}" stroke="url(#neon)" stroke-width="4"/><circle cx="450" cy="357" r="5" fill="{COLORS["text"]}"/><text x="450" y="340" fill="{COLORS["muted"]}" font-family="ui-monospace,monospace" font-size="10" text-anchor="middle" letter-spacing="2">SKILL CLOCK // ONLINE</text><text x="450" y="650" fill="{COLORS["cyan"]}" font-family="ui-monospace,monospace" font-size="12" text-anchor="middle" letter-spacing="2">HOUR / MINUTE / SECOND // LIVE MOTION</text></svg>'''
    write("skill-clock.svg", svg)


def generate_clock_precise() -> None:
    """Generate the centered 800px analog skill instrument used in the README."""
    cx, cy = 400, 400
    skills = [("HTML", 0, COLORS["cyan"]), ("CSS", 1, COLORS["purple"]), ("JavaScript", 2, COLORS["pink"]), ("React", 3, COLORS["cyan"]), ("Node.js", 4, COLORS["green"]), ("Python", 5, COLORS["pink"]), ("SQL", 6, COLORS["purple"]), ("PostgreSQL", 7, COLORS["cyan"]), ("Java", 8, COLORS["pink"]), ("DSA", 9, COLORS["cyan"]), ("Problem Solving", 10, COLORS["purple"]), ("C Basics", 11, COLORS["green"])]
    now = datetime.now(timezone.utc)
    hour_angle = ((now.hour % 12) + now.minute / 60 + now.second / 3600) * 30
    minute_angle = (now.minute + now.second / 60) * 6
    second_angle = (now.second + now.microsecond / 1_000_000) * 6
    ticks = []
    for minute in range(60):
        angle = math.radians(minute * 6)
        inner = 218 if minute % 5 == 0 else 229
        outer = 242
        ticks.append(f'<line x1="{cx + math.sin(angle) * inner:.1f}" y1="{cy - math.cos(angle) * inner:.1f}" x2="{cx + math.sin(angle) * outer:.1f}" y2="{cy - math.cos(angle) * outer:.1f}" stroke="{COLORS["cyan"]}" stroke-width="{3 if minute % 5 == 0 else 1}" opacity="{1 if minute % 5 == 0 else .38}"/>')
    label_nodes = []
    for label, hour, color in skills:
        angle = math.radians(hour * 30)
        marker_x = cx + math.sin(angle) * 250
        marker_y = cy - math.cos(angle) * 250
        label_x = cx + math.sin(angle) * 294
        label_y = cy - math.cos(angle) * 294 + (5 if hour in (0, 6) else 0)
        label_nodes.append(f'<line x1="{marker_x:.1f}" y1="{marker_y:.1f}" x2="{label_x:.1f}" y2="{label_y:.1f}" stroke="{color}" stroke-width="1" opacity=".55"/><circle cx="{marker_x:.1f}" cy="{marker_y:.1f}" r="4" fill="{color}"/><text x="{label_x:.1f}" y="{label_y:.1f}" fill="{color}" font-family="ui-monospace,monospace" font-size="13" font-weight="700" text-anchor="middle">{escape(label)}</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800" role="img" aria-labelledby="title desc"><title id="title">Tanu Tomar futuristic analog skill clock</title><desc id="desc">A professional analog skill clock centered at 400, 400 with HTML, CSS, JavaScript, React, Node.js, Python, SQL, PostgreSQL, Java, DSA, Problem Solving, and Git &amp; GitHub around the face.</desc>
<defs><radialGradient id="clock-bg"><stop stop-color="#111A35"/><stop offset="1" stop-color="#020617"/></radialGradient><linearGradient id="clock-accent"><stop stop-color="{COLORS["cyan"]}"/><stop offset=".5" stop-color="{COLORS["purple"]}"/><stop offset="1" stop-color="{COLORS["pink"]}"/></linearGradient><filter id="clock-glow"><feGaussianBlur stdDeviation="5" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<rect width="800" height="800" rx="24" fill="url(#clock-bg)" stroke="#172342"/><text x="400" y="42" text-anchor="middle" fill="{COLORS["text"]}" font-family="ui-monospace,monospace" font-size="24" font-weight="700" letter-spacing="5">SKILL CLOCK</text><text x="400" y="67" text-anchor="middle" fill="{COLORS["cyan"]}" font-family="ui-monospace,monospace" font-size="11" letter-spacing="3">TANU TOMAR / DEVELOPER CONTROL</text>
<circle cx="400" cy="400" r="282" fill="none" stroke="{COLORS["cyan"]}" stroke-width="2" opacity=".14"/><circle cx="400" cy="400" r="270" fill="none" stroke="url(#clock-accent)" stroke-width="4" stroke-dasharray="18 12"><animateTransform attributeName="transform" type="rotate" from="0 400 400" to="360 400 400" dur="28s" repeatCount="indefinite"/></circle><circle cx="400" cy="400" r="258" fill="none" stroke="{COLORS["purple"]}" stroke-width="1" stroke-dasharray="3 13"><animateTransform attributeName="transform" type="rotate" from="360 400 400" to="0 400 400" dur="18s" repeatCount="indefinite"/></circle>
<circle cx="400" cy="400" r="246" fill="#050914" stroke="{COLORS["cyan"]}" stroke-width="3"/><circle cx="400" cy="400" r="232" fill="none" stroke="#26375D" stroke-width="1"/>
<g>{''.join(ticks)}</g><g>{''.join(label_nodes)}</g>
<path d="M180 400H620" stroke="{COLORS["cyan"]}" opacity=".18" stroke-width="2"><animateTransform attributeName="transform" type="translate" values="0 -180;0 180;0 -180" dur="9s" repeatCount="indefinite"/></path>
<circle cx="400" cy="400" r="78" fill="#081024" stroke="url(#clock-accent)" stroke-width="2" opacity=".96"/><text x="400" y="386" text-anchor="middle" fill="{COLORS["text"]}" font-family="ui-monospace,monospace" font-size="21" font-weight="700">TANU</text><text x="400" y="412" text-anchor="middle" fill="{COLORS["text"]}" font-family="ui-monospace,monospace" font-size="21" font-weight="700">TOMAR</text><text x="400" y="437" text-anchor="middle" fill="{COLORS["cyan"]}" font-family="ui-monospace,monospace" font-size="10" letter-spacing="2">B.TECH CSE</text>
<g stroke-linecap="round"><line x1="400" y1="400" x2="400" y2="312" stroke="{COLORS["purple"]}" stroke-width="10" opacity=".28" filter="url(#clock-glow)" transform="rotate({hour_angle:.3f} 400 400)"/><line x1="400" y1="400" x2="400" y2="312" stroke="{COLORS["purple"]}" stroke-width="7" transform="rotate({hour_angle:.3f} 400 400)"><animateTransform attributeName="transform" type="rotate" from="{hour_angle:.3f} 400 400" to="{hour_angle + 360:.3f} 400 400" dur="43200s" repeatCount="indefinite"/></line><line x1="400" y1="400" x2="400" y2="260" stroke="{COLORS["cyan"]}" stroke-width="9" opacity=".25" filter="url(#clock-glow)" transform="rotate({minute_angle:.3f} 400 400)"/><line x1="400" y1="400" x2="400" y2="260" stroke="{COLORS["cyan"]}" stroke-width="5" transform="rotate({minute_angle:.3f} 400 400)"><animateTransform attributeName="transform" type="rotate" from="{minute_angle:.3f} 400 400" to="{minute_angle + 360:.3f} 400 400" dur="3600s" repeatCount="indefinite"/></line><line x1="400" y1="400" x2="400" y2="232" stroke="{COLORS["pink"]}" stroke-width="3" transform="rotate({second_angle:.3f} 400 400)"><animateTransform attributeName="transform" type="rotate" from="{second_angle:.3f} 400 400" to="{second_angle + 360:.3f} 400 400" dur="60s" repeatCount="indefinite"/></line></g><circle cx="400" cy="400" r="13" fill="#020617" stroke="url(#clock-accent)" stroke-width="4"/><circle cx="400" cy="400" r="4" fill="{COLORS["text"]}"/><text x="400" y="720" text-anchor="middle" fill="{COLORS["cyan"]}" font-family="ui-monospace,monospace" font-size="12" letter-spacing="2">SKILL CLOCK // ONLINE</text><text x="400" y="744" text-anchor="middle" fill="{COLORS["muted"]}" font-family="ui-monospace,monospace" font-size="10">HOUR / MINUTE / SECOND // LIVE MOTION</text></svg>'''
    write("skill-clock.svg", svg)


def generate_clock_gif() -> None:
    """Create a small raster fallback for renderers that ignore SVG animation."""
    try:
        from PIL import Image, ImageDraw  # pyright: ignore[reportMissingImports]
    except ImportError:
        print("warning: Pillow is unavailable; skill-clock.gif was not regenerated")
        return
    frames = []
    for frame_number in range(24):
        image = Image.new("RGB", (360, 360), COLORS["bg"])
        draw = ImageDraw.Draw(image)
        draw.ellipse((24, 24, 336, 336), outline=COLORS["cyan"], width=3)
        draw.ellipse((39, 39, 321, 321), outline=COLORS["purple"], width=1)
        for minute in range(60):
            angle = math.radians(minute * 6)
            outer = 150
            inner = 139 if minute % 5 else 132
            draw.line((180 + math.sin(angle) * inner, 180 - math.cos(angle) * inner, 180 + math.sin(angle) * outer, 180 - math.cos(angle) * outer), fill=COLORS["cyan"], width=2 if minute % 5 == 0 else 1)
        for length, angle, color, width in ((74, frame_number * 15, COLORS["pink"], 2), (58, frame_number * 0.25, COLORS["cyan"], 4), (42, frame_number * 0.0208, COLORS["purple"], 6)):
            radians = math.radians(angle)
            draw.line((180, 180, 180 + math.sin(radians) * length, 180 - math.cos(radians) * length), fill=color, width=width)
        draw.ellipse((173, 173, 187, 187), fill=COLORS["text"], outline=COLORS["cyan"], width=2)
        frames.append(image)
    frames[0].save(ASSETS / "skill-clock.gif", save_all=True, append_images=frames[1:], duration=100, loop=0, optimize=True)


def generate_static_assets() -> None:
    def panel(name: str, title: str, subtitle: str, rows: list[tuple[str, str, str]], height: int = 180) -> None:
        body = svg_start(900, height, title).replace("</svg>", "") + text(40, 48, title, 22, COLORS["text"], "700") + text(40, 76, subtitle, 12, COLORS["muted"])
        for index, (heading, value, color) in enumerate(rows):
            x = 40 + (index % 3) * 285
            y = 115 + (index // 3) * 44
            body += f'<rect x="{x}" y="{y-25}" width="250" height="34" rx="8" fill="{COLORS["panel2"]}" stroke="#1A2A4A"/><circle cx="{x+15}" cy="{y-8}" r="4" fill="{color}"/><text x="{x+28}" y="{y-4}" fill="{COLORS["muted"]}" font-family="ui-monospace,monospace" font-size="11">{escape(heading.upper())}</text><text x="{x+235}" y="{y-4}" fill="{COLORS["text"]}" font-family="ui-monospace,monospace" font-size="16" font-weight="700" text-anchor="end">{escape(value)}</text>'
        write(name, body + "</svg>")

    write("hero.svg", svg_start(900, 150, "Tanu Tomar developer mission control").replace("</svg>", "") + text(42, 58, "DEVELOPER MISSION CONTROL", 12, COLORS["cyan"], "700") + text(42, 98, "Learn deliberately. Build honestly. Keep moving.", 27, COLORS["text"], "700") + text(42, 126, "STATUS / CURIOUS · PRACTICING · IMPROVING", 12, COLORS["muted"]) + "</svg>")
    write("mission.svg", svg_start(900, 175, "G.R.I.L. Training at NVIDIA").replace("</svg>", "") + text(42, 58, "CURRENT MISSION // 2026", 12, COLORS["green"], "700") + text(42, 99, "G.R.I.L. TRAINING @ NVIDIA", 26, COLORS["text"], "700") + text(42, 128, "Strengthening engineering fundamentals while expanding software development and problem-solving skills.", 13, COLORS["muted"]) + text(42, 157, "ACTIVE     LEARNING     BUILDING     EXPLORING", 10, COLORS["green"], "700") + "</svg>")
    write("technology.svg", svg_start(900, 205, "Technology universe").replace("</svg>", "") + text(40, 45, "TECHNOLOGY UNIVERSE", 20, COLORS["text"], "700") + "".join(f'<rect x="{40 + i * 215}" y="75" width="195" height="90" rx="10" fill="{COLORS["panel2"]}" stroke="#1A2A4A"/><text x="{55 + i * 215}" y="101" fill="{color}" font-family="ui-monospace,monospace" font-size="11" font-weight="700">{group}</text><text x="{55 + i * 215}" y="130" fill="{COLORS["text"]}" font-family="ui-monospace,monospace" font-size="12">{escape(skills)}</text>' for i, (group, skills, color) in enumerate([("FRONTEND", "HTML · CSS · JS · React", COLORS["cyan"]), ("BACKEND", "Node.js", COLORS["purple"]), ("DATABASE", "SQL · PostgreSQL", COLORS["pink"]), ("PROGRAMMING", "Java · C Basics", COLORS["green"])])) + "</svg>")
    panel("focus.svg", "CURRENT FOCUS", "Learning signals, not proficiency claims.", [("WEB DEVELOPMENT", "EXPLORING", COLORS["cyan"]), ("REACT", "LEARNING", COLORS["purple"]), ("NODE.JS", "PRACTICING", COLORS["green"]), ("SQL", "LEARNING", COLORS["pink"]), ("POSTGRESQL", "EXPLORING", COLORS["cyan"]), ("PROGRAMMING", "PRACTICING", COLORS["purple"])], 205)
    path = [("FOUNDATIONS", COLORS["cyan"]), ("FRONTEND", COLORS["purple"]), ("BACKEND", COLORS["pink"]), ("DATABASES", COLORS["green"]), ("BUILD", COLORS["cyan"]), ("IMPROVE", COLORS["purple"])]
    body = svg_start(900, 150, "Learning path").replace("</svg>", "") + text(40, 45, "LEARNING PATH", 20, COLORS["text"], "700")
    for i, (label, color) in enumerate(path):
        x = 38 + i * 143
        body += f'<rect x="{x}" y="75" width="120" height="42" rx="8" fill="{COLORS["panel2"]}" stroke="{color}"/><text x="{x+60}" y="101" fill="{COLORS["text"]}" font-family="ui-monospace,monospace" font-size="11" text-anchor="middle">{label}</text>'
        if i < len(path) - 1:
            body += f'<path d="M{x+122} 96h16" stroke="{COLORS["muted"]}"/><path d="m{x+134} 90 6 6-6 6" fill="none" stroke="{COLORS["muted"]}"/>'
    write("learning-path.svg", body + "</svg>")
    write("footer.svg", svg_start(900, 90, "Learn build debug evolve").replace("</svg>", "") + text(450, 56, "LEARN  ·  BUILD  ·  DEBUG  ·  EVOLVE", 18, COLORS["text"], "700", "middle") + "</svg>")
    write("profile.svg", svg_start(900, 245, "Developer profile").replace("</svg>", "") + text(40, 45, "DEVELOPER PROFILE", 20, COLORS["text"], "700") + text(40, 70, "IDENTITY / Tanu Tomar", 12, COLORS["cyan"], "700") + "".join(f'<rect x="{40 + (i % 2) * 410}" y="{90 + (i // 2) * 48}" width="380" height="34" rx="8" fill="{COLORS["panel2"]}" stroke="#1A2A4A"/><text x="{55 + (i % 2) * 410}" y="{112 + (i // 2) * 48}" fill="{color}" font-family="ui-monospace,monospace" font-size="10" font-weight="700">{label}</text><text x="{200 + (i % 2) * 410}" y="{112 + (i // 2) * 48}" fill="{COLORS["text"]}" font-family="ui-monospace,monospace" font-size="11">{value}</text>' for i, (label, value, color) in enumerate([("ROLE", "B.Tech CSE Student · Developer", COLORS["purple"]), ("CURRENT MISSION", "G.R.I.L. Training @ NVIDIA", COLORS["green"]), ("FOCUS", "Web Development · DSA · Problem Solving", COLORS["pink"]), ("INTERESTS", "Frontend · Backend · Databases", COLORS["cyan"]), ("LEARNING MODE", "Build → Practice → Experiment → Improve", COLORS["purple"])])) + "</svg>")
    write("constellation.svg", svg_start(900, 220, "Skill constellation").replace("</svg>", "") + text(40, 45, "SKILL CONSTELLATION", 20, COLORS["text"], "700") + text(40, 68, "A working map of the systems Tanu is learning and practicing.", 11, COLORS["muted"]) + "".join(f'<rect x="{40 + (i % 3) * 275}" y="{88 + (i // 3) * 52}" width="245" height="38" rx="8" fill="{COLORS["panel2"]}" stroke="#1A2A4A"/><text x="{55 + (i % 3) * 275}" y="{111 + (i // 3) * 52}" fill="{color}" font-family="ui-monospace,monospace" font-size="10" font-weight="700">{label}</text><text x="{55 + (i % 3) * 275}" y="{124 + (i // 3) * 52}" fill="{COLORS["text"]}" font-family="ui-monospace,monospace" font-size="10">{value}</text>' for i, (label, value, color) in enumerate([("LANGUAGES", "Java · JavaScript · C · SQL", COLORS["cyan"]), ("FRONTEND", "HTML · CSS · React", COLORS["purple"]), ("BACKEND", "Node.js · REST APIs", COLORS["pink"]), ("DATABASE", "SQL · PostgreSQL", COLORS["green"]), ("COMPUTER SCIENCE", "DSA · Problem Solving", COLORS["cyan"]), ("TOOLS", "Git · GitHub", COLORS["purple"])])) + "</svg>")
    trajectory_nodes = []
    trajectory = [("FOUNDATIONS", COLORS["cyan"]), ("FRONTEND", COLORS["purple"]), ("BACKEND", COLORS["pink"]), ("DATABASE", COLORS["green"]), ("ENGINEERING", COLORS["cyan"])]
    for i, (label, color) in enumerate(trajectory):
        x = 72 + i * 172
        trajectory_nodes.append(f'<circle cx="{x}" cy="115" r="12" fill="{COLORS["bg"]}" stroke="{color}" stroke-width="3"/><text x="{x}" y="158" fill="{COLORS["text"]}" font-family="ui-monospace,monospace" font-size="10" text-anchor="middle">{label}</text>')
        if i < len(trajectory) - 1:
            trajectory_nodes.append(f'<path d="M{x + 12} 115h148" stroke="{COLORS["muted"]}" stroke-dasharray="4 6"/>')
    write("trajectory.svg", svg_start(900, 210, "Learning trajectory").replace("</svg>", "") + text(40, 43, "LEARNING TRAJECTORY", 20, COLORS["text"], "700") + text(40, 67, "A connected path from fundamentals to engineering practice.", 11, COLORS["muted"]) + "".join(trajectory_nodes) + "</svg>")
    write("learning.svg", svg_start(900, 230, "Currently learning").replace("</svg>", "") + text(40, 43, "CURRENTLY LEARNING", 20, COLORS["text"], "700") + text(40, 67, "Status markers describe direction, not mastery.", 11, COLORS["muted"]) + "".join(f'<rect x="{40 + (i % 3) * 275}" y="{88 + (i // 3) * 48}" width="245" height="34" rx="8" fill="{COLORS["panel2"]}" stroke="#1A2A4A"/><circle cx="{57 + (i % 3) * 275}" cy="{105 + (i // 3) * 48}" r="4" fill="{color}"><animate attributeName="opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/></circle><text x="{70 + (i % 3) * 275}" y="{109 + (i // 3) * 48}" fill="{COLORS["text"]}" font-family="ui-monospace,monospace" font-size="11">{escape(label)}</text><text x="{270 + (i % 3) * 275}" y="{109 + (i // 3) * 48}" fill="{color}" font-family="ui-monospace,monospace" font-size="9" text-anchor="end">{escape(status)}</text>' for i, (label, status, color) in enumerate([("DSA", "PRACTICING", COLORS["cyan"]), ("Problem Solving", "ACTIVE", COLORS["purple"]), ("Advanced JavaScript", "EXPLORING", COLORS["pink"]), ("React Development", "PRACTICING", COLORS["green"]), ("Node.js", "EXPLORING", COLORS["cyan"]), ("REST APIs", "LEARNING", COLORS["purple"]), ("Database Design", "EXPLORING", COLORS["pink"]), ("Git & GitHub", "PRACTICING", COLORS["green"]), ("Software Engineering", "LEARNING", COLORS["cyan"])])) + "</svg>")
    write("signals.svg", svg_start(900, 155, "Developer signal").replace("</svg>", "") + text(40, 43, "DEVELOPER SIGNAL", 20, COLORS["text"], "700") + "".join(f'<text x="{45 + i * 205}" y="92" fill="{color}" font-family="ui-monospace,monospace" font-size="11" font-weight="700">{escape(label)}</text><text x="{45 + i * 205}" y="116" fill="{COLORS["muted"]}" font-family="ui-monospace,monospace" font-size="10">{escape(value)}</text>' for i, (label, value, color) in enumerate([("BUILDING", "Web Development", COLORS["cyan"]), ("TRAINING", "G.R.I.L. @ NVIDIA", COLORS["green"]), ("PRACTICING", "DSA & Problem Solving", COLORS["purple"]), ("EXPLORING", "Backend & Databases", COLORS["pink"])])) + "</svg>")


def generate_skill_panels() -> None:
    categories = [("LANGUAGES", "Python · JavaScript", COLORS["cyan"]), ("FRONTEND", "React.js · HTML/CSS · Tailwind CSS", COLORS["purple"]), ("DEVELOPMENT", "REST APIs · Git · GitHub", COLORS["pink"]), ("DEPLOYMENT", "Docker", COLORS["green"]), ("PROBLEM SOLVING", "Data Structures & Algorithms", COLORS["cyan"]), ("TOOLS", "VS Code", COLORS["purple"])]
    body = svg_start(900, 285, "Technology universe").replace("</svg>", "") + text(40, 45, "TECHNOLOGY UNIVERSE", 20, COLORS["text"], "700") + text(40, 68, "Current tools and learning areas, without proficiency claims.", 11, COLORS["muted"])
    for i, (category, skills, color) in enumerate(categories):
        x = 40 + (i % 3) * 275
        y = 90 + (i // 3) * 88
        body += f'<rect x="{x}" y="{y}" width="245" height="66" rx="10" fill="{COLORS["panel2"]}" stroke="#1A2A4A"/><text x="{x + 15}" y="{y + 23}" fill="{color}" font-family="ui-monospace,monospace" font-size="10" font-weight="700">{category}</text><text x="{x + 15}" y="{y + 47}" fill="{COLORS["text"]}" font-family="ui-monospace,monospace" font-size="10">{escape(skills)}</text>'
    write("technology.svg", body + "</svg>")
    learning = [("Data Structures & Algorithms", "PRACTICING", COLORS["cyan"]), ("Full Stack Development", "BUILDING", COLORS["purple"]), ("REST APIs", "LEARNING", COLORS["pink"]), ("Docker", "EXPLORING", COLORS["green"]), ("Deployment", "EXPLORING", COLORS["cyan"]), ("Real-World Software Development", "BUILDING", COLORS["purple"])]
    body = svg_start(900, 205, "Current learning active").replace("</svg>", "") + text(40, 43, "CURRENT LEARNING // ACTIVE", 20, COLORS["text"], "700") + text(40, 67, "Status signals show direction, not mastery.", 11, COLORS["muted"])
    for i, (skill, status, color) in enumerate(learning):
        x = 40 + (i % 3) * 275
        y = 90 + (i // 3) * 42
        body += f'<rect x="{x}" y="{y}" width="245" height="30" rx="8" fill="{COLORS["panel2"]}" stroke="#1A2A4A"/><circle cx="{x + 15}" cy="{y + 15}" r="4" fill="{color}"><animate attributeName="opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/></circle><text x="{x + 28}" y="{y + 19}" fill="{COLORS["text"]}" font-family="ui-monospace,monospace" font-size="10">{escape(skill)}</text><text x="{x + 232}" y="{y + 19}" fill="{color}" font-family="ui-monospace,monospace" font-size="9" text-anchor="end">{status}</text>'
    write("learning.svg", body + "</svg>")


def fetch_data() -> tuple[dict, list, dict]:
    if not TOKEN:
        raise RuntimeError("GITHUB_TOKEN is required for live GitHub analytics generation.")

    profile = api(f"/users/{urllib.parse.quote(USER)}")
    if not isinstance(profile, dict):
        raise RuntimeError("GitHub returned an invalid profile response")
    if profile.get("login", "").lower() != USER.lower():
        raise RuntimeError(f"GitHub returned a different account than {USER}")

    repos = []
    page = 1
    while True:
        batch = api(f"/users/{urllib.parse.quote(USER)}/repos?per_page=100&page={page}&type=owner&sort=updated")
        if not isinstance(batch, list):
            raise RuntimeError("GitHub returned an invalid repository response")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    repos = [repo for repo in repos if repo.get("private") is False]

    now = datetime.now(timezone.utc).replace(microsecond=0)
    start = now - timedelta(days=365)
    query = """query($login:String!, $from:DateTime!, $to:DateTime!) {
      user(login:$login) {
        contributionsCollection(from:$from, to:$to) {
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
          totalRepositoryContributions
          contributionCalendar {
            totalContributions
            weeks { contributionDays { contributionCount date } }
          }
        }
      }
    }"""
    response = api("/graphql", method="POST", body={
        "query": query,
        "variables": {
            "login": USER,
            "from": start.isoformat().replace("+00:00", "Z"),
            "to": now.isoformat().replace("+00:00", "Z"),
        },
    })
    if not isinstance(response, dict):
        raise RuntimeError("GitHub returned an invalid GraphQL response")
    if response.get("errors"):
        raise RuntimeError(f"GitHub GraphQL returned errors: {response['errors']}")
    data = response.get("data")
    user_data = data.get("user") if isinstance(data, dict) else None
    contributions = user_data.get("contributionsCollection") if isinstance(user_data, dict) else None
    calendar = contributions.get("contributionCalendar") if contributions else None
    if not contributions or not isinstance(calendar, dict) or not isinstance(calendar.get("weeks"), list):
        raise RuntimeError("GitHub did not return the rolling-year contribution calendar")

    language_repos: Counter[str] = Counter()
    language_bytes: Counter[str] = Counter()
    for repo in repos:
        if repo.get("private") is not False or repo.get("fork") or not repo.get("full_name") or not repo.get("language"):
            continue
        languages = api(f"/repos/{repo['full_name']}/languages")
        if not isinstance(languages, dict):
            raise RuntimeError(f"GitHub returned invalid language data for {repo['full_name']}")
        measured_languages = {name: size for name, size in languages.items() if isinstance(size, int) and size > 0}
        language_repos.update(measured_languages.keys())
        language_bytes.update(measured_languages)

    return profile, repos, {"contributions": contributions, "language_repos": language_repos, "language_bytes": language_bytes, "window_start": start, "window_end": now}


def generate_repository_radar(repos: list) -> None:
    meaningful = [repo for repo in repos if not repo.get("fork") and not repo.get("archived")][:5]
    height = 115 + max(len(meaningful), 1) * 34
    body = svg_start(900, height, "Repository radar").replace("</svg>", "") + text(40, 42, "REPOSITORY RADAR", 20, COLORS["text"], "700") + text(40, 65, "Public repositories detected from the GitHub API.", 11, COLORS["muted"])
    if not meaningful:
        body += text(40, 108, "Repository radar is warming up — more builds coming online.", 13, COLORS["muted"])
    for index, repo in enumerate(meaningful):
        y = 99 + index * 34
        name = repo.get("name", "Unnamed repository")
        description = (repo.get("description") or "No description provided")[:62]
        language = repo.get("language") or "Unspecified"
        updated = (repo.get("updated_at") or "")[:10] or "Unknown"
        body += f'<rect x="40" y="{y-19}" width="820" height="26" rx="6" fill="{COLORS["panel2"]}" stroke="#1A2A4A"/><text x="52" y="{y-2}" fill="{COLORS["cyan"]}" font-family="ui-monospace,monospace" font-size="11" font-weight="700">{escape(name)}</text><text x="220" y="{y-2}" fill="{COLORS["muted"]}" font-family="ui-monospace,monospace" font-size="10">{escape(description)}</text><text x="650" y="{y-2}" fill="{COLORS["purple"]}" font-family="ui-monospace,monospace" font-size="10">{escape(language)}</text><text x="840" y="{y-2}" fill="{COLORS["muted"]}" font-family="ui-monospace,monospace" font-size="10" text-anchor="end">★ {repo.get("stargazers_count", 0)} · {updated}</text>'
    write("repository-radar.svg", body + "</svg>")


def contribution_data(contributions: dict) -> tuple[dict, list[tuple[date, int]]]:
    calendar = contributions.get("contributionCalendar")
    if not isinstance(calendar, dict):
        raise RuntimeError("Contribution calendar data is missing")
    days = []
    for week in calendar.get("weeks", []):
        for item in week.get("contributionDays", []):
            try:
                days.append((date.fromisoformat(item["date"]), int(item["contributionCount"])))
            except (KeyError, TypeError, ValueError):
                raise RuntimeError("GitHub returned an invalid contribution day")
    if not days or not isinstance(calendar.get("totalContributions"), int):
        raise RuntimeError("GitHub returned an empty or invalid contribution calendar")
    days.sort()
    return calendar, days


def generate_activity_card(profile: dict, repos: list, contributions: dict, window_start: datetime, window_end: datetime) -> None:
    calendar, days = contribution_data(contributions)
    month_totals: Counter[str] = Counter()
    for day, count in days:
        if window_start.date() <= day <= window_end.date():
            month_totals[day.strftime("%Y-%m")] += count

    end_month = window_end.date().replace(day=1)
    months = []
    for offset in range(11, -1, -1):
        month_index = end_month.year * 12 + end_month.month - 1 - offset
        months.append(f"{month_index // 12:04d}-{month_index % 12 + 1:02d}")
    values = [month_totals[month] for month in months]
    stars = sum(repo.get("stargazers_count", 0) for repo in repos if isinstance(repo.get("stargazers_count"), int))

    body = svg_start(1200, 350, f"GitHub contribution activity for {USER}").replace("</svg>", "")
    body += text(38, 42, "MY GITHUB PROFILE", 18, COLORS["text"], "700")
    body += text(38, 80, USER, 25, COLORS["cyan"], "700")
    body += '<path d="M430 28V322" stroke="#1A2A4A" stroke-width="1"/>'
    profile_rows = [
        ("CONTRIBUTIONS / LAST 12 MONTHS", calendar["totalContributions"], COLORS["purple"]),
        ("PUBLIC REPOSITORIES", profile.get("public_repos"), COLORS["cyan"]),
        ("STARS ON PUBLIC REPOSITORIES", stars, COLORS["green"]),
        ("JOINED GITHUB", profile.get("created_at", "")[:10], COLORS["pink"]),
    ]
    y = 127
    for label, value, accent in profile_rows:
        if not isinstance(value, (int, str)) or not value:
            continue
        body += f'<circle cx="48" cy="{y - 5}" r="4" fill="{accent}"/><text x="63" y="{y}" fill="{COLORS["muted"]}" font-family="ui-monospace,monospace" font-size="10">{escape(label)}</text><text x="63" y="{y + 20}" fill="{COLORS["text"]}" font-family="ui-monospace,monospace" font-size="15" font-weight="700">{escape(str(value))}</text>'
        y += 49

    body += text(465, 42, "contributions in the last year", 16, COLORS["text"], "700")
    body += text(465, 63, f"{window_start.date().isoformat()} TO {window_end.date().isoformat()} / MONTHLY TOTALS", 9, COLORS["muted"])
    chart_left, chart_right = 520, 1162
    chart_top, chart_bottom = 94, 282
    max_value = max(values, default=0)
    tick = max(1, math.ceil(max_value / 4))
    ceiling = tick * 4
    for tick_index in range(5):
        y_pos = chart_bottom - (chart_bottom - chart_top) * tick_index / 4
        body += f'<path d="M{chart_left} {y_pos:.1f}H{chart_right}" stroke="#1A2A4A" stroke-width="1"/><text x="{chart_left - 11}" y="{y_pos + 4:.1f}" text-anchor="end" fill="{COLORS["cyan"]}" font-family="ui-monospace,monospace" font-size="9">{tick * tick_index}</text>'

    points = []
    for index, (month, value) in enumerate(zip(months, values)):
        x = chart_left + (chart_right - chart_left) * index / (len(months) - 1)
        y_pos = chart_bottom - (chart_bottom - chart_top) * value / ceiling
        points.append((x, y_pos))
        body += f'<text x="{x:.1f}" y="{chart_bottom + 20}" text-anchor="middle" fill="{COLORS["cyan"]}" font-family="ui-monospace,monospace" font-size="9">{date.fromisoformat(month + "-01").strftime("%b")}</text>'

    line_path = f"M{points[0][0]:.1f},{points[0][1]:.1f}"
    for (start_x, start_y), (end_x, end_y) in zip(points, points[1:]):
        dx = end_x - start_x
        line_path += f" C{start_x + dx * 0.4:.1f},{start_y:.1f} {end_x - dx * 0.4:.1f},{end_y:.1f} {end_x:.1f},{end_y:.1f}"
    area_path = f"M{points[0][0]:.1f},{chart_bottom} L{points[0][0]:.1f},{points[0][1]:.1f}{line_path[len(f'M{points[0][0]:.1f},{points[0][1]:.1f}'):]} L{points[-1][0]:.1f},{chart_bottom} Z"
    body += f'<path d="{area_path}" fill="{COLORS["purple"]}" opacity=".48"/><path d="{line_path}" fill="none" stroke="{COLORS["cyan"]}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
    for x, y_pos in points:
        body += f'<circle cx="{x:.1f}" cy="{y_pos:.1f}" r="3" fill="{COLORS["cyan"]}" stroke="{COLORS["bg"]}" stroke-width="1"/>'
    write("github-activity.svg", body + "</svg>")


def generate_language_donut(filename: str, title: str, subtitle: str, data: Counter, unit: str) -> None:
    body = svg_start(600, 330, title).replace("</svg>", "")
    body += text(28, 40, title.upper(), 16, COLORS["text"], "700")
    body += text(28, 61, subtitle, 9, COLORS["muted"])
    ranked = data.most_common(5)
    total = sum(data.values())
    if not ranked or total == 0:
        raise RuntimeError(f"GitHub returned no language data for {title}")
    rows = list(ranked)
    remainder = total - sum(value for _, value in ranked)
    if remainder:
        rows.append(("Other", remainder))
    colors = [COLORS["cyan"], COLORS["purple"], COLORS["pink"], COLORS["green"], "#5B8CFF", "#A9B5D0"]
    circumference = 2 * math.pi * 57
    body += f'<circle cx="155" cy="185" r="57" fill="none" stroke="#172342" stroke-width="18"/>'
    offset = 0.0
    for index, (language, value) in enumerate(rows):
        segment = circumference * value / total
        body += f'<circle cx="155" cy="185" r="57" fill="none" stroke="{colors[index % len(colors)]}" stroke-width="18" stroke-dasharray="{segment:.2f} {circumference:.2f}" stroke-dashoffset="{-offset:.2f}" transform="rotate(-90 155 185)"/>'
        offset += segment
        y = 126 + index * 36
        percentage = value / total * 100
        body += f'<circle cx="270" cy="{y - 4}" r="4" fill="{colors[index % len(colors)]}"/><text x="284" y="{y}" fill="{COLORS["text"]}" font-family="ui-monospace,monospace" font-size="11">{escape(language)}</text><text x="558" y="{y}" text-anchor="end" fill="{COLORS["muted"]}" font-family="ui-monospace,monospace" font-size="10">{value:,} {escape(unit)} · {percentage:.1f}%</text>'
    body += text(155, 181, str(len(rows)), 20, COLORS["text"], "700", "middle")
    body += text(155, 199, "LANGUAGES", 8, COLORS["muted"], "400", "middle")
    write(filename, body + "</svg>")


def generate_stats_card(repos: list, contributions: dict) -> None:
    stats = [
        ("TOTAL STARS", sum(repo.get("stargazers_count", 0) for repo in repos), COLORS["green"]),
        ("COMMITS / LAST 12 MONTHS", contributions.get("totalCommitContributions"), COLORS["cyan"]),
        ("PULL REQUESTS / LAST 12 MONTHS", contributions.get("totalPullRequestContributions"), COLORS["purple"]),
        ("ISSUES / LAST 12 MONTHS", contributions.get("totalIssueContributions"), COLORS["pink"]),
        ("REPOSITORIES CONTRIBUTED TO", contributions.get("totalRepositoryContributions"), COLORS["green"]),
    ]
    stats = [(label, value, color) for label, value, color in stats if isinstance(value, int) and value >= 0]
    body = svg_start(600, 330, "GitHub stats").replace("</svg>", "")
    body += text(28, 40, "STATS", 16, COLORS["text"], "700")
    body += text(28, 61, f"{USER} / LAST 12 MONTHS WHERE SHOWN", 9, COLORS["muted"])
    for index, (label, value, accent) in enumerate(stats):
        y = 82 + index * 46
        body += f'<rect x="28" y="{y}" width="544" height="36" rx="7" fill="{COLORS["panel2"]}" stroke="#1A2A4A"/><circle cx="47" cy="{y + 18}" r="4" fill="{accent}"/><text x="62" y="{y + 22}" fill="{COLORS["text"]}" font-family="ui-monospace,monospace" font-size="10">{label}</text><text x="550" y="{y + 23}" text-anchor="end" fill="{COLORS["text"]}" font-family="ui-monospace,monospace" font-size="14" font-weight="700">{value:,}</text>'
    write("github-stats.svg", body + "</svg>")


def generate_contributions_bar(contributions: dict, window_start: datetime, window_end: datetime) -> None:
    calendar, days = contribution_data(contributions)
    month_totals: Counter[str] = Counter()
    for day, count in days:
        if window_start.date() <= day <= window_end.date():
            month_totals[day.strftime("%Y-%m")] += count
    end_month = window_end.date().replace(day=1)
    months = []
    for offset in range(11, -1, -1):
        month_index = end_month.year * 12 + end_month.month - 1 - offset
        months.append(f"{month_index // 12:04d}-{month_index % 12 + 1:02d}")
    values = [month_totals[month] for month in months]

    body = svg_start(600, 330, "Monthly Contributions").replace("</svg>", "")
    body += text(28, 40, "MONTHLY CONTRIBUTIONS", 16, COLORS["text"], "700")
    body += text(28, 61, "ROLLING 12-MONTH CONTRIBUTION CALENDAR / NOT HOURLY DATA", 8, COLORS["muted"])
    chart_left, chart_right = 58, 575
    chart_top, chart_bottom = 96, 260
    max_value = max(values, default=0)
    tick = max(1, math.ceil(max_value / 3))
    ceiling = tick * 3
    for tick_index in range(4):
        value = tick * tick_index
        y_pos = chart_bottom - (chart_bottom - chart_top) * tick_index / 3
        body += f'<path d="M{chart_left} {y_pos:.1f}H{chart_right}" stroke="#1A2A4A"/><text x="{chart_left - 9}" y="{y_pos + 3:.1f}" text-anchor="end" fill="{COLORS["cyan"]}" font-family="ui-monospace,monospace" font-size="8">{value}</text>'
    colors = [COLORS["cyan"], COLORS["purple"], COLORS["pink"], COLORS["green"]]
    slot = (chart_right - chart_left) / len(values)
    bar_width = min(25, slot * 0.58)
    for index, (month, value) in enumerate(zip(months, values)):
        height = (chart_bottom - chart_top) * value / ceiling
        x = chart_left + index * slot + (slot - bar_width) / 2
        body += f'<rect x="{x:.1f}" y="{chart_bottom - height:.1f}" width="{bar_width:.1f}" height="{height:.1f}" rx="3" fill="{colors[index % len(colors)]}"/>'
        body += f'<text x="{x + bar_width / 2:.1f}" y="280" text-anchor="middle" fill="{COLORS["muted"]}" font-family="ui-monospace,monospace" font-size="8">{date.fromisoformat(month + "-01").strftime("%b")}</text>'
    write("github-commits-hourly.svg", body + "</svg>")


def generate_pulse() -> None:
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    body = svg_start(900, 110, "GitHub pulse").replace("</svg>", "")
    body += text(35, 43, "PROFILE DATA SYNC", 18, COLORS["text"], "700")
    body += text(35, 70, f"GITHUB API / {USER} / REFRESHED {updated}", 10, COLORS["muted"])
    body += '<circle cx="858" cy="53" r="7" fill="#76B900"><animate attributeName="opacity" values="1;.35;1" dur="2.5s" repeatCount="indefinite"/></circle>'
    write("github-pulse.svg", body + "</svg>")


def generate_dynamic(profile: dict, repos: list, extra: dict) -> None:
    repo_languages = extra["language_repos"]
    language_bytes = extra["language_bytes"]
    if not repo_languages:
        raise RuntimeError("GitHub returned no public repository language data")
    if not language_bytes:
        raise RuntimeError("GitHub returned no public repository language byte data")

    generate_repository_radar(repos)
    generate_pulse()
    contributions = extra["contributions"]
    generate_activity_card(profile, repos, contributions, extra["window_start"], extra["window_end"])
    generate_language_donut("github-languages-repo.svg", "Top Languages by Repo", "LANGUAGES PRESENT / NON-FORK PUBLIC REPOSITORIES", repo_languages, "repos")
    generate_language_donut("github-languages-commit.svg", "Top Languages by Code", "LANGUAGE BY BYTES / NON-FORK PUBLIC REPOSITORIES", language_bytes, "bytes")
    generate_stats_card(repos, contributions)
    generate_contributions_bar(contributions, extra["window_start"], extra["window_end"])


def main() -> int:
    if not TOKEN:
        print("GITHUB_TOKEN is required for live GitHub analytics generation.", file=sys.stderr)
        return 1
    try:
        profile, repos, extra = fetch_data()
    except RuntimeError as error:
        print(f"error: analytics data was not refreshed; previous SVGs are unchanged: {error}", file=sys.stderr)
        return 1
    ASSETS.mkdir(exist_ok=True)
    generate_clock_precise()
    generate_clock_gif()
    generate_static_assets()
    generate_skill_panels()
    generate_dynamic(profile, repos, extra)
    print(f"generated profile assets for {USER}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
