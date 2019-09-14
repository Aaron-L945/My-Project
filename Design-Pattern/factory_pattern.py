class Cars(object):
    BMW_cars = ["宝马999", "宝马101"]
    AUTO_cars = ["奥迪400", "奥迪600"]
    BC_cars = ["奔弛1000", "奔弛800"]
    Red_flag = ["红旗500"]


def Factory(name, color):
    if name in Cars.BMW_cars:
        factory = BMW_Factory

    elif name in Cars.AUTO_cars:
        factory = AUTO_Factory

    else:
        raise ValueError("The car not found in FoursStore! ")
    return factory(name, color)


def FactoryStore(name, color):
    factory = None
    try:
        factory = Factory(name, color)
    except Exception as e:
        print(e)
    return factory


class BMW_Factory(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __str__(self):
        return "这是一辆%s,%s的车" % (self.name, self.color)


class AUTO_Factory(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __str__(self):
        return "这是一辆%s,%s的车" % (self.name, self.color)


class BC_Factory(object):
    pass


class RedFlagFactory(object):
    pass


car = FactoryStore("宝马999", "黑色")
print(car)
# car.get_car_from_cars_factory()
