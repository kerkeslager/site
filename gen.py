import collections
import errno
import os
import os.path
import shutil
import string

import blog
import menu
import sml
import template

def rm_r_if_exists(path):
    try:
        shutil.rmtree(path)
    except FileNotFoundError as e:
        if e.errno != errno.ENOTDIR and e.errno != errno.ENOENT:
            raise

def mktree(root_path, tree):
    assert isinstance(root_path, str)
    assert isinstance(tree, dict)

    for directory, contents in tree.items():
        directory_path = os.path.join(root_path, directory)
        os.mkdir(directory_path)
        mktree(directory_path, contents)

current_dir = os.path.dirname(os.path.abspath(__file__))
TARGET_DIR = os.path.join(current_dir, 'dest')

rm_r_if_exists(TARGET_DIR)
mktree(current_dir, {
    'dest': {
        'posts': {},
    },
})

template_index_filename = 'index.html'
target_index_filename = 'index.html'

template_index_path = os.path.join(template.template_dir, template_index_filename)
target_index_path = os.path.join(TARGET_DIR, target_index_filename)

LITERAL_DIR = os.path.join(current_dir, 'literal')

for literal_filename in os.listdir(LITERAL_DIR):
    literal_file_path = os.path.join(LITERAL_DIR, literal_filename)
    target_file_path = os.path.join(TARGET_DIR, literal_filename)
    
    try:
        shutil.copytree(literal_file_path, target_file_path)
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copyfile(literal_file_path, target_file_path)
        else:
            raise

index_template = template.get_template(template_index_path)
index_html = template.apply_base_template(
    '::1',
    ['David Kerkeslager'],
    [],
    "David Kerkeslager's personal website",
    index_template.substitute(menu = menu.MENU),
)

with open(target_index_path, 'w') as target_index_file:
    target_index_file.write(index_html)

posts_target_dir = os.path.join(TARGET_DIR, 'posts')
posts_src_dir = os.path.join(current_dir, 'posts')

post_links = list(blog.generate(posts_src_dir, posts_target_dir))

blog_template_filename = os.path.join(template.template_dir, 'blog.html')
target_blog_filename = os.path.join(TARGET_DIR, 'blog.html')

blog_template = template.get_template(blog_template_filename)
blog_html = template.apply_base_template(
    'Blog',
    ['David Kerkeslager'],
    ['blog,David Kerkeslager'],
    "David Kerkeslager's blog",
    blog_template.substitute(
        menu = menu.MENU,
        posts = ''.join(sml.write(pl) for pl in post_links),
    ),
)

with open(target_blog_filename, 'w') as target_blog_file:
    target_blog_file.write(blog_html)

# TODO Generate About, Signals, and 404 from the pages/ directory

Page = collections.namedtuple(
    'Page',
    [
        'template_name',
        'title',
        'authors',
        'keywords',
        'description',
    ],
)

pages = [
    Page(
        template_name = 'about.html',
        title = 'About',
        authors = ['David Kerkeslager'],
        keywords = ['David Kerkeslager','kerkeslager.com'],
        description = 'About David Kerkeslager and his website',
    ),
    Page(
        template_name = 'card.html',
        title = 'Card',
        authors = ['David Kerkeslager'],
        keywords = ['Links'],
        description = 'Business Card',
    ),
    Page(
        template_name = 'signals.html',
        title = 'Signals',
        authors = ['David Kerkeslager'],
        keywords = ['Links'],
        description = 'Signals in the noise',
    ),
    Page(
        template_name = '404.html',
        title = '404 File Not Found',
        authors = ['David Kerkeslager'],
        keywords = ['error','404'],
        description = '404 File not found',
    ),
]

for page in pages:
    template_path = os.path.join(template.template_dir, page.template_name)
    templ = template.get_template(template_path)
    target_path = os.path.join(TARGET_DIR, page.template_name)

    html = template.apply_base_template(
        page.title,
        page.authors,
        page.keywords,
        page.description,
        templ.substitute(menu = menu.MENU),
    )

    with open(target_path, 'w') as target_file:
        target_file.write(html)
