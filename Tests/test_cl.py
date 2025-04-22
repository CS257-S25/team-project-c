"""Test for functions in both production codes and command line tool."""
import unittest
import sys
from unittest.mock import patch, mock_open
from io import StringIO
from ProductionCode.processor import (
    load_data, display_results,
    filter_sightings_by_year, filter_by_shape,
    get_sightings_by_shape
)
import cl 

class TestProcessorMethods(unittest.TestCase):
    """Unit tests for functions in ProductionCode."""
    
    def setUp(self):
        """Redirect stdout and prepare sample UFO data for testing."""
        self.sample_data = [
            {'datetime': '10/10/1949 20:30', 'city': 'san marcos', 'shape': 'cylinder'},
            {'datetime': '10/10/1949 21:00', 'city': 'lackland afb', 'shape': 'light'},
            {'datetime': '10/10/1956 21:00', 'city': 'edna', 'shape': 'cylinder'}
        ]
        self._stdout = sys.stdout
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        """Restore original stdout."""
        sys.stdout = self._stdout

    @patch("builtins.open", new_callable=mock_open, read_data='datetime,city\na,b\n')
    def test_load_data(self, mock_file):
        """Test loading CSV data into a list of dictionaries."""
        result = load_data("test_file.csv")
        expected_result = [{'datetime': 'a', 'city': 'b'}]
        self.assertEqual(result, expected_result)
        mock_file.assert_called_with("test_file.csv", newline='', encoding='utf-8')

    def test_display_results(self):
        """Test that display_results prints each row in the data."""
        display_results(self.sample_data)
        output = self.held_output.getvalue()
        self.assertIn('san marcos', output)
        self.assertIn('lackland afb', output)
        self.assertIn('edna', output)
        self.assertEqual(output.count('{'), 3)

    def test_filter_sightings_by_year(self):
        """Test filtering sightings by year returns correct rows."""
        result_1949 = filter_sightings_by_year(self.sample_data, 1949)
        self.assertEqual(len(result_1949), 2)
        self.assertEqual({r['city'] for r in result_1949}, {'san marcos', 'lackland afb'})

        result_1956 = filter_sightings_by_year(self.sample_data, 1956)
        self.assertEqual(len(result_1956), 1)
        self.assertEqual(result_1956[0]['city'], 'edna')

        result_empty = filter_sightings_by_year(self.sample_data, 2000)
        self.assertEqual(len(result_empty), 0)

    def test_filter_by_shape(self):
        """Test filtering sightings by shape returns matching entries."""
        result_cylinder = filter_by_shape(self.sample_data, "cylinder")
        self.assertEqual(len(result_cylinder), 2)
        self.assertSetEqual({row['city'] for row in result_cylinder}, {'san marcos', 'edna'})

        result_light = filter_by_shape(self.sample_data, "light")
        self.assertEqual(len(result_light), 1)
        self.assertEqual(result_light[0]['city'], 'lackland afb')

        result_empty = filter_by_shape(self.sample_data, "disk")
        self.assertEqual(len(result_empty), 0)

    @patch("builtins.open", new_callable=mock_open, read_data=
        "datetime,city,state,shape,duration,comments\n"
        "10/10/1949 20:30,san marcos,tx,cylinder,5 mins,\"desc\"\n"
        "10/10/1956 21:00,edna,tx,cylinder,5 mins,\"desc\"\n")
    def test_get_sightings_by_shape(self, mock_file):
        """Test wrapper that loads data and filters by shape correctly."""
        result = get_sightings_by_shape("cylinder")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["shape"], "cylinder")

def test_no_arguments(self):
        """Test that the command line tool handles no arguments correctly."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('sys.argv', ['cl.py']):
                cl.main()
            output = fake_out.getvalue()
            self.assertIn("Please use existing arguments to filter the data", output)


if __name__ == '__main__':
    unittest.main()
