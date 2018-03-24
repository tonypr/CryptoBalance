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

Then `cd` into the directory and install the project's dependencies:

`cd CryptoBalance && pip3 install -r requirements.txt`

## Using the tool

To run the code, use the following:

`python3 main.py`

This will attempt to get your total investment and your current balance. As this is the first time that you will run this, it will set up configuration files for your Coinbase and Gdax accounts. You will find these files under the `config` folder that is generated for you.

You'll then have to replace the TODOs in the files in order for the tool to work. You can generate api keys for this tool on both Coinbase and Gdax. Please only use "read" permissions! I do not want this tool to be able to perform trades on your account so please limit your access to only what is needed for the tool. I'll be reviewing the permissions soon to see which "read" permissions are needed.

After filling in the TODOs, you can re-run the previous command and you'll be able to see the results.

## Versioning

This project uses [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
