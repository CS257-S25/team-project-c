"""Helper functions for loading and filtering UFO sightings data from a PostgreSQL database."""

import sys
import psycopg2
import ProductionCode.psqlConfig as config

class DataSource:
    '''Class to manage connection to the PostgreSQL database.'''
    def __init__(self):
        '''Constructor that initiates connection to database'''
        self.connection = self.connect()

    def connect(self):
        '''Initiates connection to database using information in the psqlConfig.py file.
        Returns the connection object.'''
        try:
            connection = psycopg2.connect(
                database=config.DATABASE,
                user=config.USER,
                password=config.PASSWORD,
                host="localhost"
            )
        except psycopg2.Error as e:
            print("Connection error: ", e)
            sys.exit(1)
        return connection

    def get_sightings_by_shape(self, shape):
        '''Fetches all columns of UFO records from the database based on the shape provided.
        shape: str - The shape of the UFO to filter by.
        Returns a list of UFO records matching the shape.'''
        results = None
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM ufo WHERE LOWER(ufo_shape) = %s"
            cursor.execute(query, (shape.lower(),))
            results = self._format_results(cursor)
        except psycopg2.Error as e:
            print("Error fetching sightings by shape: ", e)
            return None
        finally:
            if cursor:
                cursor.close()
        return results

    def get_sightings_by_year(self, year):
        '''Fetches all columns of UFO records from the database based on the year of the sighting.
        year: int - The year to filter by.
        Returns a list of UFO records matching the year.'''
        results = None
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM ufo WHERE EXTRACT(YEAR FROM ufo_date) = %s"
            cursor.execute(query, (year,))
            results = self._format_results(cursor)
        except psycopg2.Error as e:
            print("Error fetching sightings by year: ", e)
            return None
        finally:
            if cursor:
                cursor.close()
        return results

    def _format_results(self, cursor):
        '''Helper function to format the results from the cursor into a list of dictionaries.'''
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def display_results(results):
    """Display search results."""
    if not results:
        print("No sightings found matching your query, please try again with different parameters.")
        return
    for row in results:
        print(row)

def get_sightings_by_shape(shape):
    """Get sightings by given shape."""
    data_source = DataSource()
    return data_source.get_sightings_by_shape(shape)

def get_sightings_by_year(year):
    """Get sightings by given year."""
    data_source = DataSource()
    return data_source.get_sightings_by_year(year)
