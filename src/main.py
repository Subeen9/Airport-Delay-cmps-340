from src.handle_csv import handleData

def main():
    child = handleData()
    child.perform_analysis()

if __name__ == "__main__":
    main()
