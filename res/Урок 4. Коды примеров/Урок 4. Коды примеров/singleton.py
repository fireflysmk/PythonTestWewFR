class Origin:
    pass

o1 = Origin()
o2 = Origin()  # либо запрещено, либо возвращает ссылку на уже созданный экземпляр

print(o1)
print(o2)

print(o1 is o2)  # -> True или False

a = []
b = a
print(a is b)  # -> True или False

b = a.copy()
print(a is b)
