"""
FILE CARVING MODULE
"""
import re
from extractors import html, jpg, png, zip, rar,gif,pdf,ppt

magic_nums = {
    "JPG": (
        b'\xFF\xD8\xFF\xD8',
        b'\xFF\xD8\xFF\xE0', 
        b'\xFF\xD8\xFF\xE1'
        b'\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00\x01'
    ),
    "PNG": (
        b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A',
    ),
    "ZIP": (
        b'\x50\x4B\x03\x04',
    ),
    "HTML": (
        b'<html>',
        b'<!DOCTYPE html>',
        b'<!doctype html>'
    ),
    "GIF": (
        b'\x47\x49\x46\x38\x37\x61',
        b'\x47\x49\x46\x38\x39\x61'
    ),
    "PPT":(
        b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1',
    ),
    "PDF":(
        b'\x25\x50\x44\x46\x2D',
    )

}

class Carver:
    def __init__(self, path):
        self.path = path
        self.data = b''
        self.indexes = []
        self.readData()
    
    def readData(self):
        with open(self.path, "rb") as file:
            self.data = file.read()
    
    def extractFiles(self):
        for file_type in magic_nums:
            for byte_string in magic_nums[file_type]:
                try:
                    for match in re.finditer(byte_string, self.data):
                        print(f"{file_type}: {match.start()}")

                        match file_type:
                            case "JPG":
                                jpg_extractor = jpg.JPGExtractor(self.data[match.start():])
                                jpg_extractor.extract_file(f"extracted_{match.start()}.jpg")
                            case "PNG":
                                png_extractor = png.PNGExtractor(self.data[match.start():])
                                png_extractor.extract_file(f"extracted_{match.start()}.png")
                            case "ZIP":
                                zip_extractor = zip.ZIPExtractor(self.data[match.start():])
                                zip_extractor.extract_file(f"extracted_{match.start()}.zip")
                            case "HTML":
                                html_extractor = html.HTMLExtractor(self.data[match.start():])
                                html_extractor.extract_file(f"extracted_{match.start()}.html")
                            case "GIF":
                                gif_extractor = gif.GIFExtractor(self.data[match.start():])
                                gif_extractor.extract_file(f"extracted_{match.start()}.gif")
                            case "PPT":
                                ppt_extractor = ppt.PPTExtractor(self.data[match.start():])
                                ppt_extractor.extract_file(f"extracted_{match.start()}.ppt")
                            case "PDF":
                                pdf_extractor = pdf.PDFExtractor(self.data[match.start():])
                                pdf_extractor.extract_file(f"extracted_{match.start()}.pdf")

                except Exception as e:
                    print(f"Unexpected error occurred. {e}")
