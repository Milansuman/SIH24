import re
class TIFFExtractor:
    def __init__(self, partial_data):
        self.data = partial_data
        self.possible_ends = []
        for match in re.finditer(b'\x00\x00\x00\x00', partial_data):
            self.possible_ends.append(match.end())

        print(self.possible_ends)

    def extract_file(self, path):
        if self.possible_ends:
            with open(path, "wb") as file:
                file.write(self.data[:self.possible_ends[-1]])
            print(f"TIFF file extracted and saved to {path}")
        else:
            print("Unable to extract TIFF file: No valid end found.")