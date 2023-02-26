#! usr/bin/env python3

def enum(**enums) -> type:
    """
    For dynamic definition of an enumerated type.

    :param enums: Name and value pairs, e.g. cat=0, dog=1, etc.

    :return:
    """
    return type("Enum", (), enums)
