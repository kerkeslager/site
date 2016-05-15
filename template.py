import os.path
import string

current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')

def get_template(path):
    with open(path, 'r') as f:
        return string.Template(f.read())

BASE_TEMPLATE = get_template(os.path.join(template_dir, 'base.html'))
def apply_base_template(title, authors, keywords, description, body):
    return BASE_TEMPLATE.substitute(
        title = title,
        authors = ','.join(authors),
        keywords = ','.join(keywords),
        description = description,
        body = body,
    )
