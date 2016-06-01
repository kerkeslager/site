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
        newest_post = post_list[0]
        oldest_post = post_list[-1]

    else:
        newest_post = None
        oldest_post = None
        
    oldest_post_list = ([oldest_post] * (len(post_list) - 1)) + [None]
    previous_post_list = post_list[1:] + [None]
    next_post_list = [None] + post_list[:-1]
    newest_post_list = [None] + ([newest_post] * (len(post_list) - 1))

    zipped = zip(
        oldest_post_list,
        previous_post_list,
        post_list,
        next_post_list,
        newest_post_list,
    )

    for oldest_post, previous_post, current_post, next_post, newest_post in zipped:
        post_target_path = os.path.join(posts_target_dir, current_post.link_filename)
        traversal_links = post.get_traversal_links(
            oldest_post,
            previous_post,
            next_post,
            newest_post,
        )

        with open(post_target_path, 'w') as f:
            f.write(template.apply_base_template(
                current_post.title,
                current_post.authors,
                current_post.keywords,
                current_post.description,
                post.to_html(current_post, menu.MENU, traversal_links),
            ))
        
        yield post.filename_to_link(current_post.link_filename, current_post)
