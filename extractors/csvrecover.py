import re
class CSVExtractor:
    def __init__(self, partial_data):
        self.data = partial_data
        self.possible_ends = []
        end_markers = [b'\r\n\r\n', b'\n\n', b'\r\r'] 
        for marker in end_markers:
            for match in re.finditer(marker, partial_data):
                self.possible_ends.append(match.start())

        if not self.possible_ends:
            self.possible_ends.append(len(partial_data))

        print(self.possible_ends)
    
    def extract_file(self, path):
        if self.possible_ends:
            with open(path, "wb") as file:
                file.write(self.data[:self.possible_ends[0]])
        else:
            print("No valid CSV structure found")