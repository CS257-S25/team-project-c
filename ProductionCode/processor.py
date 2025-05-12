"""Helper functions for loading and filtering UFO sightings data from a PostgreSQL database."""

import sys
import psycopg2
import ProductionCode.psql_config as config
from collections import Counter

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

    def get_all_sightings(self):
        '''Fetches all UFO records from the database.'''
        results = None
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM ufo"
            cursor.execute(query)
            results = self._format_results(cursor)
        except psycopg2.Error as e:
            print("Error fetching all sightings: ", e)
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

def _count_yearly_sightings(all_sightings):
    """Counts the number of sightings per year."""
    return Counter(sighting['ufo_date'].year for sighting in all_sightings)

def _find_years_with_max_sightings(yearly_counts):
    """Finds the year(s) with the maximum number of sightings."""
    if not yearly_counts:
        return [], 0
    max_sighting_count = max(yearly_counts.values())
    years_with_max_sightings = [year for year, count in yearly_counts.items() if count == max_sighting_count]
    return years_with_max_sightings, max_sighting_count

def _count_all_shapes(all_sightings):
    """Counts the occurrences of each UFO shape across all sightings."""
    all_shapes = [sighting['ufo_shape'].lower() for sighting in all_sightings if sighting['ufo_shape']]
    return Counter(all_shapes)

def _get_most_common_shapes(shape_counts, top_n=3):
    """Gets the top N most common shapes from the shape counts."""
    return shape_counts.most_common(top_n)

def calculate_max_sightings():
    """Calculates and returns the years with the maximum number of sightings and the most frequent shape overall."""
    data_source = DataSource()
    all_sightings = data_source.get_all_sightings()
    if not all_sightings:
        return "No sightings data available."

    yearly_counts = _count_yearly_sightings(all_sightings)
    years_with_max, max_count = _find_years_with_max_sightings(yearly_counts)
    all_shape_counts = _count_all_shapes(all_sightings)
    most_common_shapes = _get_most_common_shapes(all_shape_counts)

    return {
        "years_with_max_sightings": years_with_max,
        "max_sighting_count": max_count,
        "most_common_shapes_overall": most_common_shapes
    }
