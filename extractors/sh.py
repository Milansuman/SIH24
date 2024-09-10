import re
class SHExtractor:
    def __init__(self, partial_data):
        self.data = partial_data
        self.end_marker = None
        self.find_end_marker()

    def find_end_marker(self):
        eof_markers = [b'\n# EOF', b'\n# End of file', b'\n exit 0', b'\n exit']
        for marker in eof_markers:
            pos = self.data.rfind(marker)
            if pos != -1:
                self.end_marker = pos + len(marker)
                return
        
        last_newline = self.data.rfind(b'\n')
        if last_newline != -1:
            self.end_marker = last_newline + 1
        else:
            self.end_marker = len(self.data)

    def extract_file(self, path):
        with open(path, "wb") as file:
            file.write(self.data[:self.end_marker])