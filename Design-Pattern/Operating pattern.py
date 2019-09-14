from abc import ABCMeta, abstractmethod
from enum import Enum


class State(Enum):
    new = 0
    running = 1
    sleeping = 2
    restart = 3
    zombie = 4


class User:
    pass


class Process:
    pass


class File:
    pass


class Server(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    def __str__(self):
        return self.name

    @abstractmethod
    def boot(self):
        pass

    @abstractmethod
    def kill(self, result=True):
        pass


class FileServer(Server):
    def __init__(self):
        self.name = "FileServer"
        self.state = State.new

    def boot(self):
        print("FileServer is Running!")

    def kill(self, result=True):
        pass

    def create_file(self, filename, path):
        return "Create {} in {}".format(filename, path)


class ProcessServer(Server):
    def __init__(self):
        self.name = "ProcessServer"
        self.state = State.new

    def boot(self):
        print("ProcessServer is Running!")

    def kill(self, result=True):
        pass

    def create_process(self, name, user):
        return "Create process {} for user {}".format(name, user)


class OperatingSystem:
    def __init__(self):
        self.file = FileServer()
        self.process = ProcessServer()

    def boot(self):
        [i.boot() for i in (self.file, self.process)]

    def create_file(self, filename, path):
        return self.file.create_file(filename, path)

    def create_process(self, name, user):
        return self.process.create_process(name, user)


def main():
    operating = OperatingSystem()
    operating.boot()
    file = operating.create_file("lxy", "./")
    process = operating.create_process("lxy", "admin")
    print(file)
    print(process)


if __name__ == '__main__':
    main()
