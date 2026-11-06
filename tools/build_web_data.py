#!/usr/bin/env python3
"""Export compact JSON for the static site from jburson/bible-data (KJV only).

Usage: python3 tools/build_web_data.py /path/to/bible-data/data docs/data

Outputs
  books.json     [[name, testament, chapters], ...]            index = book id - 1
  verses.json    [[bookIdx, chapter, verse, text], ...]        index = verse id (canonical order)
  strongs.json   {"g26": [definition, pronunciation, partOfSpeech], ...}
  uses.json      {"g26": [[verseIdx, "english", ...], ...]}    verseIdx followed by its English words
"""
import json
import os
import sys
from collections import defaultdict


def clean_verse(raw):
    out = []
    for tok in raw.split(" "):
        if "*" in tok:
            word, feat = tok.split("*", 1)
            if "s" in feat:
                word = word.upper()
            out.append(word)
        else:
            out.append(tok)
    return " ".join(out)


def dump(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
    print(f"{os.path.basename(path)}: {os.path.getsize(path)/1e6:.2f} MB")


def main(data_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    load = lambda *p: json.load(open(os.path.join(data_dir, *p), encoding="utf-8"))
    kjv, inter = load("kjv", "kjv.json"), load("kjv", "kjv-interlinear.json")
    books, strongs = load("books.json"), load("interlinear", "strongs.json")

    book_idx = {b["book"]: i for i, b in enumerate(books)}
    dump([[b["book"], b["testament"], b["numChapters"]] for b in books], os.path.join(out_dir, "books.json"))

    verses, by_order = [], {}
    for item in kjv:
        if "h" in item:
            continue
        _, book, ch, vs = item["r"].split(":")
        by_order[item["o"]] = len(verses)
        verses.append([book_idx[book], int(ch), int(vs), clean_verse(item["t"])])
    dump(verses, os.path.join(out_dir, "verses.json"))

    dump(
        {k: [" ".join((e.get("d") or "").split()), e.get("p") or "", e.get("s") or ""] for k, e in strongs.items()},
        os.path.join(out_dir, "strongs.json"),
    )

    uses = defaultdict(lambda: defaultdict(set))
    for item in inter:
        if "h" in item:
            continue
        vi = by_order.get(item["o"])
        if vi is None:  # Psalm titles: tagged in the interlinear file but not verses in kjv.json
            continue
        for d in item.get("d", []):
            sid = (d.get("s") or "").lower()
            if sid:
                uses[sid][vi].add(d["t"].split("|")[0])
    out = {sid: [[vi, *sorted(en)] for vi, en in sorted(m.items())] for sid, m in uses.items()}
    dump(out, os.path.join(out_dir, "uses.json"))
    print(f"verses={len(verses)} strongs_with_uses={len(out)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
