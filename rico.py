import pdfplumber
import re
import requests
from brokerage import Brokerage

def pdfToText(path):
    with pdfplumber.open(path, password=str(933)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        return text
    
def getAuctionDate(text):
    lines = text.split("\n")
    for index,line in enumerate(lines):
        if "Data pregão" in line:
            datePattern = r"\b\d{2}/\d{2}/\d{4}\b"
            date = re.search(datePattern, lines[index+1])

            if not date:
                continue
            
            return date.group(0)
            
    return None

def getBrokerages(text):
    brokerages = []
    lines = text.split("\n")
    date = getAuctionDate(pdfText)
    
    for index,line in enumerate(lines):
        if "Negócios realizados" in line:
            lineIndex = index + 2
            while "Resumo dos Negócios" not in lines[lineIndex]:
                data = lines[lineIndex].split(" ")
                price = data[-3].replace(",", ".")
                quantity = data[-4]
                
                dealTypePattern = r"\bC\b|\bV\b"
                dealTypeMatch = re.search(dealTypePattern, lines[lineIndex])
                dealType = dealTypeMatch.group(0) if dealTypeMatch else None
                
                typePattern = r"\bFRACIONARIO\b|\bVISTA\b"
                typeMatch = re.search(typePattern, lines[lineIndex])
                type = typeMatch.group(0) if typeMatch else None
                
                if not type:
                    lineIndex += 1
                    continue
                
                stockName = lines[lineIndex][lines[lineIndex].index(type) + len(type) : lines[lineIndex].index(str(quantity)) - 1]
                stockName = stockName.replace("#", "")

                stockCode = getStockCode(stockName)
                
                price = float(price.replace(",", "."))
                quantity = int(quantity)
                
                if dealType == "V":
                    quantity = -quantity
                
                brokerages.append(Brokerage(date=date, stockCode=stockCode, quantity=quantity, price=price, broker="rico"))
                
                lineIndex += 1
                
    return brokerages
    
                
def getStockCode(stockName):
    stockName = stockName.strip()
    yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": stockName, "quotes_count": 1, "country": "Brazil"}

    res = requests.get(url=yfinance, params=params, headers={'User-Agent': userAgent})
    
    if res.status_code != 200:
        raise Exception("Failed to get stock code")
    
    data = res.json()
    
    if len(data['quotes']) == 0:
        # remove last word from stockName
        stockName = " ".join(stockName.split(" ")[:-1]) 
        params['q'] = stockName
        
        res = requests.get(url=yfinance, params=params, headers={'User-Agent': userAgent})
        
        if res.status_code != 200:
            raise Exception("Failed to get stock code")
        
        data = res.json()
    
    companyCode = data['quotes'][0]['symbol'].split(".")[0]
    
    if companyCode.endswith('F'):
        companyCode = companyCode[:-1]
    
    return companyCode
    
    
pdf_file = "/home/alisson/Desktop/teste.pdf"
pdfText = pdfToText(pdf_file)
brokerages = getBrokerages(pdfText)

print(brokerages)

