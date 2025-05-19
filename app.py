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

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Handle search requests and display results."""
    results = None
    count = 0
    
    if request.method == 'POST':
        search_type = request.form.get('search_type')
        search_term = request.form.get('search_term')
        
        if search_type == 'shape':
            results = processor.get_sightings_by_shape(search_term)
            if not results:
                abort(404)
        elif search_type == 'year':
            try:
                year = int(search_term)
                if 1941 <= year <= 2013:
                    results = processor.get_sightings_by_year(year)
                    if not results:
                        abort(404)
                else:
                    abort(404)
            except ValueError:
                abort(404)
        
        if results:
            count = len(results)
    
    return render_template('search.html', results=results, count=count)

@app.route('/topdata')
def topdata():
    """Display top years and shapes data."""
    top_years = processor.get_top_years(10)  # Get top 10 years
    top_shapes = processor.get_top_shapes(10)  # Get top 10 shapes
    return render_template('topdata.html', top_years=top_years, top_shapes=top_shapes)

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port=8000)
