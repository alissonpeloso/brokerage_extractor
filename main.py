from extractors.nuinvest import Nuinvest
from extractors.rico import Rico
import json
import sys

def get_brokerages_data(broker: str, path: str, password: str | None = None) -> list:
    if broker == "rico":
        rico = Rico(path, password)
        data = rico.extract()
    elif broker == "nuinvest":
        nuinvest = Nuinvest(path, password)
        data = nuinvest.extract()
    else:
        raise ValueError("Broker not supported")
    
    return data

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <broker> <path_to_pdf> [password]")
        sys.exit(1)

    broker = sys.argv[1]
    path = sys.argv[2]
    password = sys.argv[3] if len(sys.argv) == 4 else None
    
    try:
        data = get_brokerages_data(broker, path, password)
    except Exception as e:
        error_data = {
            "error": {
                "message": "An error occurred while extracting the data.",
                "exception": str(e)
            }    
        }
        print(json.dumps(error_data))
        sys.exit(1)
    
    data_json = [brokerage.__json__() for brokerage in data]
    print(json.dumps(data_json))