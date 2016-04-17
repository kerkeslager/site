import collections
import os
import os.path
import string

import post
import sml

current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')
target_dir = os.path.join(current_dir, 'target')

template_index_filename = 'index.html'
target_index_filename = 'index.html'

template_index_path = os.path.join(template_dir, template_index_filename)
target_index_path = os.path.join(target_dir, target_index_filename)

MENU = '''
<a href='/'>Home</a>
<a href='/blog.html'>Blog</a>
<a href='https://www.github.com/kerkeslager'>GitHub</a>
'''

with open(template_index_path, 'r') as template_index_file:
    template_index = string.Template(template_index_file.read())

    html_index = template_index.substitute(menu = MENU)

    with open(target_index_path, 'w') as target_index_file:
        target_index_file.write(html_index)

target_posts_dir = os.path.join(target_dir, 'posts')

posts_dir = os.path.join(current_dir, 'posts')
post_filenames = [fn for fn in os.listdir(posts_dir) if fn.endswith('.post')]
post_links = []

for post_filename in post_filenames:
    post_path = os.path.join(posts_dir, post_filename)
    p = post.from_file(post_path)
    target_post_filename = post_filename[:-4] + 'html'
    post_target_path = os.path.join(target_posts_dir, target_post_filename)

    with open(post_target_path, 'w') as f:
        f.write(post.to_html(p, MENU))

    post_links.append(sml.Node(
        tag = 'li',
        attributes = {},
        children = [
            sml.Node(
                tag = 'a',
                attributes = { 'href': '/posts/{}'.format(target_post_filename) },
                children = [p.title],
            ),
        ]
    ))
    
blog_template_filename = os.path.join(template_dir, 'blog.html')
target_blog_filename = os.path.join(target_dir, 'blog.html')

with open(blog_template_filename, 'r') as template_file:
    template = string.Template(template_file.read())
    html = template.substitute(
        menu = MENU,
        posts = ''.join(sml.write(pl) for pl in post_links),
    )

    with open(target_blog_filename, 'w') as target_blog_file:
        target_blog_file.write(html)
