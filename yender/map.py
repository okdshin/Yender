import copy
from .block import Block

class Map:
    '''Map class

    Args:
        size (tuple of two int): size
        data (list of Block): block list
    '''

    def __init__(self, size=(3, 3), data=[Block() for _ in range(3*3)]):
        self.size = size
        self.data = data

    def _index(self, pos):
        # x + y*w
        return pos[1] + pos[0]*self.size[1]

    def get_block(self, pos):
        '''Getter

        Args:
            pos (tuple of two ints): target block position

        Returns:
            Block: corresponding block
        '''
        return self.data[self._index(pos)]

    def safe_get_block(self, pos, default_block):
        '''Getter (safe version)

        This function returns default_block if pos is out of area.

        Args:
            pos (tuple of two ints): target block position
            default_block (Block): default block when pos is out of area

        Returns:
            Block: corresponding block or default_block
        '''
        if pos[0] < 0 or self.size[0] <= pos[0] or pos[1] < 0 or self.size[1] <= pos[1]:
            return default_block
        return self.get_block(pos)

    def set_block(self, pos, block):
        '''Setter

        Args:
            pos (tuple of two ints): target block position
            block (~yender.Block): block to be set

        Returns:
            None: None
        '''
        assert isinstance(block, Block)
        self.data[self._index(pos)] = copy.copy(block)

    def print(self):
        for y in range(self.size[0]):
            for x in range(self.size[1]):
                indicator = self.get_block((y, x)).indicator
                print(indicator, end="")
            print()


def load_map(block_set, block_list):
    '''load map from source
    #TODO

    Args:
        block_set (dict of (indicator, Block)): block set included in map
        block_list (list of str): source of map

    Returns:
        tuple of Map and positions: loaded map and annotated positions
    '''
    data = []
    positions = {}
    for y, line in enumerate(block_list):
        for x, block in enumerate(line):
            if block in [str(i) for i in range(10)]:
                positions[block] = (y, x)
                data.append(Block())
            else:
                data.append(copy.copy(block_set[block]))
    size = (len(block_list), len(block_list[0]))
    return Map(size, data), positions
