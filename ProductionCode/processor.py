"""Helper functions for loading and filtering UFO sightings data."""

import csv

def load_data(filepath="Data/UFO_Sightings.csv"):
    """Load UFO sightings data from a CSV file and return it as a list of dictionaries."""
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        return list(csv.DictReader(csvfile))

def display_results(results):
    """Display search results."""
    if not results:
        print("No sightings found matching your query, please try again with different parameters.")
        return    
    for row in results:
        print(row)

def filter_sightings_by_year(data,year):
    """Filter data data by year."""
    results = []
    for row in data:
        try:
            row_year = int(row['datetime'].split('/')[2].split()[0])
            if row_year == year:
                results.append(row)
        except (IndexError, ValueError):
            continue
    return results

def filter_by_shape(data, shape):
    """filter data to match the given shape."""
    results = []
    shape = shape.strip().lower()
    for row in data:
        row_shape = row['shape'].strip().lower()
        if row_shape == shape:
            results.append(row)
    return results

def get_sightings_by_shape(shape):
    """Get sightings by given shape."""
    data = load_data()
    return filter_by_shape(data, shape)

def get_sightings_by_year(year):
    """Get sightings by given year."""
    data = load_data()
    return filter_sightings_by_year(data,year)
