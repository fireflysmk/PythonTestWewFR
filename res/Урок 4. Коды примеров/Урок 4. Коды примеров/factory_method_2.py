import abc


class Animal(abc.ABC):

    @abc.abstractmethod
    def say(self):
        pass



class Dog(Animal):

    def say(self):
        print('wow-wow')


class Cat(Animal):

    def say(self):
        print('мяу-мяу')


class Bird(Animal):

    def say(self):
        print('мяу-мяу')


class AnimalCreator:

    @staticmethod
    def create_animal(animal_type):
        if animal_type == 'dog':
            animal = Dog()
        elif animal_type == 'cat':
            animal = Cat()
        elif animal_type == 'bird':
            animal = Cat()

        return animal