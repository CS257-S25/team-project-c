"""Tests for the command line interface (cl.py) and processor.py standalone functions."""

import unittest
import sys
from unittest.mock import patch, Mock
from io import StringIO
import cl
from ProductionCode.processor import display_results, get_sightings_by_shape, get_sightings_by_year, get_top_years, get_top_shapes, DataSource
from ProductionCode import psql_config as config
import psycopg2 # Needed for mocking

# Sample data
mock_shape_results = [{'shape': 'circle', 'city': 'Testville', 'ufoshaped': 'circle'}]
mock_year_results = [{'year': 2000, 'city': 'Testburg', 'ufo_date': '2000-01-01'}]
mock_empty_results = []

class TestUFOProcessing(unittest.TestCase):
    """Combined tests for cl.py and processor.py using Mocks."""

    def setUp(self):
        """Redirect stdout to capture print statements."""
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        """Restore stdout."""
        sys.stdout = sys.__stdout__

    @patch('ProductionCode.processor.DataSource')
    def test_cl_main_with_shape_arg(self, mock_data_source_class):
        """Test CLT with --shape argument."""
        mock_instance = Mock()
        mock_instance.get_sightings_by_shape.return_value = mock_shape_results
        mock_data_source_class.return_value = mock_instance
        with patch('sys.argv', ['cl.py', '--shape', 'circle']):
            cl.main()
        output = self.held_output.getvalue()
        self.assertIn(str(mock_shape_results[0]), output)
        mock_data_source_class.assert_called_once()
        mock_instance.get_sightings_by_shape.assert_called_once_with('circle')

    @patch('ProductionCode.processor.DataSource')
    def test_cl_main_with_year_arg(self, mock_data_source_class):
        """Test CLT with --year argument."""
        mock_instance = Mock()
        mock_instance.get_sightings_by_year.return_value = mock_year_results
        mock_data_source_class.return_value = mock_instance
        with patch('sys.argv', ['cl.py', '--year', '2000']):
            cl.main()
        output = self.held_output.getvalue()
        self.assertIn(str(mock_year_results[0]), output)
        mock_data_source_class.assert_called_once()
        mock_instance.get_sightings_by_year.assert_called_once_with(2000)

    @patch('ProductionCode.processor.DataSource')
    def test_cl_main_with_shape_no_results(self, mock_data_source_class):
        """Test CLT with --shape argument and no results."""
        mock_instance = Mock()
        mock_instance.get_sightings_by_shape.return_value = mock_empty_results
        mock_data_source_class.return_value = mock_instance
        with patch('sys.argv', ['cl.py', '--shape', 'nosuchshape']):
            cl.main()
        output = self.held_output.getvalue()
        self.assertIn("No sightings found matching your query", output)
        mock_data_source_class.assert_called_once()
        mock_instance.get_sightings_by_shape.assert_called_once_with('nosuchshape')

    def test_cl_main_no_arguments(self):
        """Test CLT with no arguments prints usage."""
        with patch('sys.argv', ['cl.py']):
            cl.main()
        output = self.held_output.getvalue()
        self.assertIn("Please use existing arguments to filter the data.", output)

    def test_cl_main_invalid_argument(self):
        """Test CLT with an invalid argument (via argparse error handling)."""
        with patch('sys.argv', ['cl.py', '--nonexistentarg', 'value']), \
             patch('sys.stderr', new_callable=StringIO):
            with self.assertRaises(SystemExit):
                cl.main()

    @patch('ProductionCode.processor.DataSource')
    def test_get_sightings_by_shape_calls_datasource(self, mock_data_source_class):
        """Test standalone get_sightings_by_shape instantiates DataSource and calls its method."""
        mock_instance = Mock()
        mock_instance.get_sightings_by_shape.return_value = mock_shape_results
        mock_data_source_class.return_value = mock_instance
        result = get_sightings_by_shape('circle')
        self.assertEqual(result, mock_shape_results)
        mock_data_source_class.assert_called_once()
        mock_instance.get_sightings_by_shape.assert_called_once_with('circle')

    @patch('ProductionCode.processor.DataSource')
    def test_get_sightings_by_year_calls_datasource(self, mock_data_source_class):
        """Test standalone get_sightings_by_year instantiates DataSource and calls its method."""
        mock_instance = Mock()
        mock_instance.get_sightings_by_year.return_value = mock_year_results
        mock_data_source_class.return_value = mock_instance
        result = get_sightings_by_year(2000)
        self.assertEqual(result, mock_year_results)
        mock_data_source_class.assert_called_once()
        mock_instance.get_sightings_by_year.assert_called_once_with(2000)

    def test_display_results_with_data(self):
        """Test display_results prints data correctly."""
        display_results(mock_shape_results)
        output = self.held_output.getvalue()
        self.assertIn(str(mock_shape_results[0]), output)

    def test_display_results_empty(self):
        """Test display_results handles empty list."""
        display_results(mock_empty_results)
        output = self.held_output.getvalue()
        self.assertIn("No sightings found matching your query", output)

    @patch('ProductionCode.processor.DataSource')
    def test_get_top_years_calls_datasource(self, mock_data_source_class):
        """Test standalone get_top_years instantiates DataSource and calls its method."""
        mock_instance = Mock()
        mock_top_years_result = [(1999, 10), (2005, 8)] # Sample return data
        mock_instance.get_top_n_years.return_value = mock_top_years_result
        mock_data_source_class.return_value = mock_instance

        num_years = 2
        result = get_top_years(num_years) # Call the standalone function

        self.assertEqual(result, mock_top_years_result)
        mock_data_source_class.assert_called_once()
        mock_instance.get_top_n_years.assert_called_once_with(num_years)

    @patch('ProductionCode.processor.DataSource')
    def test_get_top_shapes_calls_datasource(self, mock_data_source_class):
        """Test standalone get_top_shapes instantiates DataSource and calls its method."""
        mock_instance = Mock()
        mock_top_shapes_result = [('circle', 25), ('light', 20)] # Sample return data
        mock_instance.get_top_n_shapes.return_value = mock_top_shapes_result
        mock_data_source_class.return_value = mock_instance

        num_shapes = 2
        result = get_top_shapes(num_shapes) # Call the standalone function

        self.assertEqual(result, mock_top_shapes_result)
        mock_data_source_class.assert_called_once()
        mock_instance.get_top_n_shapes.assert_called_once_with(num_shapes)

