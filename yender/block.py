from .renderer import box_triangles, tile_triangles
class Block:
    """Block class
    """
    def __init__(self,
            char,
            block_type="block", color=(100,0,100),
            name="unknown", movable=True, visible=True):
        """Constructor
        """
        self.block_type = block_type
        self.color = color
        self.char = char
        self.name = name
        self.movable = movable
        self.visible = visible

