
import re

from abstract.extractor import Extractor
from models.brokerage import Brokerage

class Nuinvest (Extractor):
    
    def extract(self) -> list:
        brokerages = self._get_brokerages()
        fee, ir = self._get_taxes()
        self._make_brokerage_apportionment(brokerages, fee, ir)
        
        return brokerages
    
    def _get_auction_date(self) -> str | None:
        """
        Extracts the auction date from the given text.
                    
        Returns:
            str or None: The extracted auction date in the format "dd/mm/yyyy", or None if no date is found.
        """
        # Combine the search for "Data pregão" and the date pattern in one regex
        pattern = r"Data Pregão(.|\n)*?(\d{2}/\d{2}/\d{4})"
        
        # Search for the pattern in the entire text
        match = re.search(pattern, self._text, re.DOTALL)
        
        # Return the date if found, otherwise return None
        return match.group(2) if match else None


    def _get_note_id(self) -> str | None:
        """
        Extracts the note ID from the given text.
        
        Returns:
            str or None: The extracted note ID, or None if no ID is found.
        """
        pattern = r"Número da nota(.|\n)*?(\d{5,})"
        match = re.search(pattern, self._text, re.DOTALL)
        
        return match.group(2) if match else None


    def _get_brokerages(self) -> list:
        """
        Extracts brokerage transactions from the given text.
        
        Args:
            text (str): The text to extract brokerage transactions from.
            
        Returns:
            list: A list of Brokerage objects containing date, stock code, quantity, price, and broker information.
        """
        
        brokerages = []
        date = self._get_auction_date()
        note_id = self._get_note_id()

        if not date:
            raise ValueError("Auction date not found in the provided text")
        
        pattern = r"MMeerrccaaddoo(.|\n)*?RReessuummoo"
        match = re.search(pattern, self._text, re.DOTALL)
        
        if not match:
            raise ValueError("No brokerage transactions found in the provided text")
        
        lines = match.group(0).split("\n")
        
        # Ignore first and last lines and table header
        lines = lines[1:-1]
            
        # Look for the "Negócios realizados" section in the text
        for line in lines:
            brokerage = self._extract_brokerage_note_from_text(line)
            
            if not brokerage:
                continue
            
            brokerage.__setattr__("date", date)
            brokerage.__setattr__("note_id", note_id)
            brokerages.append(brokerage)
        
        return brokerages
    
    
    def _extract_brokerage_note_from_text(self, line: str) -> Brokerage | None:
        
        def extract_deal_type(line: str) -> str | None:
            """Extracts the deal type ('C' for buy, 'V' for sell) from the line."""
            match = re.search(r"\bC\b|\bV\b", line)
            return match.group(0) if match else None
        
        def extract_transaction_type(line: str) -> str | None:
            """Extracts the transaction type (e.g., 'FRACIONARIO', 'VISTA') from the line."""
            match = re.search(r"\bFRACIONARIO\b|\bVISTA\b", line)
            return match.group(0) if match else None
        
        data = line.split(" ")
            
        if len(data) < 4:
            # Skip lines that don't have enough data
            return None
        
        # Extract the stock code from the line
        price = data[-3].replace(",", ".")
        quantity = data[-4]
        
        deal_type = extract_deal_type(line)
        transaction_type = extract_transaction_type(line)
        
        if not transaction_type:
            # Skip if the transaction type is not found
            return None
        
        # Extract stock name based on its position relative to the transaction type and quantity
        stock_name_start = line.index(transaction_type) + len(transaction_type)
        stock_name_end = line.index(str(quantity)) - 1
        stock_name = line[stock_name_start:stock_name_end].replace("#", "").strip()
        
        stock_symbol = self._get_stock_symbol(stock_name)
        
        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            # Skip lines with invalid data
            return None
        
        # If the deal type is 'V' (sell), make quantity negative
        if deal_type == "V":
            quantity = -quantity
        
        # Append the brokerage information
        return Brokerage(
            stock_symbol=stock_symbol, 
            quantity=quantity, 
            price=price, 
            broker="nuinvest",
        )
                        
                        
    def _get_stock_symbol(self, stock_name: str) -> str:
        """
        Extracts the stock code from the given stock name.
        
        Args:
            stock_name (str): The stock name to extract the code from.
            
        Returns:
            str: The stock code.
        """
        stock_symbol = stock_name.split(" ")[0]
        
        # Remove any non-alphanumeric characters from the stock code
        stock_symbol = re.sub(r"\W", "", stock_symbol)
        
        # Remove F from the end of the stock code if it's there
        stock_symbol = stock_symbol.rstrip("F")
                    
        if stock_symbol:
            return stock_symbol

        # Raise an exception if no valid stock code is found after all attempts
        raise Exception("Stock code not found after trying all possibilities.")
    
    def _get_taxes(self) -> list:
        fee_patterns = [
            r"Taxa de liquidação.*?(\d+,\d+)",
            r"Taxa de Registro.*?(\d+,\d+)",
            r"Taxa de Termo / Opções.*?(\d+,\d+)",
            r"Taxa A.N.A.*?(\d+,\d+)",
            r"Emolumentos.*?(\d+,\d+)",
            r"Corretagem.*?(\d+,\d+)",
            r"ISS.*?(\d+,\d+)",
            r"Outras.*?(\d+,\d+)"
        ]
        
        ir_pattern = r"I.R.R.F.*?(\d+,\d+)(?!.*\d+,\d+)"
        
        fees = []
        for pattern in fee_patterns:
            match = re.search(pattern, self._text, re.IGNORECASE)
            if match:
                fees.append(float(match.group(1).replace(",", ".")))
        
        ir_match = re.search(ir_pattern, self._text, re.IGNORECASE)
        ir = float(ir_match.group(1).replace(",", ".")) if ir_match else 0.0
        
        fee = sum(fees)
        
        return [fee, ir]
    
    def _make_brokerage_apportionment(self, brokerages: list, fee: float, ir: float):
        """
        Splits the fee and IR among the brokerages.
        
        Args:
            brokerages (list): A list of Brokerage objects.
            fee (float): The total fee to split.
            ir (float): The total IR to split.
            
        Returns:
            None
        """
        total_amount, sold_amount = 0, 0
        
        for brokerage in brokerages:
            total_amount += abs(brokerage.price * brokerage.quantity)
            if brokerage.quantity < 0:
                sold_amount += abs(brokerage.price * brokerage.quantity)
                
        for brokerage in brokerages:
            brokerage.fees = round(fee * abs(brokerage.price * brokerage.quantity) / total_amount, 2) if total_amount else 0.0
            
            if brokerage.quantity < 0:
                brokerage.ir = round(ir * abs(brokerage.price * brokerage.quantity) / sold_amount, 2) if sold_amount else 0.0
        
        return 

    def _get_deal_type(self, line: str) -> str | None:
        raise NotImplementedError
