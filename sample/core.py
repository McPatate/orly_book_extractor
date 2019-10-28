from .extractor import Extractor
from ebooklib import epub

class BookGeneration():
    def __init__(self):
        extractor = Extractor()
        extractor.sign_in()
        print(extractor.jwt)
