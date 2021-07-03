class Endpoint:
    def __init__(self, which_endpoint, color, x,y, complete_bool):
        self.whichendpoint = which_endpoint
        self.color = color
        self.position = tuple(x,y)
        self.complete = complete_bool

    def movePosition(self, x, y):
        L1 = list(self.position)
        L1[0] = L1[0] + x
        L1[1] = L1[1] + y
        self.position = tuple(L1)

