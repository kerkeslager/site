def find(predicate, xs):
    for x in xs:
        if predicate(x):
            return x

    raise Exception('No item found matching predicate')
