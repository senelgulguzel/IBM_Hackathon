class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self):
        super().__init__("Dog")

dog = Dog()
print(dog.name) 