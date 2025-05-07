"""Tests for the command line interface (cl.py)."""

import unittest
import sys
from unittest.mock import patch
from io import StringIO
import cl
from ProductionCode.processor import display_results, get_sightings_by_shape, get_sightings_by_year


class TestCLIMethodsSimplified(unittest.TestCase):
    """Simplified unit tests for the command line interface."""

    def setUp(self):
        """Redirect stdout."""
        self._stdout = sys.stdout
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        """Restore original stdout."""
        sys.stdout = self._stdout

    @patch('ProductionCode.processor.get_sightings_by_shape', return_value=[{'shape': 'circle', 'location': 'here'}])
    @patch('ProductionCode.processor.display_results')
    @patch('sys.argv', ['cl.py', '--shape', 'circle'])
    def test_main_with_shape(self, mock_display, mock_get_shape):
        """Test CLI with --shape argument."""
        cl.main()
        mock_get_shape.assert_called_once_with('circle')
        mock_display.assert_called_once_with([{'shape': 'circle', 'location': 'here'}])
        self.assertEqual(self.held_output.getvalue(), "")

    @patch('ProductionCode.processor.get_sightings_by_year', return_value=[{'year': 2000, 'place': 'there'}])
    @patch('ProductionCode.processor.display_results')
    @patch('sys.argv', ['cl.py', '--year', '2000'])
    def test_main_with_year(self, mock_display, mock_get_year):
        """Test CLI with --year argument."""
        cl.main()
        mock_get_year.assert_called_once_with(2000)
        mock_display.assert_called_once_with([{'year': 2000, 'place': 'there'}])
        self.assertEqual(self.held_output.getvalue(), "")

    @patch('sys.argv', ['cl.py'])
    def test_main_no_arguments_prints_usage(self):
        """Test CLI with no arguments prints usage message."""
        cl.main()
        output = self.held_output.getvalue()
        self.assertIn("Please use existing arguments to filter the data.", output)
        self.assertIn("You can filter by shape:", output)
        self.assertIn("Or filter by year:", output)

    @patch('ProductionCode.processor.display_results')
    @patch('sys.argv', ['cl.py', '--shape', 'triangle'])
    def test_main_calls_display_results_shape(self, mock_display):
        """Test CLI calls display_results when filtering by shape."""
        # We don't need to check the return value of get_sightings_by_shape here,
        # just that display_results is called.
        cl.main()
        mock_display.assert_called_once()
        self.assertEqual(self.held_output.getvalue(), "")

    @patch('ProductionCode.processor.display_results')
    @patch('sys.argv', ['cl.py', '--year', '1970'])
    def test_main_calls_display_results_year(self, mock_display):
        """Test CLI calls display_results when filtering by year."""
        # Similar to the shape test, just check if display_results is called.
        cl.main()
        mock_display.assert_called_once()
        self.assertEqual(self.held_output.getvalue(), "")


class TestProcessorFunctionsSimplified(unittest.TestCase):
    """Simplified unit tests for processor functions."""

    def setUp(self):
        """Prepare a mock DataSource."""
        self.mock_data_source = unittest.mock.Mock()

    def test_get_sightings_by_shape_calls_datasource(self):
        """Test get_sightings_by_shape calls the DataSource method."""
        get_sightings_by_shape('disk')
        self.mock_data_source.get_sightings_by_shape.assert_called_once_with('disk')

    def test_get_sightings_by_year_calls_datasource(self):
        """Test get_sightings_by_year calls the DataSource method."""
        get_sightings_by_year(1960)
        self.mock_data_source.get_sightings_by_year.assert_called_once_with(1960)

    def test_display_results_prints_list(self):
        """Test display_results prints each item in the list."""
        results_to_display = [{'item': 1}, {'item': 'two'}]
        with patch('sys.stdout', new_callable=StringIO) as stdout:
            display_results(results_to_display)
            output = stdout.getvalue()
            self.assertIn("{'item': 1}", output)
            self.assertIn("{'item': 'two'}", output)

    def test_display_results_handles_empty_list(self):
        """Test display_results handles an empty list."""
        with patch('sys.stdout', new_callable=StringIO) as stdout:
            display_results([])
            output = stdout.getvalue().strip()
            self.assertEqual(output, "No sightings found matching your query, please try again with different parameters.")

if __name__ == '__main__':
    unittest.main()
