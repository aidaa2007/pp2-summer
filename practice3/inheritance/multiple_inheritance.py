class Flyable:

    def fly(self):
        print("Can fly")


class Swimmable:

    def swim(self):
        print("Can swim")


class Duck(Flyable, Swimmable):
    pass


duck = Duck()

duck.fly()
duck.swim()