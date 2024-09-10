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
    "HTML": (
        b'<html>',
        b'<!DOCTYPE html>',
        b'<!doctype html>'
    ),
     "PDF": (
        b'%PDF-',
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
        
class HTMLExtractor:
    def __init__(self, partial_data):
        self.data = partial_data
        self.possible_ends = []

        for match in re.finditer(b'</html>', partial_data):
            self.possible_ends.append(match.start())

        print(self.possible_ends)
    
    def extract_file(self, path):
        with open(path, "wb") as file:
            file.write(self.data[:self.possible_ends[0]+7])

class PDFExtractor:
    def __init__(self, partial_data):
        self.data = partial_data
        self.possible_ends = []

        for match in re.finditer(b'%%EOF', partial_data):
            self.possible_ends.append(match.start())

        print(self.possible_ends)
    
    def extract_file(self, path):
        if not self.possible_ends:
            print("No PDF end marker found")
            return
        with open(path, "wb") as file:
            file.write(self.data[:self.possible_ends[-1]+5])

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

                        if file_type == "JPG":
                            jpg_extractor = JPGExtractor(self.data[match.start():])
                            jpg_extractor.extract_file("test.jpg")
                except Exception as e:
                    print("Unexpected error occurred.")
            
with open("Tutorial6.pdf", 'rb') as file:
    pdf_extractor = PDFExtractor(file.read())
    pdf_extractor.extract_file("recover.pdf")