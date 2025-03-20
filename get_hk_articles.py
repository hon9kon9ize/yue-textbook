import wikipediaapi
import pandas as pd
from tqdm.auto import tqdm
import multiprocessing
import re
from matplotlib import pyplot as plt
from datasets import load_dataset

wiki = wikipediaapi.Wikipedia('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36', language='zh', extract_format=wikipediaapi.ExtractFormat.WIKI)

def get_wiki_article(title):
    try:
        page = wiki.page(title)
        if page is None or not page.exists():
            return ''
        output = page.text
        return output
    except:
        return ''

def get_wiki_category(category):
    page = wiki.page(category)
    categories = set([page for page in page.categorymembers.keys() if page.startswith('Category:')])
    return list(categories)

def get_wiki_titles_by_category(category_name):
    category = wiki.page(category_name)
    titles = list(set([(page, category_name) for page in category.categorymembers if not (page.startswith('Category:') or page.startswith('Template:') or page.startswith('Portal:'))]))
    return titles

def clean_unused_text(text):
    text_to_clean = ["連出去","出面網頁","睇埋","註","註同攷","參考","拎","攷"]
    pattern = r'\n({})[\s\S]*'.format('|'.join(text_to_clean))
    output = re.sub(pattern, '', text)
    return output

print(get_wiki_article('香港'))

wiki_cats_processing = set(['Category:香港'])
wiki_cats_processed = set()

def process_category(category):
  if category in wiki_cats_processed:
    return
  categories = get_wiki_category(category)
  if len(categories) == 0:
    return
  wiki_cats_processed.update([category])
  wiki_cats_processing.update(categories)

while len(wiki_cats_processing) > 0:
  process_category(wiki_cats_processing.pop())

with open('hk_categories.txt', 'w') as fOut:
  fOut.write('\n'.join(wiki_cats_processed))

hk_titles = set()

for category in tqdm(wiki_cats_processed):
  titles = get_wiki_titles_by_category(category)
  hk_titles.update(titles)

print(len(hk_titles))

with open('notebooks/cantonese/wikipedia/hk_titles.txt', 'w') as fOut:
  fOut.write('\n'.join([f'{title[0]}\t{title[1]}' for title in hk_titles]))

hk_articles = []

with multiprocessing.Pool(8) as pool:
  for articles in tqdm(pool.imap(get_wiki_article, hk_titles), total=len(hk_titles)):
    hk_articles.append(articles)

print(clean_unused_text(hk_articles[13]))

df = pd.DataFrame({'text': [clean_unused_text(a) for a in hk_articles], 'title': list(hk_titles) })

for title in tqdm(df[df['text'].isna()]['title']):
  index = df[df['title'] == title].index[0]
  article = get_wiki_article(title)
  if article:
    df.at[index, 'text'] = article

missed_contents_index = df[df['text'].isna()]['title'].index
df.drop(missed_contents_index, inplace=True)

title_to_cats = {title: re.sub(r'^Category:', '', category) for title, category in hk_titles}
df['category'] = df['title'].apply(lambda x: title_to_cats[x])

df.drop_duplicates(subset=['title', 'text'], inplace=True)

df.to_csv('notebooks/cantonese/wikipedia/hk_articles.csv', index=False)
print(df)
