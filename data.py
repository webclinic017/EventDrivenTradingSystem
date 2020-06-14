from datetime import datetime, timedelta
import pandas as pd
import sqlite3
import yfinance as yf

class Data():
    def __init__(self):
        """Creates a data source for stock data via an sqlite3 database.
        Data will first be searched in the database file. If not found locally,
        it will be retrieved from the financial data provider.
        """
        self.con = sqlite3.connect("data/data.db")
        self.db = self.con.cursor()

        # SQLite does not have foreign keys enabled by default
        self.db.execute('PRAGMA foreign_keys = ON')

    def __del__(self):
        self.con.commit()
        self.con.close()

    def getAssetId(self, symbol):
        """Returns the asset ID as stored in the database.

        :param symbol: Symbol of the asset
        :type symbol: str
        :raises ValueError: If the symbol is not found in the database
        :return: Asset ID
        :rtype: int
        """
        result = self.db.execute(
            "SELECT id FROM assets WHERE symbol=?",
            (symbol, )
            ).fetchone()
        if result == None:
            raise ValueError("Asset '{}' does not exist in database".format(symbol))
        return result[0]

    def getVendorId(self, name):
        """Returns the vendor ID as stored in the database.

        :param name: Name of the vendor
        :type name: str
        :raises ValueError: If the vendor name is not foundd in the database
        :return: Vendor ID
        :rtype: int
        """
        result = self.db.execute(
            "SELECT id FROM data_vendor WHERE name=?",
            (name, )
            ).fetchone()
        if result == None:
            raise ValueError("Vendor '{}' does not exist in database".format(name))
        return result[0]
    
    def getEodData(self, symbol, start=None, end=None, resolution="D"):
        # Data aggregation from resolution not implemented

        """Returns the end of day OHLCV price data.

        :param symbol: Asset symbol
        :type symbol: str
        :param start: Start date of price data as YYYY-MM-DD, defaults to None
        :type start: str, optional
        :param end: End date of price data as YYYY-MM-DD, defaults to None
        :type end: str, optional
        :param resolution: Candlestick data frequency, defaults to "D"
        :type resolution: str, optional
        :raises ValueError: If the start is after the end or if the symbol is not found in the database
        :return: A asset price candlestick time series
        :rtype: pandas.DataFrame
        """

        if start > end:
            raise ValueError("Start date is after end date")

        query = """ SELECT date, open, high, low, close, adj_close, volume
                FROM daily_price
                WHERE asset_id = ? """
        params = [self.getAssetId(symbol)]
        if start != None:
            query += "AND date >= ?"
            params.append(start)
        if end != None:
            query += "AND date <= ?"
            params.append(end)

        return pd.read_sql(
            query,
            self.con,
            params=params,
            index_col="date",
            parse_dates="date"
            ).round(4)

    def updateEodData(self, symbols=None):
        """Updates the database with the new end of day data based on the
        last price that is present in the database for each given asset.
        If symbols are not specified, all assets present in the database will be updated. 

        :param symbols: List of symbol prices to be updated, defaults to None
        :type symbols: list of str, optional
        """
        vendorId = self.getVendorId("Yahoo Finance")
        if symbols == None:
            symbols = map(lambda x: x[0], self.db.execute("SELECT symbol FROM assets").fetchall())

        for s in symbols:
            assetId = self.getAssetId(s)
            latestDate = self.db.execute(
                "SELECT MAX(date) FROM daily_price WHERE asset_id = ?",
                (assetId, )
                ).fetchone()[0]

            if latestDate == None:
                df = yf.download(s)
            else:
                startDate = (datetime.fromisoformat(latestDate) + timedelta(days=1)).strftime("%Y-%m-%d")
                df = yf.download(s, start=startDate).loc[startDate:]
                if len(df) == 0:
                    print("{} is already up to date (latest date: {})".format(s, latestDate))
                    continue
            
            df.rename(
                columns=lambda x: x.lower().replace(' ', '_'),
                index=lambda x: str(x.date()),
                inplace=True)
            
            df.insert(loc=len(df.columns), column="asset_id", value=assetId)
            df.insert(loc=len(df.columns), column="data_vendor_id", value=vendorId)
            df.to_sql('daily_price', self.con, index_label="date", if_exists="append")
            print("{} has been updated from {})".format(s, latestDate))