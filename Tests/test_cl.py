"""Tests for the command line interface (cl.py) and processor.py standalone functions."""
import unittest
import sys
from unittest.mock import patch, Mock
from io import StringIO
import cl

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

if __name__ == '__main__':
    unittest.main()
