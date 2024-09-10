import re
class PPTExtractor:
    def __init__(self, partial_data):
        self.data = partial_data
        self.possible_ends = []

        for match in re.finditer(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', partial_data):
            self.possible_ends.append(match.start())

        print(self.possible_ends)
    
    def extract_file(self, path):
        if not self.possible_ends:
            print("No potential PPT end marker found")
            return
        with open(path, "wb") as file:
            file.write(self.data[:self.possible_ends[-1] + 1024])