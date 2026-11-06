# KJV Concordance (web)

A free, offline-capable King James Bible concordance that runs entirely in the browser. No server, no tracking, no accounts.

- **Search** any word: see every form (love, loved, loveth…) with counts, then every verse with the word highlighted. Filter by Old/New Testament.
- **Read** any chapter.
- **Strong's**: look up G/H numbers or search definitions; see every verse and how the KJV translated the word.
- **Bookmark** verses (saved in your browser only), copy or share them.
- Works offline after the first visit; light and dark themes.

The same data powers the Android app.

## Run locally
The page loads JSON files, so serve the `docs` folder over http (opening the file directly won't work):

    python3 -m http.server 8000 --directory docs

then open <http://localhost:8000>.

## Publish with GitHub Pages
Repo **Settings → Pages → Build and deployment → Deploy from a branch → `main` / `/docs`**. The site appears at `https://<your-username>.github.io/<repo-name>/`.

## Updating the data
`docs/data/*.json` is generated from a clone of [jburson/bible-data](https://github.com/jburson/bible-data):

    python3 tools/build_web_data.py /path/to/bible-data/data docs/data

If you change `index.html` or the data, bump `VERSION` in `docs/sw.js` so returning visitors get the new files.

## Licensing
- **KJV text**: public domain in the United States (in the UK it is under Crown letters patent).
- **Strong's dictionary and KJV word tagging**: taken from jburson/bible-data, whose origin and license are not documented (that repo has no license file and says "use with permission of the copyright holders"). Strong's original work is public domain, but confirm the data's source before relying on it commercially.
- This project uses **only the KJV**. Don't add ESV, NIV, NASB, CSB or NKJV without a license from the publisher.
- The code in this repo is yours to license as you like; add a `LICENSE` file (MIT is a common choice) once you've decided.

## Known limitations
- Single-word search only (no phrases yet).
- Case is ignored, so "Lord" and "LORD" are one entry. Use Strong's (H3068 vs H136) to tell them apart.
- About 6% of Strong's occurrences, including H3068 (the LORD's name), have no dictionary entry in the source data. Their verses still list.
