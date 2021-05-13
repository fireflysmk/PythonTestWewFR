from factory_method import Cat, Dog

animal_type = input()

if animal_type == 'dog':
    animal = Dog()
elif animal_type == 'cat':
    animal = Cat()

animal.say()



