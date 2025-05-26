"""Helper functions for loading and filtering UFO sightings data from a PostgreSQL database."""

import sys
import psycopg2
import ProductionCode.psql_config as config


class DataSource:
    '''Class to manage connection to the PostgreSQL database.'''
    def __init__(self):
        '''Constructor that initiates connection to database'''
        self.connection = self.connect()

    def connect(self):
        '''Initiates connection to database using information in the psqlConfig.py file.
        Returns the connection object.'''
        connection = None # Initialize connection to None
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

    def get_top_n_years(self, n):
        """Fetches the top N years with the most UFO sightings.
        Args:
            n (int): The number of top years to retrieve.
        Returns:
            list[tuple]: A list of tuples, where each tuple is (year, count),
                         ordered by count descending. Returns None on error.
        """
        results = None
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT EXTRACT(YEAR FROM ufo_date)::INTEGER AS year, COUNT(*) AS count
                FROM ufo
                WHERE ufo_date IS NOT NULL
                GROUP BY year
                ORDER BY count DESC
                LIMIT %s
            """
            cursor.execute(query, (n,))
            # Fetches list of tuples directly
            results = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching top {n} years: ", e)
            return None
        finally:
            if cursor:
                cursor.close()
        return results

    def get_top_n_shapes(self, n):
        """Fetches the top N shapes with the most UFO sightings.
        Args:
            n (int): The number of top shapes to retrieve.
        Returns:
            list[tuple]: A list of tuples, where each tuple is (shape, count),
                         ordered by count descending. Returns None on error.
        """
        results = None
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT LOWER(ufo_shape) AS shape, COUNT(*) AS count
                FROM ufo
                WHERE ufo_shape IS NOT NULL AND TRIM(LOWER(ufo_shape)) != ''
                GROUP BY shape
                ORDER BY count DESC
                LIMIT %s
            """
            cursor.execute(query, (n,))
            results = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching top {n} shapes: ", e)
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

def get_top_years(num_years):
    """Gets the top N years with the most sightings.
    Args:
        num_years (int): Number of top years required.
    Returns:
        list[tuple]: List of (year, count) tuples or None on error.
    """
    data_source = DataSource()
    return data_source.get_top_n_years(num_years)

def get_top_shapes(num_shapes):
    """Gets the top N shapes with the most sightings.
    Args:
        num_shapes (int): Number of top shapes required.
    Returns:
        list[tuple]: List of (shape, count) tuples or None on error.
    """
    data_source = DataSource()
    return data_source.get_top_n_shapes(num_shapes)
