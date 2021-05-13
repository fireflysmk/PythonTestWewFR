from factory_method_4 import create_animal

animal_type = input()
animal = create_animal(animal_type)
animal.say()
