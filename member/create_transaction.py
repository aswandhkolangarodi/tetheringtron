from cryptoutilts import CoinPayments,crypto_client

def index():
    rates = crypto_client.rates()
    print(rates)


if __name__ == "__main__":
    index()
