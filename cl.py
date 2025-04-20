'''
The eventual location for the command line interface (CLI) for the project.
This will be the entry point for the project when run from the command line.
'''

# cl.py
import argparse
from ProductionCode.ufo_data_processor import load_ufo_data, filter_by_place_year, filter_by_shape

def display_sightings(sightings, search_criteria):
    """
    Displays the UFO sightings based on the search criteria.

    Args:
        sightings (list): A list of UFO sighting dictionaries to display.
        search_criteria (str): A string describing the search performed.
    """
    if sightings:
        print(f"UFO sightings found for {search_criteria}:")
        for sighting in sightings:
            print(sighting)
    else:
        print(f"No UFO sightings found for {search_criteria}.")

def handle_place_year_search(args, ufo_data):
    """
    Handles the command-line arguments for searching by place and year.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
        ufo_data (list): The loaded UFO sighting data.
    """
    if args.year:
        results = filter_by_place_year(ufo_data, args.place, args.year)
        display_sightings(results, f"place '{args.place}' and year '{args.year}'")
    else:
        print("Error: When searching by place, you must also specify a year using --year.")

def handle_shape_search(args, ufo_data):
    """
    Handles the command-line arguments for searching by shape.

    Args:
        args (argparse.Namespace): The parsed command-line arguments.
        ufo_data (list): The loaded UFO sighting data.
    """
    results = filter_by_shape(ufo_data, args.shape)
    display_sightings(results, f"shape '{args.shape}'")

def main():
    parser = argparse.ArgumentParser(description="Search UFO sightings data.")
    parser.add_argument("data_file", help="Path to the UFO sightings CSV file.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--place", help='Search by place (e.g., "City, State").')
    group.add_argument("--shape", help="Search by UFO shape.")

    parser.add_argument("--year", help="Filter by year (if searching by place).")

    args = parser.parse_args()

    ufo_data = load_ufo_data(args.data_file)

    if ufo_data:
        if args.place:
            handle_place_year_search(args, ufo_data)
        elif args.shape:
            handle_shape_search(args, ufo_data)

if __name__ == "__main__":
    main()