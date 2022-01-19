class Dog:
    def __init__(self, func):
        self.age = 10
        self.talent = func

    def bark(self):
        print("Bark !!!")

@Dog
def dog_can_pee():
    print("I can pee very hard......")



if __name__ == "__main__":
    dog = dog_can_pee       # equals to "dog = DOG(dog_can_pee)" with no decorator @Dog 

    print(dog.age)
    # > 10

    dog.bark()
    # > Bark !!!

    dog.talent()
    # > I can pee very hard......
