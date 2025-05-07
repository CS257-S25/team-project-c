"""Tests for the command line interface (cl.py) and processor.py standalone functions."""

import unittest
import sys
from unittest.mock import patch, MagicMock
from io import StringIO
import cl 
from ProductionCode.processor import display_results, get_sightings_by_shape, get_sightings_by_year

# Sample data to be returned by mocked DataSource methods
mock_shape_results = [{'shape': 'circle', 'city': 'Testville', 'ufoshaped': 'circle'}]
mock_year_results = [{'year': 2000, 'city': 'Testburg', 'ufo_date': '2000-01-01'}]
mock_empty_results = []

class TestCLIMainFunction(unittest.TestCase):
    """Tests for the main function in cl.py."""

    def setUp(self):
        """Redirect stdout to capture print statements."""
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        """Restore stdout."""
        sys.stdout = sys.__stdout__

    @patch('ProductionCode.processor.DataSource')
    def test_main_with_shape_arg(self, mock_data_source_class):
        """Test cl.main() with --shape argument."""
        # Configure the mock DataSource instance and its method
        mock_instance = MagicMock()
        mock_instance.get_sightings_by_shape.return_value = mock_shape_results
        mock_data_source_class.return_value = mock_instance

        with patch('sys.argv', ['cl.py', '--shape', 'circle']):
            cl.main()

        mock_data_source_class.assert_called_once() # Check DataSource was instantiated
        mock_instance.get_sightings_by_shape.assert_called_once_with('circle')
        output = self.held_output.getvalue()
        self.assertIn(str(mock_shape_results[0]), output)

    @patch('ProductionCode.processor.DataSource')
    def test_main_with_year_arg(self, mock_data_source_class):
        """Test cl.main() with --year argument."""
        mock_instance = MagicMock()
        mock_instance.get_sightings_by_year.return_value = mock_year_results
        mock_data_source_class.return_value = mock_instance

        with patch('sys.argv', ['cl.py', '--year', '2000']):
            cl.main()

        mock_data_source_class.assert_called_once()
        mock_instance.get_sightings_by_year.assert_called_once_with(2000)
        output = self.held_output.getvalue()
        self.assertIn(str(mock_year_results[0]), output)
        
    @patch('ProductionCode.processor.DataSource')
    def test_main_with_shape_no_results(self, mock_data_source_class):
        """Test cl.main() with --shape argument and no results."""
        mock_instance = MagicMock()
        mock_instance.get_sightings_by_shape.return_value = mock_empty_results
        mock_data_source_class.return_value = mock_instance

        with patch('sys.argv', ['cl.py', '--shape', 'nosuchshape']):
            cl.main()
        
        mock_data_source_class.assert_called_once()
        mock_instance.get_sightings_by_shape.assert_called_once_with('nosuchshape')
        output = self.held_output.getvalue()
        self.assertIn("No sightings found matching your query", output)


    def test_main_no_arguments(self):
        """Test cl.main() with no arguments prints usage."""
        with patch('sys.argv', ['cl.py']):
            cl.main()
        output = self.held_output.getvalue()
        self.assertIn("Please use existing arguments to filter the data.", output)

    def test_main_invalid_argument(self):
        """Test cl.main() with an invalid argument (via argparse error handling)."""
        # Suppress stderr for this test as argparse prints there
        with patch('sys.argv', ['cl.py', '--nonexistentarg', 'value']), \
             patch('sys.stderr', new_callable=StringIO):
            with self.assertRaises(SystemExit): # Argparse calls sys.exit on error
                cl.main()


class TestProcessorStandaloneFunctions(unittest.TestCase):
    """Tests for the standalone functions in processor.py."""

    @patch('ProductionCode.processor.DataSource')
    def test_get_sightings_by_shape_calls_datasource(self, mock_data_source_class):
        """Test standalone get_sightings_by_shape instantiates DataSource and calls its method."""
        mock_instance = MagicMock()
        mock_instance.get_sightings_by_shape.return_value = mock_shape_results
        mock_data_source_class.return_value = mock_instance # Configure what DataSource() returns

        result = get_sightings_by_shape('circle')

        mock_data_source_class.assert_called_once() # DataSource was instantiated
        mock_instance.get_sightings_by_shape.assert_called_once_with('circle')
        self.assertEqual(result, mock_shape_results)

    @patch('ProductionCode.processor.DataSource')
    def test_get_sightings_by_year_calls_datasource(self, mock_data_source_class):
        """Test standalone get_sightings_by_year instantiates DataSource and calls its method."""
        mock_instance = MagicMock()
        mock_instance.get_sightings_by_year.return_value = mock_year_results
        mock_data_source_class.return_value = mock_instance

        result = get_sightings_by_year(2000)

        mock_data_source_class.assert_called_once()
        mock_instance.get_sightings_by_year.assert_called_once_with(2000)
        self.assertEqual(result, mock_year_results)

class TestDisplayResults(unittest.TestCase):
    """Tests for the display_results function in processor.py."""

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

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

if __name__ == '__main__':
    unittest.main()
