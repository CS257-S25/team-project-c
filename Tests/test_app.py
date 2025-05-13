"""Test for Flask app."""
from app import app
import unittest
import sys
import os
from unittest.mock import patch
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)


mock_data_app = [
    {
        'datetime': '10/10/1999 20:30',
        'city': 'test city 1',
        'state': 'XX',
        'shape': 'triangle',
        'duration': '5 mins',
        'comments': 'test comment 1'
    },
    {
        'datetime': '11/11/1999 21:00',
        'city': 'test city 2',
        'state': 'YY',
        'shape': 'circle',
        'duration': '10 mins',
        'comments': 'test comment 2'
    },
    {
        'datetime': '12/12/2000 22:00',
        'city': 'test city 3',
        'state': 'ZZ',
        'shape': 'circle',
        'duration': '1 hour',
        'comments': 'test comment 3'
    }
]

class FlaskAppTests(unittest.TestCase):
    """Unit tests for the Flask app."""

    def setUp(self):
        """Set up a test client before each test."""
        self.client = app.test_client()
        app.testing = True

    back_link_text = b"<a href='/'>Back to Homepage</a>"
    top_data_link_text = b"<code>/sightings/topdata</code>"

    @patch('ProductionCode.processor.get_sightings_by_year', return_value=mock_data_app[:2])
    def test_sightings_by_valid_year(self, mock_get_year):
        """Test valid year returns table, count, and back link."""
        response = self.client.get('/sightings/year/1999')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<table', response.data)
        self.assertIn(b'<h3>Total Results: 2</h3>', response.data)
        self.assertIn(b'test city 1', response.data)
        self.assertIn(b'test city 2', response.data)
        self.assertNotIn(b'test city 3', response.data)
        self.assertIn(self.back_link_text, response.data)
        mock_get_year.assert_called_once_with(1999)

    @patch('ProductionCode.processor.get_sightings_by_year', return_value=[])
    def test_sightings_by_invalid_year(self, mock_get_year):
        """Test invalid year gives message, count 0, and back link."""
        response = self.client.get('/sightings/year/1000')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h3>Total Results: 0</h3>', response.data)
        self.assertIn(b'No sightings found for the year 1000', response.data)
        self.assertIn(self.back_link_text, response.data)
        mock_get_year.assert_called_once_with(1000)

    @patch('ProductionCode.processor.get_sightings_by_shape',
           return_value=[mock_data_app[1], mock_data_app[2]])
    def test_sightings_by_valid_shape(self, mock_get_shape):
        """Test valid shape returns table, count, and back link."""
        response = self.client.get('/sightings/shape/circle')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<table', response.data)
        self.assertIn(b'<h3>Total Results: 2</h3>', response.data)
        self.assertNotIn(b'triangle', response.data)
        self.assertIn(b'test city 2', response.data)
        self.assertIn(b'test city 3', response.data)
        self.assertIn(self.back_link_text, response.data)
        mock_get_shape.assert_called_once_with('circle')

    @patch('ProductionCode.processor.get_sightings_by_shape', return_value=[])
    def test_sightings_by_invalid_shape(self, mock_get_shape):
        """Test invalid shape gives message, count 0, and back link."""
        response = self.client.get('/sightings/shape/unknownshape')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h3>Total Results: 0</h3>', response.data)
        self.assertIn(b"No sightings found for shape 'unknownshape'", response.data)
        self.assertIn(self.back_link_text, response.data)
        mock_get_shape.assert_called_once_with('unknownshape')

    def test_homepage(self):
        """Test homepage loads and includes topdata link."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the UFO Sightings App', response.data)
        self.assertIn(b'/sightings/year/', response.data)
        self.assertIn(b'/sightings/shape/', response.data)
        self.assertIn(self.top_data_link_text, response.data)

    def test_404_error(self):
        """Test 404 page includes topdata link and back link."""
        response = self.client.get('/thispagedoesnotexist')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404 - Page Not Found', response.data)
        self.assertIn(b'Oops, invalid URL!', response.data)
        self.assertIn(self.top_data_link_text, response.data)
        self.assertIn(self.back_link_text, response.data)

    @patch('ProductionCode.processor.get_top_years')
    @patch('ProductionCode.processor.get_top_shapes')
    def test_topdata_route(self, mock_get_shapes, mock_get_years):
        """Test the /sightings/topdata route."""
        mock_get_years.return_value = [(1999, 10), (2005, 8)]
        mock_get_shapes.return_value = [('circle', 20), ('light', 15)]

        response = self.client.get('/sightings/topdata')
        self.assertEqual(response.status_code, 200)
        mock_get_years.assert_called_once_with(5)
        mock_get_shapes.assert_called_once_with(5)
        self.assertIn(b'Top 5 Years by Sightings', response.data)
        self.assertIn(b'<li>1999: 10 sightings</li>', response.data)
        self.assertIn(b'Top 5 Shapes by Sightings', response.data)
        self.assertIn(b'<li>circle: 20 sightings</li>', response.data)
        self.assertIn(self.back_link_text, response.data)

    @patch('ProductionCode.processor.get_top_years', return_value=None)
    @patch('ProductionCode.processor.get_top_shapes', return_value=None)
    def test_topdata_route_db_error(self, _mock_get_shapes, _mock_get_years):
        """Test the /sightings/topdata route when DB calls return None."""
        response = self.client.get('/sightings/topdata')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error retrieving data.', response.data)
        self.assertIn(self.back_link_text, response.data)

if __name__ == '__main__':
    unittest.main()
