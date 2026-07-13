import pandas as pd
import requests

words = pd.read_csv("*.csv")["word"].dropna()

for word in words:
    r = requests.get(
        "https://en.wiktionary.org/w/api.php",
        params={
            "action": "query",
            "titles": word,
            "format": "json",
        },
    )

    pages = r.json()["query"]["pages"]
    exists = "-1" not in pages
    print(word, exists)