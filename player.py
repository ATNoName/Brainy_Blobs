import enum
import neural_network as nn

# Get all inputs for the player before implement ANN

class Direction(enum.Enum):
    North = 1
    East = 2
    South = 3
    West = 4

class Player:
    def __init__(self, id, colour=(0,0,0), x=-1, y=-1, length = 0, width = 0):
        self.id = id
        self.colour = colour
        self.baseX = x
        self.baseY = y
        self.blob_location = list((x,y)) # location of all blobs
        self.bignet = nn.NeuralNetwork(length*width, length*width, 3, length*width)
        self.bignet.randomize_weight()
        self.smallnet = nn.NeuralNetwork(length*width+2, length*width, 1, 5)
        self.smallnet.randomize_weight()
        
    def set_ann(self, bignet: nn.NeuralNetwork, smallnet: nn.NeuralNetwork):
        self.bignet = bignet
        self.smallnet = smallnet

    def get_base(self):
        """
        Get the location of the player's base
        """
        return (self.baseX, self.baseY)
    
    def get_colour(self) -> tuple[int]:
        return self.colour
    
    def move_blob(self, direction: Direction, number=0, x=0, y=0):
        """
        The player input for a blob army in that area. Used for process_movement
        Argument: direction: which direction to go
                  number: how many blobs to sent to
                  x: the x coordinate of a particular blob
                  y: the y coordinate of a particular blob
                  return: the input set for process movement
        """
        target = tuple()
        if direction == Direction.North:
            target = (x, y-1)
        elif direction == Direction.East:
            target = (x+1, y)
        elif direction == Direction.South:
            target = (x, y+1)
        else:
            target = (x-1,y)
        return ((x,y), number, target)
