"""
FILE CARVING MODULE
"""

magic_nums = {
    "JPG": (
        b'\xFF\xD8\xFF\xD8',
        b'\xFF\xD8\xFF\xE0', 
        b'\xFF\xD8\xFF\xE1'
        b'\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00\x01'
    )
}

class Carver:
    def __init__(self, path):
        self.path = path
        self.data = b''
        self.indexes = []
    
    def readData(self):
        with open(self.path, "rb") as file:
            self.data = file.read()
    
    def findOffsets(self):
        for file_type in magic_nums:
            for byte_string in magic_nums[file_type]:
                print(self.data.find(byte_string))
            
carver = Carver("../test.iso")
carver.readData()
carver.findOffsets()