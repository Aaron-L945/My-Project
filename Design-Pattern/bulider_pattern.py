# 三个类，第一个物品类，第二个建造者，第三个指挥者

class Ice_Cream():
    def __init__(self):
        self.color = None
        self.shape = None
        self.taste = None

    def __str__(self):
        return "%s%s%s冰淇淋做好了！" % (self.color, self.shape, self.taste)


class Bulider():

    def __init__(self):
        self.ice_cream = Ice_Cream()

    def create_color(self, color):
        self.ice_cream.color = color

    def create_shape(self, shape):
        self.ice_cream.shape = shape

    def crete_taste(self, taste):
        self.ice_cream.taste = taste


class Handler():
    def __init__(self):
        self.bulider = None

    def create_ice_cream(self, color, shape, taste):
        self.bulider = Bulider()
        (step for step in
         (self.bulider.create_color(color), self.bulider.create_shape(shape), self.bulider.crete_taste(taste)))

    @property
    def _ice_cream(self):
        return self.bulider.ice_cream


def main():
    hander = Handler()
    hander.create_ice_cream("红色", "大杯", "草莓味")
    ice_cream = hander._ice_cream
    print(ice_cream)


if __name__ == '__main__':
    main()
