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

post_links = blog.generate(posts_src_dir, posts_target_dir)

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

# TODO Generate About, Signals, and 404 from the pages/ directory

with open(target_blog_filename, 'w') as target_blog_file:
    target_blog_file.write(blog_html)

about_template_path = os.path.join(template.template_dir, 'about.html')
about_template = template.get_template(about_template_path)
about_target_path = os.path.join(TARGET_DIR, 'about.html')

about_html = template.apply_base_template(
    'About',
    ['David Kerkeslager'],
    ['David Kerkeslager','kerkeslager.com'],
    'About David Kerkeslager and his website',
    about_template.substitute(menu = menu.MENU),
)

with open(about_target_path, 'w') as about_target_file:
    about_target_file.write(about_html)
    
signals_template_path = os.path.join(template.template_dir, 'signals.html')
signals_template = template.get_template(signals_template_path)
signals_target_path = os.path.join(TARGET_DIR, 'signals.html')

signals_html = template.apply_base_template(
    'Signals',
    ['David Kerkeslager'],
    ['Links'],
    'Signals in the noise',
    signals_template.substitute(menu = menu.MENU),
)

with open(signals_target_path, 'w') as signals_target_file:
    signals_target_file.write(signals_html)

file_not_found_template_path = os.path.join(template.template_dir, '404.html')
file_not_found_template = template.get_template(file_not_found_template_path)
file_not_found_target_path = os.path.join(TARGET_DIR, '404.html')

file_not_found_html = template.apply_base_template(
    '404 File Not Found',
    ['David Kerkeslager'],
    ['error','404'],
    '404 File not found',
    file_not_found_template.substitute(menu = menu.MENU),
)

with open(file_not_found_target_path, 'w') as file_not_found_target_file:
    file_not_found_target_file.write(file_not_found_html)
