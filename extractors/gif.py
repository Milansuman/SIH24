import re

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