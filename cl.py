import argparse
from ProductionCode.processor import (
    get_sightings_by_shape,
    get_sightings_by_year,
    display_results
)

def main():
    parser = argparse.ArgumentParser(description="UFO Sightings CLI Tool")
    parser.add_argument('--shape', type=str, help='Filter sightings by UFO shape (e.g. "circle")')
    parser.add_argument('--year', type=int, help='Filter sightings by year, from 1941 to 2013')
    args = parser.parse_args()

    if args.shape:
        results = get_sightings_by_shape(args.shape)
    elif args.year:
        results = get_sightings_by_year(args.year)
    else:
        print("Please use existing arguments to filter the data.\n"
              "You can filter by shape:\n  python3 cl.py --shape \"circle\"\n"
              "Or filter by year:\n  python3 cl.py --year 1981")
        return


    display_results(results)

if __name__ == "__main__":
    main()