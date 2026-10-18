#!/usr/bin/env python3
"""Build content.json from image files and per-anime folders for GitHub Pages."""
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
ART_DIR = ROOT / "assets" / "artworks"
ANIME_DIR = ROOT / "assets" / "anime"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}

def title_from_filename(name: str) -> str:
    stem = Path(name).stem
    stem = re.sub(r"[-_]+", " ", stem)
    stem = re.sub(r"\bfeatured\b", "", stem, flags=re.I)
    stem = re.sub(r"\s+", " ", stem).strip()
    return stem.title() if stem else "Retutta artwork"

def read_description(folder: Path) -> str:
    for filename in ("description.md", "description.txt", "info.txt"):
        path = folder / filename
        if path.is_file():
            text = path.read_text(encoding="utf-8").strip()
            # First non-empty line may be a Markdown heading; use it as title only if title.txt is absent.
            return text
    return ""

def read_title(folder: Path, default: str) -> str:
    path = folder / "title.txt"
    return path.read_text(encoding="utf-8").strip() if path.is_file() else default

ART_DIR.mkdir(parents=True, exist_ok=True)
ANIME_DIR.mkdir(parents=True, exist_ok=True)
artworks = []
for p in sorted(ART_DIR.iterdir(), key=lambda p: p.name.lower()):
    if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
        artworks.append({
            "src": "./assets/artworks/" + p.name,
            "title": title_from_filename(p.name),
            "description": "",
            "featured": "featured" in p.stem.lower() or "main" in p.stem.lower()
        })

anime = []
for folder in sorted(ANIME_DIR.iterdir(), key=lambda p: p.name.lower()):
    if not folder.is_dir():
        continue
    images = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS]
    if not images:
        continue
    images.sort(key=lambda p: (0 if p.stem.lower() in {"cover", "poster", "обложка"} else 1, p.name.lower()))
    description = read_description(folder)
    default_title = re.sub(r"[-_]+", " ", folder.name).strip().title()
    anime.append({
        "src": "./assets/anime/" + folder.name + "/" + images[0].name,
        "title": read_title(folder, default_title),
        "description": description,
        "featured": False
    })

games_path = ROOT / "games.json"
games = json.loads(games_path.read_text(encoding="utf-8")) if games_path.exists() else []
data = {"artworks": artworks, "anime": anime, "games": games}
(ROOT / "content.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Built content.json: {len(artworks)} artworks, {len(anime)} anime entries, {len(games)} games.")
