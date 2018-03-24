# CryptoBalance

This project deals with calculating the following:
- Current amount of money invested in cryptocurrencies (Gdax/Coinbase currently supported)
- Current total balance in cryptocurrencies (Gdax/Coinbase supported)
- Your current return on investment, calculated from the two numbers above.

If you've interacted with both Coinbase and Gdax to perform trades, then you might have already started having a hard time keeping track of your overall gains/losses. This project helps address this need. It can also be extended to support other exchanges.

#### Warning

While I believe the calculations in the code are done correctly, I make no guarantee that that is indeed the case. There could be edge cases unaccounted for which may present an inaccurate view of your balance. If you were to find such a case, I would gladly update the code to reflect it. However, so far, I have not found any inaccuracies.

## Getting Started

To run this code locally, you can git clone the repo:

`git clone git@github.com:tonypr/CryptoBalance.git`

### Prerequisites

You'll need Python 3 installed in your system in order to be able to run the code.

You can install the required dependencies with:

`cd cryptobalance && pip3 install -r requirements.txt`

## Versioning

This project uses [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
