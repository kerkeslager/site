import collections
import string

import footnotes
import functional
import sml

Post = collections.namedtuple('Post', ['title','authors','body'])

def is_node_with_tag(node, tag):
    return isinstance(node, sml.Node) and node.tag == tag

def is_title(node):
    return is_node_with_tag(node, 'title')

def is_author(node):
    return is_node_with_tag(node, 'author')

def is_body(node):
    return is_node_with_tag(node, 'body')

def from_sml(s):
    tree = sml.read(s)

    assert tree.tag == 'post'

    title = functional.find(is_title, tree.children).children[0]
    authors = [a.children[0] for a in filter(is_author, tree.children)]
    body = functional.find(is_body, tree.children)

    return Post(
        title = title,
        authors = authors,
        body = body,
    )
    
def from_file(filename):
    with open(filename, 'r') as f:
        return from_sml(f.read())

with open('templates/post.html','r') as post_template_file:
    POST_TEMPLATE = string.Template(post_template_file.read())

def comma_separated_list(xs):
    if len(xs) == 1:
        return xs[0]

    if len(xs) == 2:
        return '{} and {}'.format(xs[0], xs[1])

    if len(xs) > 2:
        return '{}, and {}'.format(', '.join(xs[:-1], xs[-1]))

    raise Exception()

def to_html(post, menu):
    body_nodes, footnote_nodes = footnotes.extract_footnotes(post.body)

    body_html = ''.join(sml.write(body_node) for body_node in body_nodes.children)
    footnote_html = ''.join(sml.write(fn) for fn in footnote_nodes)

    return POST_TEMPLATE.substitute(
        title = post.title,
        author = comma_separated_list(post.authors),
        body = body_html,
        footnotes = footnote_html,
        menu = menu,
    )
