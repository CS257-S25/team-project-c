# UFO Sightings CLI Tool

Users can filter ufo sightings by year and shape.

1. Filter by Year

The dataset contains data from 1941 to 2013.
Therefore, data input must be within this range.
User statement: python3 cl.py -- year 1981

2. Shape

The dataset categories ufos into the following list and other unkown catagories.
Therefore, data input must be witin these given catagories.
User statement: python3 cl.py --shape circle

- changing
- cigar
- circle
- cylinder
- diamond
- disk
- egg
- fireball
- formation
- light
- oval
- rectangle
- sphere
- triangle
- teardrop

# Flask App

### How to Run the Flask App1

1. Run Flask App and visit http://127.0.0.1:5000/ on web browser\
2. View sightings by year: \
   vist with http://127.0.0.1:5000/sightings/year/<year>, replace <year> with integer of years\
   for example: http://127.0.0.1:5000/sightings/year/1999\
3. View sightings by Shape:\
   vist with http://127.0.0.1:5000/sightings/shape/<shape>, replace <shape> with string of shapes from the above shape list\
   for example: http://127.0.0.1:5000/sightings/shape/circle\
4. If the requested year or shape has no data, a message suggesting trying other parameters will be shown\
   If the user enters an invalid URL, a custom 404 error page will be displayed with helpful instructions.\
   All results are displayed in an HTML table format.\
