class A:
    def process(self):
        print("A.process() called")

class B(A):
    def process(self):
        print("B.process() called")
        super().process()

class C(A):
    def process(self):
        print("C.process() called")
        super().process()

class D(B, C):
    def process(self):
        print("D.process() called")
        super().process()

obj = D()
obj.process()


print("\nMRO for class D:")
for cls in D.mro():
    print(cls)
