import sqlite3


class SQLite:

    def __init__(self, path):
        self.__connection = sqlite3.connect(path)
        self.__connection.row_factory = sqlite3.Row

    def get_connection(self):
        return self.__connection

    def execute(self, query, **parameters):
        cursor = self.get_connection().cursor()

        cursor.execute(query, parameters)

        return cursor

    def fetch_all(self, query, **parameters):
        cursor = self.execute(query, **parameters)

        results = [dict(result) for result in cursor.fetchall()]
        cursor.close()

        return results

    def get_data_for_country(self, country):
        query = f'''
            SELECT
                '{country}'         AS country,
                "time"              AS "year",
                Environmental_taxes AS tax,
                Greenhouse_gases    AS gases,
                Investments         AS investments,
                Air_pollutants      AS pollution
            FROM {country}
            ORDER BY year
        '''

        return self.fetch_all(query=query)

    def get_data_for_countries(self, countries):
        data = []

        for country in countries:
            data.extend(self.get_data_for_country(country=country))

        return data