# --- New Test Class for DataSource ---
@patch('ProductionCode.processor.psycopg2') # Mock the entire psycopg2 module
class TestDataSourceMethods(unittest.TestCase):
    """Tests for the DataSource class methods in processor.py."""

    # Patch config for all tests in this class if needed, or rely on imported config
    # @patch('ProductionCode.processor.config') 

    def test_connect_success(self, mock_psycopg2):
        """Test successful database connection."""
        # Arrange: Configure the mock connect method to return a mock connection
        mock_connection = Mock()
        mock_psycopg2.connect.return_value = mock_connection
        
        # Act: Instantiate DataSource (which calls connect)
        # We need to bypass the __init__ connection to test connect directly,
        # or test the __init__ process itself. Let's test __init__.
        data_source = DataSource()

        # Assert: Check psycopg2.connect was called correctly
        mock_psycopg2.connect.assert_called_once_with(
            database=config.DATABASE,
            user=config.USER,
            password=config.PASSWORD,
            host="localhost"
        )
        # Assert: The instance has the connection object
        self.assertEqual(data_source.connection, mock_connection)

    def test_connect_failure(self, mock_psycopg2):
        """Test database connection failure."""
        # Arrange: Configure mock connect to raise an error
        mock_psycopg2.Error = psycopg2.Error # Need to mock the Error class too
        mock_psycopg2.connect.side_effect = mock_psycopg2.Error("Connection failed")
        
        # Act & Assert: Check that sys.exit is called on connection error
        with patch('sys.exit') as mock_exit, \
             patch('builtins.print') as mock_print: # Also mock print to check output
            DataSource() # Instantiation calls connect which should fail and exit
            mock_exit.assert_called_once_with(1)
            # Check that the specific error message was printed
            # The exact error object might be tricky to match, matching the text is safer
            mock_print.assert_any_call("Connection error: ", mock_psycopg2.connect.side_effect)


    # --- Tests for get_sightings_by_shape ---
    def test_get_sightings_by_shape_success(self, mock_psycopg2):
        """Test get_sightings_by_shape success path."""
        # Arrange: Mock connection and cursor
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        
        # Simulate successful connection in __init__ before testing the method
        mock_psycopg2.connect.return_value = mock_connection 
        
        mock_cursor.description = [('col1',), ('ufo_shape',), ('col3',)]
        mock_cursor.fetchall.return_value = [('a', 'circle', 'b'), ('c', 'circle', 'd')]
        
        # Act: Instantiate DataSource and call method
        data_source = DataSource() # __init__ uses mocked connect
        shape_to_find = 'Circle'
        results = data_source.get_sightings_by_shape(shape_to_find)

        # Assert: Check query execution and formatting
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
        # Arrange: Mock connection and cursor, make execute raise error
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_psycopg2.connect.return_value = mock_connection # Mock successful connection first
        mock_psycopg2.Error = psycopg2.Error # Mock the Error class
        mock_cursor.execute.side_effect = mock_psycopg2.Error("Shape query failed")

        # Act: Instantiate DataSource and call method
        data_source = DataSource()
        # Capture print output
        with patch('builtins.print') as mock_print:
            results = data_source.get_sightings_by_shape('any_shape')

        # Assert: Check return value is None, cursor closed, and error printed
        self.assertIsNone(results)
        mock_cursor.close.assert_called_once()
        mock_print.assert_called_with("Error fetching sightings by shape: ", mock_cursor.execute.side_effect)

    # --- Tests for get_sightings_by_year ---
    def test_get_sightings_by_year_success(self, mock_psycopg2):
        """Test get_sightings_by_year success path."""
        # Arrange
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_psycopg2.connect.return_value = mock_connection
        mock_cursor.description = [('col1',), ('ufo_date',), ('col3',)]
        mock_cursor.fetchall.return_value = [('x', '2000-10-10', 'y'), ('z', '2000-11-11', 'w')]
        
        # Act
        data_source = DataSource()
        year_to_find = 2000
        results = data_source.get_sightings_by_year(year_to_find)

        # Assert
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
        # Arrange
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_psycopg2.connect.return_value = mock_connection
        mock_psycopg2.Error = psycopg2.Error
        mock_cursor.execute.side_effect = mock_psycopg2.Error("Year query failed")

        # Act
        data_source = DataSource()
        with patch('builtins.print') as mock_print:
            results = data_source.get_sightings_by_year(1999)

        # Assert
        self.assertIsNone(results)
        mock_cursor.close.assert_called_once()
        mock_print.assert_called_with("Error fetching sightings by year: ", mock_cursor.execute.side_effect)

    # --- Tests for get_top_n_years ---
    def test_get_top_n_years_success(self, mock_psycopg2):
        """Test get_top_n_years success path."""
        # Arrange
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_psycopg2.connect.return_value = mock_connection
        # Note: For aggregate queries, cursor.description might not be needed
        # if the function doesn't call _format_results, but fetchall directly.
        # Here, get_top_n_years fetches tuples directly.
        mock_cursor.fetchall.return_value = [(1999, 50), (2001, 45), (1995, 40)]
        
        # Act
        data_source = DataSource()
        n = 3
        results = data_source.get_top_n_years(n)

        # Assert
        # Ensure the query in the test matches the one in processor.py
        expected_query_fragment_select = "SELECT EXTRACT(YEAR FROM ufo_date)::INTEGER AS year, COUNT(*) AS count"
        expected_query_fragment_from = "FROM ufo"
        expected_query_fragment_where = "WHERE ufo_date IS NOT NULL"
        expected_query_fragment_group = "GROUP BY year"
        expected_query_fragment_order = "ORDER BY count DESC"
        expected_query_fragment_limit = "LIMIT %s"
        
        call_args, _ = mock_cursor.execute.call_args
        actual_query = ' '.join(call_args[0].split()) # Normalize whitespace
        
        self.assertIn(expected_query_fragment_select, actual_query)
        self.assertIn(expected_query_fragment_from, actual_query)
        self.assertIn(expected_query_fragment_where, actual_query)
        self.assertIn(expected_query_fragment_group, actual_query)
        self.assertIn(expected_query_fragment_order, actual_query)
        self.assertIn(expected_query_fragment_limit, actual_query)
        self.assertEqual(call_args[1], (n,)) # Check the parameter
        
        self.assertEqual(results, [(1999, 50), (2001, 45), (1995, 40)])
        mock_cursor.close.assert_called_once()

    def test_get_top_n_years_error(self, mock_psycopg2):
        """Test get_top_n_years on query error."""
        # Arrange
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_psycopg2.connect.return_value = mock_connection
        mock_psycopg2.Error = psycopg2.Error
        mock_cursor.execute.side_effect = mock_psycopg2.Error("Top years query failed")

        # Act
        data_source = DataSource()
        n = 5
        with patch('builtins.print') as mock_print:
            results = data_source.get_top_n_years(n)

        # Assert
        self.assertIsNone(results)
        mock_cursor.close.assert_called_once()
        mock_print.assert_called_with(f"Error fetching top {n} years: ", mock_cursor.execute.side_effect)

    # --- Tests for get_top_n_shapes ---
    def test_get_top_n_shapes_success(self, mock_psycopg2):
        """Test get_top_n_shapes success path."""
        # Arrange
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_psycopg2.connect.return_value = mock_connection
        mock_cursor.fetchall.return_value = [('light', 100), ('circle', 90), ('triangle', 80)]
        
        # Act
        data_source = DataSource()
        n = 3
        results = data_source.get_top_n_shapes(n)

        # Assert
        # Ensure the query in the test matches the one in processor.py 
        expected_query_fragment_select = "SELECT LOWER(ufo_shape) AS shape, COUNT(*) AS count" # Updated based on error
        expected_query_fragment_from = "FROM ufo"
        expected_query_fragment_where = "WHERE ufo_shape IS NOT NULL AND TRIM(LOWER(ufo_shape)) != ''" # Updated based on error
        expected_query_fragment_group = "GROUP BY shape"
        expected_query_fragment_order = "ORDER BY count DESC"
        expected_query_fragment_limit = "LIMIT %s"

        call_args, _ = mock_cursor.execute.call_args
        actual_query = ' '.join(call_args[0].split()) # Normalize whitespace

        self.assertIn(expected_query_fragment_select, actual_query)
        self.assertIn(expected_query_fragment_from, actual_query)
        self.assertIn(expected_query_fragment_where, actual_query)
        self.assertIn(expected_query_fragment_group, actual_query)
        self.assertIn(expected_query_fragment_order, actual_query)
        self.assertIn(expected_query_fragment_limit, actual_query)
        self.assertEqual(call_args[1], (n,))

        self.assertEqual(results, [('light', 100), ('circle', 90), ('triangle', 80)])
        mock_cursor.close.assert_called_once()

    def test_get_top_n_shapes_error(self, mock_psycopg2):
        """Test get_top_n_shapes on query error."""
        # Arrange
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_psycopg2.connect.return_value = mock_connection
        mock_psycopg2.Error = psycopg2.Error
        mock_cursor.execute.side_effect = mock_psycopg2.Error("Top shapes query failed")

        # Act
        data_source = DataSource()
        n = 5
        with patch('builtins.print') as mock_print:
            results = data_source.get_top_n_shapes(n)

        # Assert
        self.assertIsNone(results)
        mock_cursor.close.assert_called_once()
        mock_print.assert_called_with(f"Error fetching top {n} shapes: ", mock_cursor.execute.side_effect)


    # --- Test for _format_results (helper method) ---
    # Note: _format_results is implicitly tested by the success cases above,
    # but we can add direct tests for edge cases if needed.
    def test_format_results_direct(self, mock_psycopg2): 
        """Test the _format_results helper method directly."""
        # Arrange: Create a mock cursor with description and data
        mock_cursor = Mock()
        mock_cursor.description = [('id',), ('city',), ('comments',)]
        mock_cursor.fetchall.return_value = [
            (1, 'city1', 'comment1'),
            (2, 'city2', None) # Test with None value
        ]
        
        # Act: Instantiate DataSource (need an instance to call the method)
        # We need a mock connection to instantiate DataSource
        mock_connection = Mock()
        mock_psycopg2.connect.return_value = mock_connection
        data_source = DataSource() 
        results = data_source._format_results(mock_cursor) # Call directly

        # Assert: Check the formatted list of dictionaries
        expected_results = [
            {'id': 1, 'city': 'city1', 'comments': 'comment1'},
            {'id': 2, 'city': 'city2', 'comments': None}
        ]
        self.assertEqual(results, expected_results)

    def test_format_results_empty_direct(self, mock_psycopg2):
        """Test _format_results with empty fetchall result directly."""
        # Arrange
        mock_cursor = Mock()
        mock_cursor.description = [('id',), ('city',)] # Need description even if no rows
        mock_cursor.fetchall.return_value = [] # Empty results
        
        # Act
        mock_connection = Mock()
        mock_psycopg2.connect.return_value = mock_connection
        data_source = DataSource()
        results = data_source._format_results(mock_cursor)

        # Assert
        self.assertEqual(results, []) # Expect an empty list


if __name__ == '__main__':
    unittest.main()
