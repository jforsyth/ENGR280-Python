from collections import deque


class HeartbeatQueue():
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if HeartbeatQueue.__instance == None:
            HeartbeatQueue()
        return HeartbeatQueue.__instance

    def __init__(self):
        if HeartbeatQueue.__instance != None:
           raise Exception("This class is a singleton!")
        else:
            HeartbeatQueue.__instance = self
            self.__queue = deque()

    def push(self, item):
        self.__queue.append(item)

    def pop(self):
        return self.__queue.popleft() 

    def is_empty(self):
        if len(self.__queue) > 0:
            return False
        else:
            return True

if __name__ == "__main__":
    hbq = HeartbeatQueue()
    hbq.push(1)
    print(hbq.is_empty())
