import os

import menu
import post
import sml
import template

def get_posts(posts_src_dir):
    post_filenames = [fn for fn in os.listdir(posts_src_dir) if fn.endswith('.post')]

    for post_filename in post_filenames:
        post_path = os.path.join(posts_src_dir, post_filename)
        yield post.from_file(
            post_path,
        )

def generate(posts_src_dir, posts_target_dir):
    post_list = get_posts(posts_src_dir)
    
    post_list = list(filter(lambda p: p.published != None, post_list))

    post_list = list(sorted(
        post_list,
        key = lambda p: p.published,
        reverse = True,
    ))

    if len(post_list) > 0:
        first_post = post_list[0]
        last_post = post_list[-1]

    else:
        first_post = None
        last_post = None
        
    first_posts = [None] + ([first_post] * (len(post_list) - 1))
    previous_posts = [None] + post_list[:-1]
    next_posts = post_list[1:] + [None]
    last_posts = ([last_post] * (len(post_list) - 1)) + [None]

    zipped = zip(first_posts, previous_posts, post_list, next_posts, last_posts)

    for first_p, prev_p, p, next_p, last_p in zipped:
        post_target_path = os.path.join(posts_target_dir, p.link_filename)
        traversal_links = post.get_traversal_links(first_p, prev_p, next_p, last_p)

        with open(post_target_path, 'w') as f:
            f.write(template.apply_base_template(
                p.title,
                p.authors,
                p.keywords,
                p.description,
                post.to_html(p, menu.MENU, traversal_links),
            ))
        
        yield post.filename_to_link(p.link_filename, p)
