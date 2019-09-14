import copy
from collections import OrderedDict


class Book:
    def __init__(self, name, author, price, **rest):
        self.name = name
        self.author = author
        self.price = price
        self.__dict__.update(rest)

    def __str__(self):
        mylist = []
        ordered = OrderedDict(sorted(self.__dict__.items()))
        for item in ordered.keys():
            mylist.append('{}:{}'.format(item, ordered[item]))
            if item == "price":
                mylist.append("$")
            mylist.append("\n")
        return "".join(mylist)


class ProtoType:
    def __init__(self):
        self.object = dict()

    def register(self, key, value):
        self.object[key] = value

    def unregister(self, key):
        del self.object[key]

    def clone(self, key, **attr):
        found = self.object.get(key)
        if not found:
            raise ValueError("Not found key from dict")
        obj = copy.deepcopy(found)
        obj.__dict__.update(attr)
        return obj


def main():
    b1 = Book('The C Programming Language', ('Brian W. Kernighan', 'Dennis M.Ritchie'),
              price=118, publisher='Prentice Hall', length=228, publication_date='1978-02-22',
              tags=('C', 'programming', 'algorithms', 'data structures'))
    prototype = ProtoType()
    print(b1)
    cid = 'k&r-first'
    prototype.register(cid, b1)
    b2 = prototype.clone(cid, name='The C Programming Language(ANSI)', price=48.99,
                         length=274, publication_date='1988-04-01', edition=2)
    print(b2)
    for i in (b1, b2):
        # print(i)
        pass
    print("ID b1 : {} != ID b2 : {}".format(id(b1), id(b2)))


if __name__ == '__main__':
    main()
