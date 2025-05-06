"""Test for Flask app."""

import unittest
from app import app

class FlaskAppTests(unittest.TestCase):
    """Unit tests for the Flask app."""
    def setUp(self):
        """Set up a test client before each test."""
        self.client = app.test_client()

    def test_homepage(self):
        """Test that the homepage loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'UFO Sightings App', response.data)

    def test_sightings_by_valid_year(self):
        """Test that a valid year returns an HTML table."""
        response = self.client.get('/sightings/year/1999')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<table', response.data)

    def test_sightings_by_invalid_year(self):
        """Test that an invalid year gives a friendly message."""
        response = self.client.get('/sightings/year/1000')  # year 1000 has no data
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No sightings found for the year', response.data)

    def test_sightings_by_valid_shape(self):
        """Test that a valid shape returns an HTML table."""
        response = self.client.get('/sightings/shape/circle')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<table', response.data)

    def test_sightings_by_invalid_shape(self):
        """Test that an invalid shape gives a friendly message."""
        response = self.client.get('/sightings/shape/unknownshape')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No sightings found for shape", response.data)

    def test_404_error(self):
        """Test that a wrong URL returns the custom 404 page."""
        response = self.client.get('/thispagedoesnotexist')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404 - Page Not Found', response.data)

if __name__ == '__main__':
    unittest.main()