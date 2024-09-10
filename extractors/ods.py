import re
class ODSExtractor:
    def __init__(self, partial_data):
        self.data = partial_data
        self.possible_ends = []
        for match in re.finditer(b'\x50\x4B\x05\x06', partial_data):
            self.possible_ends.append(match.start())

        print(self.possible_ends)
    
    def extract_file(self, path):
        if not self.possible_ends:
            print("No potential ODS end marker found")
            return
        with open(path, "wb") as file:
            file.write(self.data[:self.possible_ends[-1] + 22])