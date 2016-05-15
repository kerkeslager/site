import os

import menu
import post
import sml
import template

def generate(posts_src_dir, posts_target_dir):
    post_filenames = [fn for fn in os.listdir(posts_src_dir) if fn.endswith('.post')]

    post_instances_and_target_filenames = []

    for post_filename in post_filenames:
        post_path = os.path.join(posts_src_dir, post_filename)
        p = post.from_file(post_path)
        
        if p.published == None:
            continue
        
        post_instances_and_target_filenames.append(p)

    post_instances_and_target_paths = list(sorted(
        post_instances_and_target_filenames,
        key = lambda piatp: piatp.published,
        reverse = True,
    ))

    post_links = []

    for p in post_instances_and_target_paths:
        post_target_path = os.path.join(posts_target_dir, p.link_filename)
        with open(post_target_path, 'w') as f:
            f.write(template.apply_base_template(
                p.title,
                p.authors,
                p.keywords,
                p.description,
                post.to_html(p, menu.MENU),
            ))
        
        post_links.append(post.filename_to_link(p.link_filename, p))

    return post_links
