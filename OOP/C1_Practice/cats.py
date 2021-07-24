from cat import Cat, Dog

cat1 = Cat('Baron', 'male', 2)
cat2 = Cat('Sam', 'male', 2)
cat3 = Cat('Linda', 'female', 3)

dog = Dog('Wolf', 'male', 5)
print(cat1.get_cat())
print(cat2.get_cat())
print(cat3.get_cat())

print(dog.get_pet())
