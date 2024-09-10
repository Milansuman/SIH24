import re
class EXEExtractor:
    def __init__(self, partial_data):
        self.data = partial_data
        self.file_size = None
        self.parse_pe_header()

    def parse_pe_header(self):
        pe_offset = self.data.find(b'PE\x00\x00')
        if pe_offset == -1:
            print("Not a valid PE file")
            return

        optional_header_offset = pe_offset + 24
        if len(self.data) < optional_header_offset + 60:
            print("File too short to contain valid PE header")
            return

        self.file_size = int.from_bytes(self.data[optional_header_offset+56:optional_header_offset+60], byteorder='little')
        print(f"Detected EXE file size: {self.file_size} bytes")

    def extract_file(self, path):
        if self.file_size is None:
            print("Unable to determine EXE file size")
            return
        
        with open(path, "wb") as file:
            file.write(self.data[:self.file_size])