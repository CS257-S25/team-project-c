"""Test for Flask app."""
import unittest
from unittest.mock import patch
from app import app

mock_data_app = [
    {
        'ufo_date': '10/10/1999 20:30',
        'ufo_city': 'test city 1',
        'ufo_state': 'XX',
        'ufo_shape': 'triangle',
        'ufo_duration': '5 mins',
        'ufo_comment': 'test comment 1'
    },
    {
        'ufo_date': '11/11/1999 21:00',
        'ufo_city': 'test city 2',
        'ufo_state': 'YY',
        'ufo_shape': 'circle',
        'ufo_duration': '10 mins',
        'ufo_comment': 'test comment 2'
    },
    {
        'ufo_date': '12/12/2000 22:00',
        'ufo_city': 'test city 3',
        'ufo_state': 'ZZ',
        'ufo_shape': 'circle',
        'ufo_duration': '1 hour',
        'ufo_comment': 'test comment 3'
    }
]

class FlaskAppTests(unittest.TestCase):
    """Unit tests for the Flask app."""

    def setUp(self):
        """Set up a test client before each test."""
        self.client = app.test_client()
        app.testing = True

    def test_homepage(self):
        """Test homepage loads with correct content."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to UFO Sightings App', response.data)
        self.assertIn(b'Start Search', response.data)
        self.assertIn(b'Top Years/Shapes', response.data)

    def test_about_page(self):
        """Test about page loads with correct content."""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About UFO Sightings Database', response.data)
        self.assertIn(b'Dataset(s) Metadata', response.data)

    def test_search_page_get(self):
        """Test search page loads with form and instructions."""
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search UFO Sightings', response.data)
        self.assertIn(b'Search Instructions', response.data)
        self.assertIn(
        b'<strong>Year requirements:</strong> Must be between 1941 and 2013.',
                       response.data)

    @patch('ProductionCode.processor.get_sightings_by_year')
    def test_search_by_valid_year(self, mock_get_year):
        """Test search by valid year returns results."""
        mock_get_year.return_value = mock_data_app[:2]
        response = self.client.get('/search?search_type=year&search_term=1999')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search Results', response.data)
        self.assertIn(b'Total Results: 2', response.data)
        self.assertIn(b'test city 1', response.data)
        self.assertIn(b'test city 2', response.data)
        mock_get_year.assert_called_once_with(1999)

    @patch('ProductionCode.processor.get_sightings_by_shape')
    def test_search_by_valid_shape(self, mock_get_shape):
        """Test search by valid shape returns results."""
        mock_get_shape.return_value = [mock_data_app[1], mock_data_app[2]]
        response = self.client.get('/search?search_type=shape&search_term=circle')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search Results', response.data)
        self.assertIn(b'Total Results: 2', response.data)
        self.assertIn(b'test city 2', response.data)
        self.assertIn(b'test city 3', response.data)
        mock_get_shape.assert_called_once_with('circle')

    @patch('ProductionCode.processor.get_sightings_by_year')
    def test_search_by_invalid_year(self, mock_get_year):
        """Test search by invalid year returns 404."""
        mock_get_year.return_value = None
        response = self.client.get('/search?search_type=year&search_term=1000')
        self.assertEqual(response.status_code, 404)
        mock_get_year.assert_called_once_with(1000)

    @patch('ProductionCode.processor.get_sightings_by_shape')
    def test_search_by_invalid_shape(self, mock_get_shape):
        """Test search by invalid shape returns 404."""
        mock_get_shape.return_value = None
        response = self.client.get('/search?search_type=shape&search_term=unknownshape')
        self.assertEqual(response.status_code, 404)
        mock_get_shape.assert_called_once_with('unknownshape')

    def test_search_by_invalid_year_format(self):
        """Test search by invalid year format returns 404."""
        response = self.client.get('/search?search_type=year&search_term=not-a-year')
        self.assertEqual(response.status_code, 404)

    @patch('ProductionCode.processor.get_top_years')
    @patch('ProductionCode.processor.get_top_shapes')
    def test_topdata_page(self, mock_get_shapes, mock_get_years):
        """Test top data page loads with correct content."""
        mock_get_years.return_value = [(1999, 10), (2005, 8)]
        mock_get_shapes.return_value = [('circle', 20), ('light', 15)]

        response = self.client.get('/topdata')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Top UFO Sightings Data', response.data)
        self.assertIn(b'Top Years', response.data)
        self.assertIn(b'Top Shapes', response.data)
        mock_get_years.assert_called_once_with(10)
        mock_get_shapes.assert_called_once_with(10)

    @patch('ProductionCode.processor.get_top_years')
    @patch('ProductionCode.processor.get_top_shapes')
    def test_topdata_page_error(self, mock_get_shapes, mock_get_years):
        """Test top data page handles database errors."""
        mock_get_years.return_value = None
        mock_get_shapes.return_value = None

        response = self.client.get('/topdata')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Top UFO Sightings Data', response.data)
        mock_get_years.assert_called_once_with(10)
        mock_get_shapes.assert_called_once_with(10)

    def test_404_error(self):
        """Test 404 page includes search instructions and return button."""
        response = self.client.get('/thispagedoesnotexist')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404 - Page Not Found', response.data)
        self.assertIn(b'Search Instructions', response.data)
        self.assertIn(b'Return to Search', response.data)

if __name__ == '__main__':
    unittest.main()
