import sml

def extract_footnotes(node, wrapped_counter = None):
    assert isinstance(node, str) or isinstance(node, sml.Node)
    if wrapped_counter == None:
        wrapped_counter = [0]

    if isinstance(node, str):
        return node, []

    if node.tag == 'footnote':
        footnote_ref = 'footnote-{}'.format(wrapped_counter[0])
        back_ref = 'backref-{}'.format(wrapped_counter[0])
        wrapped_counter[0] += 1

        return (sml.Node(
            tag = 'sup',
            attributes = {'id': back_ref},
            children = [
                sml.Node(
                    tag = 'a',
                    attributes = {'href': '#{}'.format(footnote_ref)},
                    children = ['[', str(wrapped_counter[0]), ']'],
                )
            ],
        ), [sml.Node(
            tag = 'p',
            attributes = {'id': footnote_ref},
            children = [
                sml.Node(
                    tag = 'a',
                    attributes = {'href': '#{}'.format(back_ref)},
                    children = ['[',str(wrapped_counter[0]), ']'],
                ),
                ' '
            ] + node.children,
        )])

    children = []
    footnotes = []

    for child in node.children:
        child_node, child_footnotes = extract_footnotes(child, wrapped_counter)
        children.append(child_node)
        footnotes += child_footnotes

    return (
        sml.Node(
            tag = node.tag,
            attributes = node.attributes,
            children = children,
        ),
        footnotes,
    )
