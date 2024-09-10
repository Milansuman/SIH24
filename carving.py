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
    "ZIP": (
        b'\x50\x4B\x03\x04',
    ),
    "HTML": (
        b'<html>',
        b'<!DOCTYPE html>',
        b'<!doctype html>'
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

class PNGExtractor:
    def __init__(self, partial_data):
        self.data = partial_data
        self.possible_ends = []

        for match in re.finditer(b'\x49\x45\x4e\x44\xae\x42\x60\x82', partial_data):
            self.possible_ends.append(match.start())

        print(self.possible_ends)

    def extract_file(self, path):
        with open(path, "wb") as file:
            file.write(self.data[:self.possible_ends[0]]+8)


class ZIPExtractor:
    def __init__(self, partial_data):
        self.data = partial_data
        self.possible_ends = []

        for match in re.finditer(b'\x50\x4B\x05\x06', partial_data):
            self.possible_ends.append(match.start())

        print(self.possible_ends)
    
    def extract_file(self, path):
        if self.possible_ends:
            with open(path, "wb") as file:
                # Write data up to and including the End of Central Directory record
                file.write(self.data[:self.possible_ends[-1] + 22])
        else:
            print("No valid ZIP end structure found")
        
class HTMLExtractor:
    def __init__(self, partial_data):
        self.data = partial_data
        self.possible_ends = []

        for match in re.finditer(b'</html>', partial_data):
            self.possible_ends.append(match.start())

        print(self.possible_ends)
    
    def extract_file(self, path):
        if self.possible_ends:
            with open(path, "wb") as file:
                # Write data up to and including the End of Central Directory record
                file.write(self.data[:self.possible_ends[-1] + 22])
        else:
            print("No valid ZIP end structure found")

class Carver:
    def __init__(self, path):
        self.path = path
        self.data = b''
        self.indexes = []
        self.readData()
    
    def readData(self):
        with open(self.path, "rb") as file:
            self.data = file.read()
    
    def extractFiles(self):
        for file_type in magic_nums:
            for byte_string in magic_nums[file_type]:
                try:
                    for match in re.finditer(byte_string, self.data):
                        print(f"{file_type}: {match.start()}")

                        # if file_type == "JPG":
                        #     jpg_extractor = JPGExtractor(self.data[match.start():])
                        #     jpg_extractor.extract_file(f"extracted_{match.start()}.jpg")
                        # elif file_type == "ZIP":
                        #     zip_extractor = ZIPExtractor(self.data[match.start():])
                        #     zip_extractor.extract_file(f"extracted_{match.start()}.zip")
                except Exception as e:
                    print("Unexpected error occurred.")
