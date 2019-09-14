
class SingleUser(object):
    __instance = None
    def __init__(self,name):
        self.name = name

    def __new__(cls,name):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

s1 = SingleUser("zs")
print(s1.name)
s2 = SingleUser("ls")

print(s1 is s2)
print(s1 == s2)

print(s1)
print(s2)

print(s1.name)
print(s2.name)

