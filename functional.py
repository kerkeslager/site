_sentinel = object()

def find(predicate, xs, default = _sentinel):
    for x in xs:
        if predicate(x):
            return x

    if default == _sentinel:
        raise Exception('No item found matching predicate')

    return default
