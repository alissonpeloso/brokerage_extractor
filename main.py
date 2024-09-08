from extractors.rico import Rico
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_pdf> [password]")
        sys.exit(1)

    path = sys.argv[1]
    password = sys.argv[2] if len(sys.argv) == 3 else None
    
    rico = Rico(path, password)
    data = rico.extract()
    
    data_json = [brokerage.__json__() for brokerage in data]
    print(data_json)        