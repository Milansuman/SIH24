import re
class LOGExtractor:
    def __init__(self, partial_data):
        self.data = partial_data
        self.possible_ends = []

        for match in re.finditer(b'\n', partial_data):
            self.possible_ends.append(match.start())

        print(f"Possible LOG ends: {self.possible_ends}")
    
    def extract_file(self, path):
        if self.possible_ends:
            with open(path, "wb") as file:
                file.write(self.data[:self.possible_ends[-1] + 1])
        else:
            print("No valid LOG end structure found")