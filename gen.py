import collections
import errno
import os
import os.path
import shutil
import string

import post
import sml

def get_template(path):
    with open(path, 'r') as f:
        return string.Template(f.read())

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
template_dir = os.path.join(current_dir, 'templates')
TARGET_DIR = os.path.join(current_dir, 'dest')

rm_r_if_exists(TARGET_DIR)
mktree(current_dir, {
    'dest': {
        'posts': {},
    },
})

BASE_TEMPLATE = get_template(os.path.join(template_dir, 'base.html'))
def apply_base_template(title, authors, keywords, description, body):
    return BASE_TEMPLATE.substitute(
        title = title,
        authors = ','.join(authors),
        keywords = ','.join(keywords),
        description = description,
        body = body,
    )

template_index_filename = 'index.html'
target_index_filename = 'index.html'

template_index_path = os.path.join(template_dir, template_index_filename)
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

MENU = '''
<a href='/'>Home</a>
<a href='/about.html'>About</a>
<a href='/blog.html'>Blog</a>
<a href='https://www.github.com/kerkeslager'>Code</a>
'''

index_template = get_template(template_index_path)
index_html = apply_base_template(
    'Home',
    ['David Kerkeslager'],
    [],
    "David Kerkeslager's personal website",
    index_template.substitute(menu = MENU),
)

with open(target_index_path, 'w') as target_index_file:
    target_index_file.write(index_html)

target_posts_dir = os.path.join(TARGET_DIR, 'posts')

posts_dir = os.path.join(current_dir, 'posts')
post_filenames = [fn for fn in os.listdir(posts_dir) if fn.endswith('.post')]

post_instances_and_target_paths = []

for post_filename in post_filenames:
    post_path = os.path.join(posts_dir, post_filename)
    p = post.from_file(post_path)
    target_post_filename = post_filename[:-4] + 'html'
    post_target_path = os.path.join(target_posts_dir, target_post_filename)

    post_instances_and_target_paths.append((p, post_target_path))

post_instances_and_target_paths = list(sorted(
    post_instances_and_target_paths,
    key = lambda piatp: piatp[0].published,
    reverse = True,
))
post_links = []

for p, post_target_path in post_instances_and_target_paths:
    with open(post_target_path, 'w') as f:
        f.write(apply_base_template(
            p.title,
            p.authors,
            p.keywords,
            p.description,
            post.to_html(p, MENU),
        ))

    post_links.append(sml.Node(
        tag = 'li',
        attributes = {},
        children = [
            sml.Node(
                tag = 'date',
                attributes = {},
                children = [p.published.date().isoformat()],
            ),
            '&nbsp;',
            sml.Node(
                tag = 'a',
                attributes = { 'href': '/posts/{}'.format(target_post_filename) },
                children = [p.title],
            ),
        ]
    ))
    
blog_template_filename = os.path.join(template_dir, 'blog.html')
target_blog_filename = os.path.join(TARGET_DIR, 'blog.html')

blog_template = get_template(blog_template_filename)
blog_html = apply_base_template(
    'Blog',
    ['David Kerkeslager'],
    ['blog,David Kerkeslager'],
    "David Kerkeslager's blog",
    blog_template.substitute(
        menu = MENU,
        posts = ''.join(sml.write(pl) for pl in post_links),
    ),
)


with open(target_blog_filename, 'w') as target_blog_file:
    target_blog_file.write(blog_html)

about_template_path = os.path.join(template_dir, 'about.html')
about_template = get_template(about_template_path)
about_target_path = os.path.join(TARGET_DIR, 'about.html')

about_html = apply_base_template(
    'About',
    ['David Kerkeslager'],
    ['David Kerkeslager','kerkeslager.com'],
    'About David Kerkeslager and his website',
    about_template.substitute(menu = MENU),
)

with open(about_target_path, 'w') as about_target_file:
    about_target_file.write(about_html)

file_not_found_template_path = os.path.join(template_dir, '404.html')
file_not_found_template = get_template(file_not_found_template_path)
file_not_found_target_path = os.path.join(TARGET_DIR, '404.html')

file_not_found_html = apply_base_template(
    '404 File Not Found',
    ['David Kerkeslager'],
    ['error','404'],
    '404 File not found',
    file_not_found_template.substitute(menu = MENU),
)

with open(file_not_found_target_path, 'w') as file_not_found_target_file:
    file_not_found_target_file.write(file_not_found_html)
