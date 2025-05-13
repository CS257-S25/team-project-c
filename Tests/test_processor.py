"""Tests for the DataSource class in processor.py."""
import unittest
from unittest.mock import patch, Mock
import psycopg2
from ProductionCode.processor import DataSource
from ProductionCode import psql_config as config

@patch('ProductionCode.processor.psycopg2')
class TestDataSourceMethods(unittest.TestCase):
    """Tests for the DataSource class methods in processor.py."""
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

    def test_connect_failure(self, mock_psycopg2):
        """Test database connection failure."""
        mock_psycopg2.Error = psycopg2.Error
        mock_psycopg2.connect.side_effect = mock_psycopg2.Error("Connection failed")

        with patch('sys.exit') as mock_exit, \
             patch('builtins.print') as mock_print:
            DataSource()
            mock_exit.assert_called_once_with(1)
            mock_print.assert_any_call("Connection error: ", mock_psycopg2.connect.side_effect)

    def test_get_sightings_by_shape(self, mock_psycopg2):
        """Test get_sightings_by_shape success path."""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_psycopg2.connect.return_value = mock_connection

        mock_cursor.description = [('col1',), ('ufo_shape',), ('col3',)]
        mock_cursor.fetchall.return_value = [('a', 'circle', 'b'), ('c', 'circle', 'd')]

        data_source = DataSource()
        shape_to_find = 'Circle'
        results = data_source.get_sightings_by_shape(shape_to_find)

        expected_query = "SELECT * FROM ufo WHERE LOWER(ufo_shape) = %s"
        mock_cursor.execute.assert_called_once_with(expected_query, (shape_to_find.lower(),))
        expected_results = [
            {'col1': 'a', 'ufo_shape': 'circle', 'col3': 'b'},
            {'col1': 'c', 'ufo_shape': 'circle', 'col3': 'd'}
        ]
        self.assertEqual(results, expected_results)
        mock_cursor.close.assert_called_once()

    def test_get_sightings_by_shape_error(self, mock_psycopg2):
        """Test get_sightings_by_shape on query error."""
        self._test_method_error(
            mock_psycopg2,
            'get_sightings_by_shape',
            args=('any_shape',),
            error_message_fragment="Error fetching sightings by shape: "
        )

    def test_get_sightings_by_year(self, mock_psycopg2):
        """Test get_sightings_by_year success path."""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_psycopg2.connect.return_value = mock_connection
        mock_cursor.description = [('col1',), ('ufo_date',), ('col3',)]
        mock_cursor.fetchall.return_value = [('x', '2000-10-10', 'y'), ('z', '2000-11-11', 'w')]

        data_source = DataSource()
        year_to_find = 2000
        results = data_source.get_sightings_by_year(year_to_find)

        expected_query = "SELECT * FROM ufo WHERE EXTRACT(YEAR FROM ufo_date) = %s"
        mock_cursor.execute.assert_called_once_with(expected_query, (year_to_find,))
        expected_results = [
            {'col1': 'x', 'ufo_date': '2000-10-10', 'col3': 'y'},
            {'col1': 'z', 'ufo_date': '2000-11-11', 'col3': 'w'}
        ]
        self.assertEqual(results, expected_results)
        mock_cursor.close.assert_called_once()

    def test_get_sightings_by_year_error(self, mock_psycopg2):
        """Test get_sightings_by_year on query error."""
        self._test_method_error(
            mock_psycopg2,
            'get_sightings_by_year',
            args=(1999,),
            error_message_fragment="Error fetching sightings by year: "
        )

    def test_get_top_n_years(self, mock_psycopg2):
        """Test get_top_n_years success path."""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_psycopg2.connect.return_value = mock_connection
        mock_cursor.fetchall.return_value = [(1999, 50), (2001, 45), (1995, 40)]

        data_source = DataSource()
        n = 3
        results = data_source.get_top_n_years(n)

        expected_query_fragment_select = (
            "SELECT EXTRACT(YEAR FROM ufo_date)::INTEGER AS year, COUNT(*) AS count"
        )
        expected_query_fragment_from = "FROM ufo"
        expected_query_fragment_where = "WHERE ufo_date IS NOT NULL"
        expected_query_fragment_group = "GROUP BY year"
        expected_query_fragment_order = "ORDER BY count DESC"
        expected_query_fragment_limit = "LIMIT %s"

        call_args, _ = mock_cursor.execute.call_args
        actual_query = ' '.join(call_args[0].split())

        self.assertIn(expected_query_fragment_select, actual_query)
        self.assertIn(expected_query_fragment_from, actual_query)
        self.assertIn(expected_query_fragment_where, actual_query)
        self.assertIn(expected_query_fragment_group, actual_query)
        self.assertIn(expected_query_fragment_order, actual_query)
        self.assertIn(expected_query_fragment_limit, actual_query)
        self.assertEqual(call_args[1], (n,))

        self.assertEqual(results, [(1999, 50), (2001, 45), (1995, 40)])
        mock_cursor.close.assert_called_once()

    def test_get_top_n_shapes(self, mock_psycopg2):
        """Test get_top_n_shapes success path."""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_psycopg2.connect.return_value = mock_connection
        mock_cursor.fetchall.return_value = [('light', 100), ('circle', 90), ('triangle', 80)]

        data_source = DataSource()
        n = 3
        results = data_source.get_top_n_shapes(n)
        expected_query_fragment_select = (
            "SELECT LOWER(ufo_shape) AS shape, COUNT(*) AS count"
        )
        expected_query_fragment_from = "FROM ufo"
        expected_query_fragment_where = (
            "WHERE ufo_shape IS NOT NULL AND TRIM(LOWER(ufo_shape)) != ''"
        )
        expected_query_fragment_group = "GROUP BY shape"
        expected_query_fragment_order = "ORDER BY count DESC"
        expected_query_fragment_limit = "LIMIT %s"
        call_args, _ = mock_cursor.execute.call_args
        actual_query = ' '.join(call_args[0].split())

        self.assertIn(expected_query_fragment_select, actual_query)
        self.assertIn(expected_query_fragment_from, actual_query)
        self.assertIn(expected_query_fragment_where, actual_query)
        self.assertIn(expected_query_fragment_group, actual_query)
        self.assertIn(expected_query_fragment_order, actual_query)
        self.assertIn(expected_query_fragment_limit, actual_query)
        self.assertEqual(call_args[1], (n,))

        self.assertEqual(results, [('light', 100), ('circle', 90), ('triangle', 80)])
        mock_cursor.close.assert_called_once()

    def _test_method_error(self, mock_psycopg2, method_name, args):
        """Helper method to test error handling in DataSource methods."""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_psycopg2.connect.return_value = mock_connection
        mock_psycopg2.Error = psycopg2.Error
        mock_cursor.execute.side_effect = mock_psycopg2.Error("Query failed")

        data_source = DataSource()
        method = getattr(data_source, method_name)
        result = method(*args)

        self.assertIsNone(result)
        mock_cursor.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
