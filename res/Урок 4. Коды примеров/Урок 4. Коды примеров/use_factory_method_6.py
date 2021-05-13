from factory_method_6 import Animal

animal_type = input()
animal = Animal.create_animal(animal_type)
animal.say()
