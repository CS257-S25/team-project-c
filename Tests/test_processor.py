"""Tests for the DataSource class in processor.py."""
import unittest
from unittest.mock import patch, Mock
import psycopg2
from ProductionCode.processor import DataSource
from ProductionCode import psql_config as config

# Sample test data
mock_shape_results = [
    {'col1': 'a', 'ufo_shape': 'circle', 'col3': 'b'},
    {'col1': 'c', 'ufo_shape': 'circle', 'col3': 'd'}
]
mock_year_results = [
    {'col1': 'x', 'ufo_date': '2000-10-10', 'col3': 'y'},
    {'col1': 'z', 'ufo_date': '2000-11-11', 'col3': 'w'}
]
mock_top_years = [(1999, 50), (2001, 45), (1995, 40)]
mock_top_shapes = [('light', 100), ('circle', 90), ('triangle', 80)]

class TestDatabaseConnection(unittest.TestCase):
    """Tests for database connection handling."""
    
    @patch('ProductionCode.processor.psycopg2')
    def test_connect_success(self, mock_psycopg2):
        """Test successful database connection."""
        mock_connection = Mock()
        mock_psycopg2.connect.return_value = mock_connection
        data_source = DataSource()
        mock_psycopg2.connect.assert_called_once_with(
            database=config.DATABASE,
            user=config.USER,
            password=config.PASSWORD,
            host="localhost"
        )
        self.assertEqual(data_source.connection, mock_connection)

    @patch('ProductionCode.processor.psycopg2')
    def test_connect_failure(self, mock_psycopg2):
        """Test database connection failure."""
        mock_psycopg2.Error = psycopg2.Error
        mock_psycopg2.connect.side_effect = mock_psycopg2.Error("Connection failed")

        with patch('sys.exit') as mock_exit, \
             patch('builtins.print') as mock_print:
            DataSource()
            mock_exit.assert_called_once_with(1)
            mock_print.assert_any_call("Connection error: ", mock_psycopg2.connect.side_effect)

class TestDataSourceMethods(unittest.TestCase):
    """Tests for DataSource query methods."""

    def setUp(self):
        """Set up mock database connection for each test."""
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        
        # Patch psycopg2 for all tests in this class
        self.psycopg2_patcher = patch('ProductionCode.processor.psycopg2')
        self.mock_psycopg2 = self.psycopg2_patcher.start()
        self.mock_psycopg2.connect.return_value = self.mock_connection
        self.mock_psycopg2.Error = psycopg2.Error

    def tearDown(self):
        """Clean up patches."""
        self.psycopg2_patcher.stop()

    def test_get_sightings_by_shape(self):
        """Test get_sightings_by_shape success path."""
        self.mock_cursor.description = [('col1',), ('ufo_shape',), ('col3',)]
        self.mock_cursor.fetchall.return_value = [('a', 'circle', 'b'), ('c', 'circle', 'd')]

        data_source = DataSource()
        results = data_source.get_sightings_by_shape('Circle')

        self.mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM ufo WHERE LOWER(ufo_shape) = %s",
            ('circle',)
        )
        self.assertEqual(results, mock_shape_results)
        self.mock_cursor.close.assert_called_once()

    def test_get_sightings_by_year(self):
        """Test get_sightings_by_year success path."""
        self.mock_cursor.description = [('col1',), ('ufo_date',), ('col3',)]
        self.mock_cursor.fetchall.return_value = [('x', '2000-10-10', 'y'), ('z', '2000-11-11', 'w')]

        data_source = DataSource()
        results = data_source.get_sightings_by_year(2000)

        self.mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM ufo WHERE EXTRACT(YEAR FROM ufo_date) = %s",
            (2000,)
        )
        self.assertEqual(results, mock_year_results)
        self.mock_cursor.close.assert_called_once()

    def test_get_top_n_years(self):
        """Test get_top_n_years success path."""
        self.mock_cursor.fetchall.return_value = mock_top_years

        data_source = DataSource()
        results = data_source.get_top_n_years(3)

        self.mock_cursor.execute.assert_called_once()
        self.assertEqual(results, mock_top_years)
        self.mock_cursor.close.assert_called_once()

    def test_get_top_n_shapes(self):
        """Test get_top_n_shapes success path."""
        self.mock_cursor.fetchall.return_value = mock_top_shapes

        data_source = DataSource()
        results = data_source.get_top_n_shapes(3)

        self.mock_cursor.execute.assert_called_once()
        self.assertEqual(results, mock_top_shapes)
        self.mock_cursor.close.assert_called_once()

    def test_query_error_handling(self):
        """Test error handling for all query methods."""
        self.mock_cursor.execute.side_effect = self.mock_psycopg2.Error("Query failed")
        data_source = DataSource()

        methods_to_test = [
            ('get_sightings_by_shape', ('circle',)),
            ('get_sightings_by_year', (2000,)),
            ('get_top_n_years', (3,)),
            ('get_top_n_shapes', (3,))
        ]

        for method_name, args in methods_to_test:
            method = getattr(data_source, method_name)
            result = method(*args)
            self.assertIsNone(result)
            self.mock_cursor.close.assert_called()

if __name__ == '__main__':
    unittest.main()
