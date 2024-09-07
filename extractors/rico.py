
import requests
import re

from abtract.extractor import Extractor
from models.brokerage import Brokerage

class Rico (Extractor):
    
    def extract(self) -> list:
        brokerages = self._get_brokerages()
        return brokerages
    
    def _get_auction_date(self) -> str | None:
        """
        Extracts the auction date from the given text.
                    
        Returns:
            str or None: The extracted auction date in the format "dd/mm/yyyy", or None if no date is found.
        """
        # Combine the search for "Data pregão" and the date pattern in one regex
        pattern = r"Data pregão.*?(\d{2}/\d{2}/\d{4})"
        
        # Search for the pattern in the entire text
        match = re.search(pattern, self._text, re.DOTALL)
        
        # Return the date if found, otherwise return None
        return match.group(1) if match else None


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
        
        if not date:
            raise ValueError("Auction date not found in the provided text")
        
        pattern = r"Negócios realizados.*?Resumo dos Negócios"
        match = re.search(pattern, self._text, re.DOTALL)
        
        if not match:
            raise ValueError("No brokerage transactions found in the provided text")
        
        lines = match.group(0).split("\n")
        
        # Ignore first and last lines and table header
        lines = lines[2:-1]
            
        # Look for the "Negócios realizados" section in the text
        for line in lines:
            brokerage = self._extract_brokerage_note_from_text(line)
            
            if not brokerage:
                continue
            
            brokerage.date = date
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
        
        stock_code = self._get_stock_code(stock_name)
        
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
            stockCode=stock_code, 
            quantity=quantity, 
            price=price, 
            broker="rico"
        )
                        
                        
    def _get_stock_code(self, stock_name: str) -> str:
        """
        Fetches the stock code for the given stock name from Yahoo Finance.
        
        Args:
            stock_name (str): The name of the stock.
            
        Returns:
            str: The stock code, or raises an exception if not found.
        """
        
        def fetch_stock_data(query: str) -> dict:
            """Helper function to make the API request to Yahoo Finance."""
            url = "https://query2.finance.yahoo.com/v1/finance/search"
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
            params = {"q": query, "quotes_count": 1, "country": "Brazil"}
            
            response = requests.get(url=url, params=params, headers={'User-Agent': user_agent})
            if response.status_code != 200:
                raise Exception(f"Failed to fetch stock data for query '{query}' (HTTP {response.status_code})")
            
            return response.json()

        stock_name = stock_name.strip()
        
        # Retry search with progressively shorter names if no results found
        while stock_name:
            data = fetch_stock_data(stock_name)
            
            if data.get('quotes'):
                company_code = data['quotes'][0]['symbol'].split(".")[0]
                
                # Remove trailing 'F' if present
                if company_code.endswith('F'):
                    company_code = company_code[:-1]
                
                return company_code
            
            # If no results, remove the last word from the stock_name
            stock_name = " ".join(stock_name.split(" ")[:-1])

        # Raise an exception if no valid stock code is found after all attempts
        raise Exception("Stock code not found after trying all possibilities.")

    def _get_deal_type(self, line: str) -> str | None:
        raise NotImplementedError


rico = Rico("/home/alisson/Desktop/teste.pdf", "933")
data = rico.extract()

for item in data:
    print(item.__str__())