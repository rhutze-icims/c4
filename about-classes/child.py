class Child:

    name = None
    age = None

    def __init__(self, name):
        self.name = name

    def set_age(self, age):
        self.age = age

    def __str__(self):
        return "My name is %s and I am %d years old." % (self.name, self.age)

