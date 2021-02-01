def raise_if_false(predicate, message):
    if not predicate:
        raise RuntimeError(message)

def raise_if_true(predicate, message):
    if predicate:
        raise RuntimeError(message)