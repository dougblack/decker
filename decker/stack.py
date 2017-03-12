class Stack(object):
    @classmethod
    def transform(cls, x, y, z, faceup, scale):
        return {
            'posX': 2.5,
            'posY': 2.5,
            'posZ': 3.5,
            'rotX': 0,
            'rotY': 180,
            'rotZ': 0 if faceup else 180,
            'scaleX': scale,
            'scaleY': scale,
            'scaleZ': scale,
        }


class Mainboard(Stack):
    name = 'Mainboard'
    position = Stack.transform(1, 1, 0, False, 1)


class Commander(Stack):
    name = 'Commander'
    position = Stack.transform(-3, 1, -2, True, 1)


class Tokens(Stack):
    name = 'Tokens'
    position = Stack.transform(-3, 1, -2, False, 1)


class Sideboard(Stack):
    name = 'Sideboard'
    position = Stack.transform(2, 1, 0, False, 1)
