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
