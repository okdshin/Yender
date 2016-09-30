class Block:
    def __init__(self,
            block_id=-1, block_type="block", color=(100,0,100), indicator="?",
            name="unknown", movable=False):
        self.block_id = block_id
        self.block_type = block_type
        self.color = color
        self.indicator = indicator
        self.name = name
        self.movable = movable
