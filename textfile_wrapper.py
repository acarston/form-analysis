import ctypes

# change according to your workspace directory
lib = ctypes.CDLL('./textfile.dll')

class TextFile:
    def __init__(self) -> None:
        # set the functions' argument, return types
        lib.CTextFileDefault.argtypes = [ctypes.c_void_p]
        lib.CTextFileDefault.restype = ctypes.c_void_p

        lib.c_set_input.argtypes = [ctypes.c_void_p]
        lib.c_set_input.restype = ctypes.c_void_p

        lib.c_parse_into_tree.argtypes = [ctypes.c_void_p]
        lib.c_parse_into_tree.restype = ctypes.c_void_p

        lib.c_print_words.argtypes = [ctypes.c_void_p]
        lib.c_print_words.restype = ctypes.c_void_p

        # call the C constructor
        self.obj = lib.CTextFileDefault(None)

    # function wrappers
    def set_input(self, input: str, person: str) -> None:
        lib.c_set_input(self.obj, input, person)
        
    def parse_into_tree(self) -> None:
        lib.c_parse_into_tree(self.obj)

    def print_words(self, filePath: str) -> None:
        lib.c_print_words(self.obj, filePath)

def driver():
    textFile = TextFile()
    textFile.set_input('something in the way', 'Aaron')
    textFile.parse_into_tree()
    textFile.print_words('./out.txt')