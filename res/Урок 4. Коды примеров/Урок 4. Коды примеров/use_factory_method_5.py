from factory_method_5 import ANIMALS

animal_type = input()
animal = ANIMALS[animal_type]()
animal.say()
