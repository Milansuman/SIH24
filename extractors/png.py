import re

class PNGExtractor:
    def __init__(self, partial_data):
        self.data = partial_data
        self.possible_ends = []

        for match in re.finditer(b'\x49\x45\x4e\x44\xae\x42\x60\x82', partial_data):
            self.possible_ends.append(match.start())

        print(self.possible_ends)

    def extract_file(self, path):
        with open(path, "wb") as file:
            file.write(self.data[:self.possible_ends[0]+8])