'''The Flask app interface for the UFO sightings project.'''

from flask import Flask, render_template, request, abort
from ProductionCode import processor

app = Flask(__name__)

@app.route('/')
def homepage():
    """Display the homepage."""
    return render_template('home.html')

@app.route('/about')
def about():
    """Display the about page."""
    return render_template('about.html')

@app.route('/search', methods=['GET'])
def search():
    """Handle search requests and display results."""
    results = None
    count = 0
    search_type = request.args.get('search_type')
    year_term = request.args.get('year_term')
    shape_term = request.args.get('shape_term')
    
    print(f"Search request - Type: {search_type}, Year: {year_term}, Shape: {shape_term}")  # Debug log

    if search_type:
        if search_type == 'shape' and shape_term:
            print(f"Searching by shape: {shape_term}")  # Debug log
            results = processor.fetch_sightings_by_shape(shape_term)
            if not results:
                print(f"No results found for shape: {shape_term}")  # Debug log
                abort(404)
        elif search_type == 'year' and year_term:
            try:
                year = int(year_term)
                print(f"Searching by year: {year}")  # Debug log
                results = processor.fetch_sightings_by_year(year)
                if not results:
                    print(f"No results found for year: {year}")  # Debug log
                    abort(404)
            except ValueError:
                print(f"Invalid year format: {year_term}")  # Debug log
                abort(404)

        if results:
            count = len(results)
            print(f"Found {count} results")  # Debug log

    return render_template('search.html', results=results, count=count)

@app.route('/topdata')
def topdata():
    """Display top years and shapes data."""
    top_years_data = processor.fetch_top_years(10)  # Get top 10 years
    top_shapes_data = processor.fetch_top_shapes(10)  # Get top 10 shapes

    # Ensure top_years and top_shapes are iterables (e.g., empty lists if None)
    top_years = top_years_data if top_years_data is not None else []
    top_shapes = top_shapes_data if top_shapes_data is not None else []

    return render_template('topdata.html', top_years=top_years, top_shapes=top_shapes)

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors."""
    del error # for style unsed variable
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5151, debug=False)  # Run the app on port 5151 with debug mode enabled
