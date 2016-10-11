from .renderer import box_triangles, tile_triangles
class Block:
    """Block class
    """
    def __init__(self,
            block_id=-1, block_type="block", color=(100,0,100), indicator="?",
            name="unknown", movable=False):
        """Constructor
        """
        self.block_id = block_id
        self.block_type = block_type
        self.color = color
        self.indicator = indicator
        self.name = name
        self.movable = movable

def block_to_triangles(block, pos):
    '''Make triangles of a block(i.e. box or tile with position)

    Args:
        block (list of three floats): block to be converted
        pos (list of three floats): block position

    Returns:
        tuple of triangles and colors
    '''
    assert isinstance(block, Block)
    if block.block_type == "block":
        triangles, colors = box_triangles(block.color)
    elif block.block_type == "tile":
        triangles, colors = tile_triangles(block.color)
    return triangles+(pos[0], pos[1], 0), colors
