from extractors import nuinvest
from extractors.nuinvest import Nuinvest
from extractors.rico import Rico
import sys

def teste():
    path = "/home/alisson/Desktop/nu2.pdf"
    nuinvest = Nuinvest(path)
    data = nuinvest.extract()
    data_json = [brokerage.__json__() for brokerage in data]
    print(data_json)

if __name__ == "__main__":
    teste()
    # if len(sys.argv) < 3:
    #     print("Usage: python main.py <broker> <path_to_pdf> [password]")
    #     sys.exit(1)

    # broker = sys.argv[1]
    # path = sys.argv[2]
    # password = sys.argv[3] if len(sys.argv) == 4 else None
    
    # if broker == "rico":
    #     rico = Rico(path, password)
    #     data = rico.extract()
    # if broker == "nuinvest":
    #     nuinvest = Nuinvest(path, password)
    #     data = nuinvest.extract()
    # else:
    #     print("Broker not supported")
    #     sys.exit(1)
    
    # data_json = [brokerage.__json__() for brokerage in data]
    # print(data_json)        