class NCS:
    def __init__(self, name, *args):
        self.__name = name
        self.__obj_list = list(args)

    def get(self):
        return self.__obj_list

    def append(self, val):
        return self.__obj_list.append(val)

    def len(self):
        return len(self.__obj_list)

    def __str__(self):
        return str(len(self.__obj_list))

    def __repr__(self) -> str:
        return str(len(self.__obj_list))
