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

## Flask App

The app displays a webpage with either ufos sorted by shape with (/sightings/year/<int:year>) or sorted by year with (sightings/shape:/<string:shape>)
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
5. View most common shape or years of sightings:\
   vist with http://127.0.0.1:5000/sightings/topdata \
   top 5 years and shapes with most ufo sightings are shown.

# Database

We plan to use the location and duration in front-end deliverble, as information users can optain through their search. \
Clarification for datatype: We wish not to focus on preprocessing the orginial format of opur dataset, therefore we have to load ufo_duration as text, even though they are mostly integers, at least one is mixed with punctuation. Especially because we keep duration for front-end purpose. 

# Front-end

Our website is designed to support different user behavior patterns.

## Scanability
- Clear navigation bar with distinct sections (Home, About, Search, Top Data)
- Search page features a prominent search form with clear labels
- Results are displayed in a well-structured table format
- Search instructions are readily available on the search page
- Consistent color scheme and layout across all pages
- Clear headings and subheadings for content organization

## Satisficing
- Quick access to most common searches through the "Top Data" page
- Search form with dropdown for search type selection
- Immediate feedback on search results with total count
- Clear error messages (404 page) 
- Prominent "Start Search" and "Ranking" buttons on homepage

## Muddling Through
- Search instructions are always visible on the search page
- Available data range are clearly displayed
- 404 error page includes helpful instructions and a return button
- Clear visual hierarchy with important actions prominently displayed 
