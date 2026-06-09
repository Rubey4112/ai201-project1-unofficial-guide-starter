#!/usr/bin/env python3
"""
Scrape sources from planning.md and save as normalized markdown files in documents/.

Usage:
    python scrape_documents.py

Each output file has YAML frontmatter (title, source, url) followed by clean markdown content.

NOTE: JavaScript-heavy pages (e.g. GMU Patriot Perks) may produce little or no content
      automatically — add those manually after running this script.
"""

import json
import re
import time
from pathlib import Path

import trafilatura

SOURCES = [
    {
        "id": 1,
        "source": "r/gmu",
        "title": "Anyone have any tips for incoming GMU freshman?",
        "url": "https://www.reddit.com/r/gmu/comments/1k9mks/anyone_have_any_tips_for_incoming_gmu_freshman/",
    },
    {
        "id": 2,
        "source": "r/gmu",
        "title": "Looking at going to gmu, what is there to do for fun around gmu?",
        "url": "https://www.reddit.com/r/gmu/comments/tdc7tz/looking_at_going_to_gmu_what_is_there_to_do_for/",
    },
    {
        "id": 3,
        "source": "Bond's Escape Room",
        "title": "Things to do near GMU Guide",
        "url": "https://bondsescaperoom.com/epic-things-to-do-near-gmu-student-guide",
    },
    {
        "id": 4,
        "source": "GMU",
        "title": "Patriot Perk things to do",
        "url": "https://patriotperks.gmu.edu/things-to-do/",
    },
    {
        "id": 5,
        "source": "GMU",
        "title": "Patriot Perk food and drinks",
        "url": "https://patriotperks.gmu.edu/food-drink/",
    },
    {
        "id": 6,
        "source": "Blog",
        "title": "My 11 Favorite Things to Do in Fairfax, VA (From a Local)",
        "url": "https://virginiavacationguide.com/things-to-do-in-fairfax-va/",
    },
    {
        "id": 7,
        "source": "DC's Website",
        "title": "DC Music Venues You Have to Experience",
        "url": "https://washington.org/visit-dc/live-music-venues-washington-dc",
    },
    {
        "id": 8,
        "source": "DC's Website",
        "title": "Your DC Bucket List",
        "url": "https://washington.org/visit-dc/bucket-list",
    },
    {
        "id": 9,
        "source": "DC's Website",
        "title": "Your Washington, DC Summer Bucket Listist 2",
        "url": "https://washington.org/visit-dc/your-washington-dc-summer-bucket-list",
    },
    {
        "id": 10,
        "source": "Blog",
        "title": "25 Fun Unique Things to Do in Alexandria VA",
        "url": "https://www.funinfairfaxva.com/things-to-do-in-alexandria-va/",
    },
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; gmu-guide-scraper/1.0)"}
DOCUMENTS_DIR = Path("documents")
DOCUMENTS_DIR.mkdir(exist_ok=True)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text[:40].strip("-")


def scrape_reddit(url: str) -> str:
    slug = url.rstrip("/").split("/")[-1]
    json_path = DOCUMENTS_DIR / f"{slug}.json"
    data = json.loads(json_path.read_text(encoding="utf-8"))

    post = data[0]["data"]["children"][0]["data"]
    post_title = post.get("title", "")
    post_body = post.get("selftext", "").strip()

    comment_texts = []
    for child in data[1]["data"]["children"]:
        if child["kind"] != "t1":
            continue
        body = child["data"].get("body", "").strip()
        score = child["data"].get("score", 0)
        if body and body not in ("[deleted]", "[removed]") and score > 1:
            comment_texts.append(f"- {body}")

    parts = [f"# {post_title}"]
    if post_body:
        parts.append(post_body)
    if comment_texts:
        parts.append("## Top Comments\n")
        parts.extend(comment_texts)

    return "\n\n".join(parts)


def scrape_web(url: str) -> str | None:
    downloaded = trafilatura.fetch_url(url)
    if downloaded is None:
        return None
    return trafilatura.extract(
        downloaded,
        output_format="markdown",
        include_links=False,
        include_images=False,
        favor_recall=True,
    )


def frontmatter(source: dict) -> str:
    title = source["title"].replace('"', '\\"')
    src = source["source"].replace('"', '\\"')
    return f'---\ntitle: "{title}"\nsource: "{src}"\nurl: "{source["url"]}"\n---\n\n'


def main() -> None:
    for source in SOURCES:
        doc_id = source["id"]
        slug = slugify(source["title"])
        out_path = DOCUMENTS_DIR / f"doc_{doc_id:02d}_{slug}.md"

        print(f"[{doc_id:02d}] {source['title']}")

        try:
            if "reddit.com" in source["url"]:
                content = scrape_reddit(source["url"])
            else:
                content = scrape_web(source["url"])

            if not content:
                content = "TODO: content could not be extracted automatically — paste manually."
                print(f"  WARNING: no content extracted")
            else:
                word_count = len(content.split())
                print(f"  {word_count} words extracted")

            out_path.write_text(frontmatter(source) + content, encoding="utf-8")
            print(f"  -> {out_path}")

        except Exception as exc:
            print(f"  ERROR: {exc}")

        time.sleep(1)


if __name__ == "__main__":
    main()
