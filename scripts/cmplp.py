import time
import datetime

import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

custom_matching = {
    'index': 'About',
    'blog': 'Blog',
}

rootPath = Path(sys.argv[0]).absolute().parent.parent
layoutPath = rootPath / 'layout/'
pagesPath = rootPath / 'pages/'
postsPath = rootPath / 'posts'

docsPath = rootPath / 'docs'

start_time = time.perf_counter()
print('Started compiling website...')
env = Environment(
    loader=FileSystemLoader([layoutPath, pagesPath]))

page_links = []
print('Gathering all pages:')
pages = list(pagesPath.glob('*.html'))
for page in pages:
    if page.stem in custom_matching:
        page_links.append([custom_matching[page.stem], page.stem + '.html'])
    else:
        page_links.append([page.stem, page.stem + '.html'])
    print(f'\t - {page.stem}')
page_links.sort()

print('Gathering all posts:')
posts = list(postsPath.glob('*.html'))
for post in posts:
    print(f'\t - {post.stem}')

for page in pages:
    print(page)
    with open(page, 'r+', encoding='utf-8') as page_file:
        template = env.get_template(page.stem + '.html')
        print('[Compiling] - ', page.stem + '.html')
        with open(docsPath / Path((page.stem + '.html')), 'w+', encoding='utf-8') as rendered_file:
            rendered_file.write(template.render(
                current_page=page.stem,
                now=datetime.datetime.now(),
                page_links = page_links
            ))

elapsed_time  = time.perf_counter() - start_time
print(f'Finished in {elapsed_time:.4f} seconds')