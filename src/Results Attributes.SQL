CREATE TABLE IF NOT EXISTS Results(
    date date,
    home_team char(100),
    away_team char(100),
    home_score int,
    away_score int,
    tournament char(100),
    city char(100),
    country char(100),
    neutral boolean,
    id SERIAL PRIMARY KEY
);

COPY Results(date, home_team, away_team, home_score, away_score, tournament, city, country, neutral)
    FROM '/Users/mortenlundorffkristensen/Desktop/DIS/nft-crypto-punk/tmp/results.csv'
    delimiter ','
    CSV HEADER
    NULL 'NA';