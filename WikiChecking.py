import requests
import time
import csv

headers = {
    "User-Agent": "SJQC Dictionary Project/1.0 (Jenni)" # change as needed (shouldn't matter though)
}

api_url = "https://en.wiktionary.org/w/api.php"

# call all entries in category

params = {
    "action": "query",
    "list": "categorymembers",
    "cmtitle": "Category:San_Juan_Quiahije_Chatino_verbs", # change as needed
    "cmlimit": "max",
    "format": "json"
}

words = []

while True:
    r = requests.get(api_url, params=params, headers=headers)
    data = r.json()

    words.extend(item["title"] for item in data["query"]["categorymembers"])

    if "continue" not in data:
        break

    params["cmcontinue"] = data["continue"]["cmcontinue"]

print(f"Found {len(words)} words")

# fethcing defs 
rows = []

for i, word in enumerate(words):
    print(f"[{i+1}/{len(words)}] {word}")

    params2 = {
        "action": "query",
        "prop": "revisions",
        "titles": word,
        "rvprop": "content",
        "rvslots": "main",
        "format": "json"
    }

    r = requests.get(api_url, params=params2, headers=headers)

    # trying to skip bad entries that cause JSON parsing errors
    try:
        data = r.json()
    except Exception:
        print("Error parsing JSON, skipping...")
        time.sleep(20)
        continue

    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), {})

    rev = page.get("revisions")
    if not rev:
        continue

    text = rev[0]["slots"]["main"]["*"]

    definitions = [
        line[2:].strip()
        for line in text.splitlines()
        if line.startswith("# ")
    ]

    if definitions:
        rows.append([word, " ; ".join(definitions)])

    # trying to work around rate limits lol
    time.sleep(20)

# csv output
filename = "chatino_verbs_final.csv" # change as needed

with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Word", "Definitions"])
    writer.writerows(rows)

print(f"\nSaved {len(rows)} entries to {filename}")