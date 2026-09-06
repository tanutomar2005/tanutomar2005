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
from datetime import datetime, timedelta, timezone
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


def fetch_data() -> tuple[dict, list, Counter, list, dict | None]:
    profile = api(f"/users/{urllib.parse.quote(USER)}")
    repos = []
    page = 1
    while page <= 10:
        batch = api(f"/users/{urllib.parse.quote(USER)}/repos?per_page=100&page={page}&type=owner&sort=updated")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    languages: Counter[str] = Counter()
    for repo in repos:
        if repo.get("fork"):
            continue
        try:
            for language, amount in api(f"/repos/{repo['full_name']}/languages").items():
                languages[language] += amount
        except RuntimeError as error:
            print(f"warning: language data skipped for {repo.get('name')}: {error}")
    events = api(f"/users/{urllib.parse.quote(USER)}/events/public?per_page=12")
    searches = {}
    for kind in ("pr", "issue"):
        try:
            searches[kind] = api(f"/search/issues?q={urllib.parse.quote(f'author:{USER} type:{kind}')}&per_page=1").get("total_count", 0)
        except RuntimeError:
            searches[kind] = 0
    contributions = None
    if TOKEN:
        query = "query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{contributionCount date} }}}}}"
        try:
            contributions = api("/graphql", method="POST", body={"query": query, "variables": {"login": USER}})
        except RuntimeError as error:
            print(f"warning: contributions unavailable: {error}")
    return profile, repos, languages, events, {"searches": searches, "contributions": contributions}


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


def generate_dynamic(profile: dict, repos: list, languages: Counter, events: list, extra: dict) -> None:
    generate_repository_radar(repos)
    searches = extra["searches"]
    push_events = sum(1 for event in events if event.get("type") == "PushEvent")
    stats = [("PUBLIC REPOSITORIES", str(profile.get("public_repos", 0)), COLORS["cyan"]), ("FOLLOWERS", str(profile.get("followers", 0)), COLORS["purple"]), ("FOLLOWING", str(profile.get("following", 0)), COLORS["pink"]), ("PUBLIC STARS", str(sum(repo.get("stargazers_count", 0) for repo in repos)), COLORS["green"]), ("PULL REQUESTS", str(searches.get("pr", 0)), COLORS["cyan"]), ("ISSUES", str(searches.get("issue", 0)), COLORS["purple"]), ("RECENT PUSH EVENTS", str(push_events), COLORS["pink"])]
    body = svg_start(900, 205, "GitHub telemetry").replace("</svg>", "") + text(40, 47, "GITHUB TELEMETRY", 21, COLORS["text"], "700") + text(40, 72, f"LIVE DATA / {USER}", 11, COLORS["muted"])
    for i, (label, value, color) in enumerate(stats):
        x, y = 40 + (i % 3) * 285, 105 + (i // 3) * 55
        body += f'<rect x="{x}" y="{y-25}" width="250" height="42" rx="8" fill="{COLORS["panel2"]}" stroke="#1A2A4A"/><circle cx="{x+17}" cy="{y-4}" r="4" fill="{color}"/><text x="{x+30}" y="{y}" fill="{COLORS["muted"]}" font-family="ui-monospace,monospace" font-size="11">{label}</text><text x="{x+230}" y="{y}" fill="{COLORS["text"]}" font-family="ui-monospace,monospace" font-size="18" font-weight="700" text-anchor="end">{value}</text>'
    write("github-stats.svg", body + "</svg>")
    total = sum(languages.values()) or 1
    language_rows = languages.most_common(6)
    body = svg_start(900, max(150, 72 + len(language_rows) * 25), "Top languages from public repositories").replace("</svg>", "") + text(40, 45, "LANGUAGE UNIVERSE", 20, COLORS["text"], "700") + text(40, 68, "Calculated from detected repository language bytes.", 11, COLORS["muted"])
    palette = [COLORS["cyan"], COLORS["purple"], COLORS["pink"], COLORS["green"]]
    if not language_rows:
        body += text(40, 110, "No public repository language data detected yet.", 13, COLORS["muted"])
    for i, (language, amount) in enumerate(language_rows):
        y = 98 + i * 25
        width = round(510 * amount / total)
        body += text(40, y + 11, language, 12, COLORS["text"], "700") + f'<rect x="175" y="{y}" width="510" height="12" rx="6" fill="#111A31"/><rect x="175" y="{y}" width="{max(width, 3)}" height="12" rx="6" fill="{palette[i % len(palette)]}"/><text x="710" y="{y+11}" fill="{COLORS["muted"]}" font-family="ui-monospace,monospace" font-size="11">{amount / total:.1%}</text>'
    write("top-languages.svg", body + "</svg>")
    body = svg_start(900, 205, "Recent GitHub activity").replace("</svg>", "") + text(40, 45, "GITHUB ACTIVITY", 20, COLORS["text"], "700") + text(40, 68, "Recent public events from the GitHub activity stream.", 11, COLORS["muted"])
    if not events:
        body += text(40, 110, "No recent public activity returned.", 13, COLORS["muted"])
    for i, event in enumerate(events[:5]):
        y = 96 + i * 20
        kind = event.get("type", "Activity").replace("Event", "")
        repo = event.get("repo", {}).get("name", "unknown repository")
        body += f'<circle cx="48" cy="{y-4}" r="3" fill="{palette[i % len(palette)]}"/>' + text(62, y, f"{kind} / {repo}", 11, COLORS["text"])
    write("activity.svg", body + "</svg>")
    contribution_data = (extra.get("contributions") or {}).get("data", {}).get("user", {}).get("contributionsCollection", {}).get("contributionCalendar")
    if contribution_data:
        days = [day for week in contribution_data.get("weeks", []) for day in week.get("contributionDays", [])]
        body = svg_start(900, 210, "GitHub contribution universe").replace("</svg>", "") + text(40, 43, "CONTRIBUTION UNIVERSE", 20, COLORS["text"], "700") + text(40, 67, f"{contribution_data.get('totalContributions', 0)} contributions in the last year", 11, COLORS["muted"])
        levels = ["#111A31", "#0B4960", "#087A86", COLORS["cyan"], COLORS["purple"]]
        start = datetime.now(timezone.utc).date() - timedelta(days=364)
        for index, day in enumerate(days[-371:]):
            x = 40 + (index % 53) * 15
            y = 88 + (index // 53) * 15
            count = day.get("contributionCount", 0)
            level = 0 if count == 0 else min(4, 1 + count // 3)
            body += f'<rect x="{x}" y="{y}" width="10" height="10" rx="2" fill="{levels[level]}" aria-label="{escape(day.get("date", str(start)))}: {count} contributions"/>'
        write("contributions.svg", body + "</svg>")
    elif not (ASSETS / "contributions.svg").exists() or "Contribution data will appear after" in (ASSETS / "contributions.svg").read_text(encoding="utf-8"):
        write("contributions.svg", svg_start(900, 150, "Contribution data unavailable").replace("</svg>", "") + text(40, 55, "CONTRIBUTION UNIVERSE", 20, COLORS["text"], "700") + text(40, 95, "Contribution telemetry will synchronize during the next profile update.", 13, COLORS["muted"]) + "</svg>")


def main() -> int:
    ASSETS.mkdir(exist_ok=True)
    generate_clock()
    generate_clock_gif()
    generate_static_assets()
    try:
        profile, repos, languages, events, extra = fetch_data()
        generate_dynamic(profile, repos, languages, events, extra)
    except RuntimeError as error:
        print(f"warning: dynamic assets kept from previous run: {error}")
        return 0
    print(f"generated profile assets for {USER}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
