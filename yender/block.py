from .renderer import box_triangles, tile_triangles
class Block:
    """Block class
    """
    def __init__(self,
            block_type="block", color=(100,0,100), indicator="?",
            name="unknown", movable=False):
        """Constructor
        """
        self.block_type = block_type
        self.color = color
        self.indicator = indicator
        self.name = name
        self.movable = movable

