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

# Get initial count for display purposes
initial_count = len(wiki_cats_processing)
print(f"Starting with {initial_count} categories to process")

# Create a progress bar
pbar = tqdm(total=initial_count, desc="Processing categories")
processed_count = 0

while len(wiki_cats_processing) > 0:
    # Process a category
    category = wiki_cats_processing.pop()
    process_category(category)

    # Update progress count
    processed_count += 1

    # If we've found more categories than we started with, update the total
    current_total = processed_count + len(wiki_cats_processing)
    if current_total > pbar.total:
        pbar.total = current_total

    # Update the progress bar
    pbar.update(1)
    pbar.set_postfix({"Remaining": len(wiki_cats_processing), "Total found": len(wiki_cats_processed)})

# Close the progress bar when done
pbar.close()

print(f"Processed {processed_count} categories, found {len(wiki_cats_processed)} unique categories")

with open('hk_categories.txt', 'w') as fOut:
    fOut.write('\n'.join(wiki_cats_processed))

hk_titles = set()

for category in tqdm(wiki_cats_processed, desc="Getting titles by category"):
    titles = get_wiki_titles_by_category(category)
    hk_titles.update(titles)

print(f"Found {len(hk_titles)} titles")

with open('notebooks/cantonese/wikipedia/hk_titles.txt', 'w') as fOut:
    fOut.write('\n'.join([f'{title[0]}\t{title[1]}' for title in hk_titles]))

hk_articles = []

with multiprocessing.Pool(8) as pool:
    for articles in tqdm(pool.imap(get_wiki_article, [title[0] for title in hk_titles]),
                         total=len(hk_titles),
                         desc="Fetching articles"):
        hk_articles.append(articles)

print(clean_unused_text(hk_articles[13]))

df = pd.DataFrame({'text': [clean_unused_text(a) for a in hk_articles],
                   'title': [title[0] for title in hk_titles],
                   'category': [title[1] for title in hk_titles]})

print("Checking for missing content...")
for title in tqdm(df[df['text'].isna()]['title'], desc="Retrying failed titles"):
    index = df[df['title'] == title].index[0]
    article = get_wiki_article(title)
    if article:
        df.at[index, 'text'] = article

missed_contents_index = df[df['text'].isna()]['title'].index
print(f"Dropping {len(missed_contents_index)} titles with missing content")
df.drop(missed_contents_index, inplace=True)

# Title to category mapping is now built directly in the DataFrame creation
df.drop_duplicates(subset=['title', 'text'], inplace=True)
print(f"Final dataset size: {len(df)} articles")

df.to_csv('notebooks/cantonese/wikipedia/hk_articles.csv', index=False)
print(df.head())