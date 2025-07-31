import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent

input_excel = base_dir / "20211030 Test Assignment" / "Input.xlsx"
output_dir = base_dir / "20211030 Test Assignment" / "Article_txt_files"

output_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_excel(input_excel)
id_list = df["URL_ID"].astype(str).tolist()
url_list = df["URL"].tolist()
url_to_id = dict(zip(url_list, id_list))

def get_title_and_text(resp):
    soup = BeautifulSoup(resp.content, 'html.parser')
    title_tag = soup.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else ""

    containers = soup.find_all('div', class_='td-post-content tagdiv-type') + \
                 soup.find_all(True, class_='wp-block-list')

    for tag in soup.find_all('a'):
        tag.unwrap()
    for tag in soup.find_all('div', class_='wp-block-heading'):
        tag.unwrap()

    paragraphs = []
    for container in containers:
        for tag in container.find_all(['p', 'li']):
            txt = tag.get_text(strip=True)
            if txt:
                paragraphs.append(txt)
    return title, paragraphs

done_count = 0
for url in tqdm(url_list, desc="Fetching and Saving Articles"):
    while True:
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                ttl, p = get_title_and_text(resp)
                if ttl and p:
                    text = f"{ttl}\n\n" + "\n".join(p)
                    file_id = url_to_id[url]
                    filepath = output_dir / f"{file_id}.txt"
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(text)
                    done_count += 1
                break
            else:
                tqdm.write(f"↳ {url} returned {resp.status_code}")
        except requests.RequestException as e:
            tqdm.write(f"↳ Error fetching {url}: {e}")
        time.sleep(1)

print(f"\n✅ Done! {done_count} articles saved in:\n  {output_dir}")
