"""
FILE CARVING MODULE
"""
import re

magic_nums = {
    "JPG": (
        b'\xFF\xD8\xFF\xD8',
        b'\xFF\xD8\xFF\xE0', 
        b'\xFF\xD8\xFF\xE1'
        b'\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00\x01'
    ),
    "PNG": (
        b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A',
    ), 
    "GIF": (
        b'GIF87a',
        b'GIF89a',
    )

}

class JPGExtractor:
    def __init__(self, partial_data):
        self.data = partial_data
        self.possible_ends = []

        for match in re.finditer(b'\xFF\xD9', partial_data):
            self.possible_ends.append(match.start())

        print(self.possible_ends)
    
    def extract_file(self, path):
        with open(path, "wb") as file:
            file.write(self.data[:self.possible_ends[0]])

class GIFExtractor:
    def __init__(self, partial_data):
        self.data = partial_data
        self.possible_ends = []

        for match in re.finditer(b'\x00\x3B', partial_data):  # GIF file terminator
            self.possible_ends.append(match.start() + 2)  # Include the terminator

        print(self.possible_ends)
    
    def extract_file(self, path):
        if self.possible_ends:
            with open(path, "wb") as file:
                file.write(self.data[:self.possible_ends[-1]])
        else:
            print("No valid GIF end marker found.")
        
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
                try:
                    for match in re.finditer(byte_string, self.data):
                        print(f"{file_type}: {match.start()}")

                        if file_type == "JPG":
                            jpg_extractor = JPGExtractor(self.data[match.start():])
                            jpg_extractor.extract_file("test.jpg")
                except Exception as e:
                    print("Unexpected error occurred.")

with open('test.gif','rb') as file:
    zip_extractors = GIFExtractor(file.read())
    zip_extractors.extract_file('recover.gif')
            
