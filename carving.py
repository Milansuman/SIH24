"""
FILE CARVING MODULE
"""
import re
from extractors import html, jpg, png, zip, rar

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
    ),
    "DOCX": (
        b'\x50\x4B\x03\x04\x14\x00\x06\x00'
    )
}

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
