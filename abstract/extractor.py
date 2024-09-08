import pdfplumber
import abc

class Extractor(abc.ABC):
    
    def __init__(self, path: str, password: str | None) -> None:
        try:
            self._text = self.pdf_to_text(path, password)
        except Exception as e:
            print(f"Error extracting text from PDF, check if the file is password protected.")
            raise e
            
    def pdf_to_text(self, path: str, passport: str | None) -> str:
        """
        Extracts text from a PDF file.

        Args:
            path (str): The path to the PDF file.

        Returns:
            str: The extracted text from the PDF file.
        """
        with pdfplumber.open(path, password=passport) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
            return text
        
    @abc.abstractmethod
    def extract(self) -> str | None:
        pass
        
    @abc.abstractmethod
    def _get_auction_date(self, text: str) -> str | None:
        pass
    
    @abc.abstractmethod
    def _get_brokerages(self, text: str) -> list:
        pass
    
    @abc.abstractmethod
    def _get_deal_type(self, line: str) -> str | None:
        pass