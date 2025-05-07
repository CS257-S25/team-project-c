"""Test for Flask app."""

import unittest
from unittest.mock import patch
import app
from ProductionCode import processor

mock_data_app = [
    {'datetime': '10/10/1999 20:30', 'city': 'test city 1', 'state': 'XX', 'shape': 'triangle', 'duration': '5 mins', 'comments': 'test comment 1'},
    {'datetime': '11/11/1999 21:00', 'city': 'test city 2', 'state': 'YY', 'shape': 'circle', 'duration': '10 mins', 'comments': 'test comment 2'},
    {'datetime': '12/12/2000 22:00', 'city': 'test city 3', 'state': 'ZZ', 'shape': 'circle', 'duration': '1 hour', 'comments': 'test comment 3'}
]

class FlaskAppTests(unittest.TestCase):
    """Unit tests for the Flask app."""
    def setUp(self):
        """Set up a test client before each test."""
        self.client = app.test_client()

    @patch('ProductionCode.processor.get_sightings_by_year', return_value=mock_data_app[:2])
    def test_sightings_by_valid_year(self, mock_get_year):
        """Test that a valid year returns an HTML table."""
        response = self.client.get('/sightings/year/1999')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<table', response.data)
        self.assertIn(b'test city 1', response.data)
        self.assertIn(b'test city 2', response.data)
        self.assertNotIn(b'test city 3', response.data)
        mock_get_year.assert_called_once_with(1999)

    @patch('ProductionCode.processor.get_sightings_by_year', return_value=[])
    def test_sightings_by_invalid_year(self, mock_get_year):
        """Test that an invalid year gives a friendly message."""
        response = self.client.get('/sightings/year/1000')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No sightings found for the year 1000', response.data)
        mock_get_year.assert_called_once_with(1000)

    @patch('ProductionCode.processor.get_sightings_by_shape', return_value=[mock_data_app[1], mock_data_app[2]])
    def test_sightings_by_valid_shape(self, mock_get_shape):
        """Test that a valid shape returns an HTML table."""
        response = self.client.get('/sightings/shape/circle')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<table', response.data)
        self.assertNotIn(b'triangle', response.data)
        self.assertIn(b'circle', response.data)
        self.assertIn(b'test city 2', response.data)
        self.assertIn(b'test city 3', response.data)
        mock_get_shape.assert_called_once_with('circle')

    @patch('ProductionCode.processor.get_sightings_by_shape', return_value=[])
    def test_sightings_by_invalid_shape(self, mock_get_shape):
        """Test that an invalid shape gives a friendly message."""
        response = self.client.get('/sightings/shape/unknownshape')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No sightings found for shape 'unknownshape'", response.data)
        mock_get_shape.assert_called_once_with('unknownshape')

    def test_homepage(self):
        """Test that the homepage loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'UFO Sightings App', response.data)
        self.assertIn(b'/sightings/year/', response.data)
        self.assertIn(b'/sightings/shape/', response.data)

    def test_404_error(self):
        """Test that a wrong URL returns the custom 404 page."""
        response = self.client.get('/thispagedoesnotexist')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404 - Page Not Found', response.data)
        self.assertIn(b'Oops, invalid URL!', response.data)

if __name__ == '__main__':
    unittest.main()