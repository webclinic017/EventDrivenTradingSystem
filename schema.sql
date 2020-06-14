-- SQLite

PRAGMA foreign_keys = ON;

-- Metadata tables i.e. stock exchanges, data sources, asset universe

DROP TABLE IF EXISTS exchange;
CREATE TABLE exchange (
    id INTEGER NOT NULL PRIMARY KEY,
    abbrev TEXT NOT NULL,
    name TEXT NOT NULL,
    code TEXT UNIQUE,
    timezone TEXT NOT NULL,
    created_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS data_vendor;
CREATE TABLE data_vendor (
    id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS assets;
CREATE TABLE assets (
    id INTEGER NOT NULL PRIMARY KEY,
    exchange_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    instrument TEXT NOT NULL,
    name TEXT,
    currency TEXT NOT NULL,
    created_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (exchange_id)
        REFERENCES exchange (id)
);


-- Price data tables i.e. EOD data, intraday data

DROP TABLE IF EXISTS daily_price;
CREATE TABLE daily_price (
    data_vendor_id INTEGER NOT NULL,
    asset_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    adj_close REAL,
    volume INTEGER,
    created_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (date, asset_id),
    FOREIGN KEY (data_vendor_id)
        REFERENCES data_vendor (id),
    FOREIGN KEY (asset_id)
        REFERENCES assets (id)
);