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
        
        target_post_filename = post_filename[:-4] + 'html'
        
        post_instances_and_target_filenames.append((p, target_post_filename))

    post_instances_and_target_paths = list(sorted(
        post_instances_and_target_filenames,
        key = lambda piatp: piatp[0].published,
        reverse = True,
    ))

    post_links = []

    for p, target_post_filename in post_instances_and_target_paths:
        post_target_path = os.path.join(posts_target_dir, target_post_filename)
        with open(post_target_path, 'w') as f:
            f.write(template.apply_base_template(
                p.title,
                p.authors,
                p.keywords,
                p.description,
                post.to_html(p, menu.MENU),
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

    return post_links
