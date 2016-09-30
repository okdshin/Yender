import copy
from .block import Block

class Map:
    def __init__(self, size=(10, 10), data=[Block() for _ in range(100)]):
        self.size = size
        self.data = data

    def _index(self, pos):
        # x + y*w
        return pos[1] + pos[0]*self.size[1]

    def get_block(self, pos):
        return self.data[self._index(pos)]

    def set_block(self, pos, block):
        isinstance(block, Block)
        self.data[self._index(pos)] = copy.copy(block)

    def print(self):
        for y in range(self.size[0]):
            for x in range(self.size[1]):
                indicator = self.get_block((y, x)).indicator
                print(indicator, end="")
            print()


def load_map(block_set, block_list):
    data = []
    positions = [None for _ in range(10)]
    for y, line in enumerate(block_list):
        for x, block in enumerate(line):
            if block in [str(i) for i in range(10)]:
                positions[int(block)] = (y, x)
                data.append(Block())
            else:
                data.append(copy.copy(block_set[block]))
    size = (len(block_list), len(block_list[0]))
    while positions[-1] == None:
        positions.pop()
    return (size, data), positions
