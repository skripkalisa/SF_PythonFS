class Cat:
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def get_cat(self):
        return f'This is {self.name}, it\'s a {self.gender}, {str(self.age)} years old'


class Dog(Cat):
    def get_pet(self):
        return f'{self.name} {self.age}'
