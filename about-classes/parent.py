from child import Child

class Parent:

    def __init__(self):
        self.child1 = Child('Tammy')
        self.child1.set_age(12)

        self.child2 = Child('Arthur')
        self.child2.set_age(8)

    def print_children(self):
        print(self.child1)
        print(self.child2)

