#! usr/bin/env python3

def enum(**enums):
    return type('Enum', (), enums)
