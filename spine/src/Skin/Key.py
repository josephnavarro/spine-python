class Key(object):
    def __init__(self, slotIndex, name):
        super(Key, self).__init__()
        self.slotIndex = slotIndex
        self.name = name

    def __lt__(self, key):
        if self.slotIndex == key.slotIndex:
            return self.name < key.name
        return self.slotIndex < key.slotIndex

    def __hash__(self):
        return hash((self.slotIndex, self.name))

    def __eq__(self, other):
        return (self.slotIndex, self.name) == (other.slotIndex, other.name)