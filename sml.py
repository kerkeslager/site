import collections
import re

_OpenTag = collections.namedtuple('_OpenTag', ['tag', 'attributes'])
Node = collections.namedtuple('Node', ['tag','attributes','children'])

attribute_matcher = r'''(?P<key>[a-z]+)\s*=\s*(?P<value>'[^']*'|"[^"]*")'''
tag_matcher = r'<\s*(?P<pre_slash>/)?\s*(?P<tag>[a-z]+)(?P<attributes>(\s+{})*)\s*(?P<post_slash>/)?\s*>'.format(attribute_matcher)

attribute_matcher = re.compile(attribute_matcher)
tag_matcher = re.compile(tag_matcher)

def read(s):
    pointer = 0
    stack = []
    buff = []

    for match in tag_matcher.finditer(s):
        text = s[pointer:match.start()]

        if len(text.strip()) > 0:
            buff.append(text)

        pointer = match.end()

        if match.group('post_slash') != None:
            assert match.group('pre_slash') == None

            attributes = {}
            for attribute_match in attribute_matcher.finditer(match.group('attributes')):
                key = attribute_match.group('key')
                value = attribute_match.group('value')
                
                assert key not in attributes
                attributes[key] = value[1:-1]

            buff.append(Node(
                tag = match.group('tag'),
                attributes = attributes,
                children = [],
            ))

        elif match.group('pre_slash') != None:
            assert match.group('attributes') == '' 

            open_tag = stack[-1].pop()
            assert open_tag.tag == match.group('tag')
            stack[-1].append(Node(
                tag = open_tag.tag,
                attributes = open_tag.attributes,
                children = buff,
            ))

            buff = stack.pop()

        else:
            attributes = {}
            for attribute_match in attribute_matcher.finditer(match.group('attributes')):
                key = attribute_match.group('key')
                value = attribute_match.group('value')
                
                assert key not in attributes
                attributes[key] = value[1:-1]

            buff.append(_OpenTag(
                tag = match.group('tag'),
                attributes = attributes,
            ))
            stack.append(buff)
            buff = []

    assert len(stack) == 0
    assert len(buff) == 1
    assert isinstance(buff[0], Node)
    return buff[0]

def write(n):
    assert isinstance(n, Node) or isinstance(n, str)
    if isinstance(n, str):
        return n

    attributes = ''
    for k,v in n.attributes.items():
        if '"' in v:
            if "'" in v:
                raise Exception()

            v = "'{}'".format(v)

        else:
            v = '"{}"'.format(v)

        attributes += ' {}={}'.format(k,v)

    if len(n.children) == 0:
        return '<{}{}/>'.format(n.tag, attributes)

    return '<{}{}>{}</{}>'.format(
        n.tag,
        attributes,
        ''.join(write(c) for c in n.children),
        n.tag,
    )

if __name__ == '__main__':
    import unittest

    class TestRead(unittest.TestCase):
        def test_reads_simple_tag(self):
            result = read('<simple/>')

            self.assertEqual(result.tag, 'simple')
            self.assertEqual(result.attributes, {})
            self.assertEqual(result.children, [])

        def test_reads_empty_tag(self):
            result = read('<empty></empty>')

            self.assertEqual(result.tag, 'empty')
            self.assertEqual(result.attributes, {})
            self.assertEqual(result.children, [])

        def test_reads_tag_with_text_child(self):
            result = read('<hello>Hello, world</hello>')

            self.assertEqual(result.tag, 'hello')
            self.assertEqual(result.attributes, {})
            self.assertEqual(result.children, ['Hello, world'])

        def test_reads_simple_tag_with_attributes(self):
            result = read('<simple key="value"/>')

            self.assertEqual(result.tag, 'simple')
            self.assertEqual(result.attributes, {'key': 'value'})
            self.assertEqual(result.children, [])

        def test_reads_open_tag_with_attributes(self):
            result = read('<empty key="value"></empty>')

            self.assertEqual(result.tag, 'empty')
            self.assertEqual(result.attributes, {'key': 'value'})
            self.assertEqual(result.children, [])

    class TestWrite(unittest.TestCase):
        def test_writes_simple_tag(self):
            self.assertEqual(
                write(Node(
                    tag = 'simple',
                    attributes = {'key': 'value'},
                    children = [],
                )),
                '<simple key="value"/>',
            )

        def test_writes_tag_with_content(self):
            self.assertEqual(
                write(Node(
                    tag = 'content',
                    attributes = {'key': 'value'},
                    children = ['Hello',Node(tag='world',attributes={},children=[])],
                )),
                '<content key="value">Hello<world/></content>',
            )

    unittest.main()
