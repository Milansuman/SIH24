import re

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