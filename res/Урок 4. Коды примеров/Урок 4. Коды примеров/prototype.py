import copy


class Original:
    pass


original = Original()
prototype = copy.deepcopy(original)


prototype.name = 2
