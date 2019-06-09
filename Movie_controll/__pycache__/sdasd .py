name = input("")
passwd = int(input(""))
userid = int(input(''))

d = 's {} {} {}'.format(name,passwd,userid)
b = d.split(" ")
print(b)