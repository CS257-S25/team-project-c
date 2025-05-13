"""Tests for the DataSource class in processor.py."""
from ProductionCode.processor import DataSource
from ProductionCode import psql_config as config
import unittest
import sys
from unittest.mock import patch, Mock
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
import psycopg2

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
    
    def test_format_results_direct(self, mock_psycopg2):
        """Test the _format_results helper method directly."""
        mock_connection, mock_cursor = self._setup_mocks(mock_psycopg2)
        mock_cursor.description = [('id',), ('city',), ('comments',)]
        mock_cursor.fetchall.return_value = [
            (1, 'city1', 'comment1'),
            (2, 'city2', None)
        ]
        data_source = DataSource()
        # pylint: disable=protected-access
        results = data_source._format_results(mock_cursor)
        expected_results = [
            {'id': 1, 'city': 'city1', 'comments': 'comment1'},
            {'id': 2, 'city': 'city2', 'comments': None}
        ]
        self.assertEqual(results, expected_results)

    def test_format_results_empty_direct(self, mock_psycopg2):
        """Test _format_results with empty fetchall result directly."""
        mock_connection, mock_cursor = self._setup_mocks(mock_psycopg2)
        mock_cursor.description = [('id',), ('city',)]
        mock_cursor.fetchall.return_value = []
        data_source = DataSource()
        # pylint: disable=protected-access
        results = data_source._format_results(mock_cursor)
        self.assertEqual(results, [])

if __name__ == '__main__':
    unittest.main()
