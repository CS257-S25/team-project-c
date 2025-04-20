import csv


def _separate_place(place_str):
    """
    Separate the place string into city and state.
    """
    parts = [p.strip() for p in place_str.split(',')]
    if len(parts) == 2:
        city = parts[0].lower()
        state_country = parts[1].split(' ')[0].lower()
        return city, state_country
    return None, None

def _get_sighting_year(sighting):
    """
    Extracts the year from the sighting's datetime.
    """
    return sighting.get('datetime', '').split('/')[2]

def _get_sighting_place_parts(sighting):
    """
    Extracts the city and state from the sighting's place.
    """
    place_str = sighting.get('place', '')
    return _separate_place(place_str)

def filter_by_place_year(data, place, year):
    """
    Filters UFO sightings by place and year.

    """
    results = []
    current_city, current_state = _separate_place(place)

    if current_city is None or current_state is None:
        return results

    for sighting in data:
        sighting_year = _get_sighting_year(sighting)
        sighting_city, sighting_state = _get_sighting_place_parts(sighting)

        if sighting_city == sighting_city and \
           sighting_state == sighting_state and \
           sighting_year == year:
            results.append(sighting)
    return results

def filter_by_shape(data, shape):
    """
    Filters UFO sightings by shape.
    """
    results = []
    sighting_shape = shape.lower()
    for sighting in data:
        if sighting.get('shape', '').lower() == sighting_shape:
            results.append(sighting)
    return results

if __name__ == '__main__':
    ufo_data = load_ufo_data() 
    if ufo_data:
        print("\nSightings in Lawrence, Kansas in 1981:")
        lawrence_sightings = filter_by_place_year(ufo_data, "Lawrence, Kansas", "1981")
        for sighting in lawrence_sightings:
            print(sighting)

        print("\nCircle shaped sightings:")
        circle_sightings = filter_by_shape(ufo_data, "circle")
        for sighting in circle_sightings:
            print(sighting)