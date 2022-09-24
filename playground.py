import requests


def run_script():
    live_tron = requests.get(url = "https://min-api.cryptocompare.com/data/price?fsym=TRX&tsyms=inr").json()
                
    print("tron_value", live_tron.json())

if __name__ == "__main__":
    run_script()