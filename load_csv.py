import csv
import pandas as pd
import psycopg2
import configparser


def data_cleaning():
    """
    data_cleaning prepare the data before storing in the db,
    as quick analysis show, 4.2% of the AverageTemperature and
    AverageTemperatureUncertainty were missing, so a quick fill
    using the ffill was applied, ffill fills the missing values
    with the value from the precedent row
    so we pandas to read the csv, make the changes and save to back to csv
    """
    data = pd.read_csv("resources/GlobalLandTemperaturesByCity.csv")
    # convert dt dtype to datetime64
    data['dt'] = pd.to_datetime(data['dt'], errors='coerce')
    # fill missing values
    data["AverageTemperature"].fillna(method='ffill', inplace=True)
    data["AverageTemperatureUncertainty"].fillna(method='ffill', inplace=True)
    # save changes back to the csv file
    data.to_csv("resources/GlobalLandTemperaturesByCity.csv", index=False)


def load_csv():
    """
    load_csv connects to postgres database using the parameters in config file
    then calls data_cleaning function
    then opens the csv file and for each row an insert query is called
    """
    config = configparser.ConfigParser()
    config.read('db.cfg')

    DB_NAME = config.get("CLUSTER", "DB_NAME")
    DB_USER = config.get("CLUSTER", "DB_USER")
    DB_PASSWORD = config.get("CLUSTER", "DB_PASSWORD")
    DB_PORT = config.get("CLUSTER", "DB_PORT")
    HOST = config.get("CLUSTER", "HOST")

    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASSWORD,
                            host=HOST,
                            port=DB_PORT
                            )

    conn.autocommit = True
    cur = conn.cursor()

    data_cleaning()
    with open('resources/GlobalLandTemperaturesByCity.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row.
        for row in reader:
            cur.execute(
                '''
                INSERT INTO city_temperature(
                        dt, 
                        avg_temperature, 
                        avg_temperature_uncertainty, 
                        city, 
                        country, 
                        latitude,
                        longitude) 
                VALUES (%s, %s, %s, %s, %s, %s, %s) 
                ''',
                row
            )
    print('Done.')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    load_csv()