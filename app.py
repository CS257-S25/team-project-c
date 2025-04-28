'''The Flask app interface for the UFO sightings project (HTML table version).'''

from flask import Flask
from ProductionCode import processor

app = Flask(__name__)

@app.route('/')
def homepage():
    return '''
        <h1>Welcome to the UFO Sightings App</h1>
        <p>Use the following URL patterns to view sightings data:</p>
        <ul>
            <li><code>/sightings/year/&lt;year&gt;</code>,  e.g. /sightings/year/1999</li>
            <li><code>/sightings/shape/&lt;shape&gt;</code>,  e.g. /sightings/shape/circle</li>
        </ul>
    '''

@app.route('/sightings/year/<int:year>')
def sightings_by_year(year):
    """Return UFO sightings from the given year in HTML table format."""
    results = processor.get_sightings_by_year(year)
    if not results:
        return f"<p>No sightings found for the year {year}, please try other .</p>"
    return render_results(f"Sightings from {year}", results)

@app.route('/sightings/shape/<string:shape>')
def sightings_by_shape(shape):
    """Return UFO sightings with the given shape in HTML table format."""
    results = processor.get_sightings_by_shape(shape)
    if not results:
        return f"<p>No sightings found for shape '{shape}'.</p>"
    return render_results(f"Sightings of shape '{shape}'", results)

def render_results(title, results):
    """Render results in an HTML table."""
    table = table_constructor(results)
    return f"<h2>{title}</h2>" + table

def table_constructor(results):
    """Construct an HTML table from the data."""
    header_row = "".join(f"<th>{key}</th>" for key in results[0].keys())
    table = "<table border='1'><tr>" + header_row + "</tr>"
    for row in results:
        data_row = "".join(f"<td>{val}</td>" for val in row.values())
        table += "<tr>" + data_row + "</tr>"
    table += "</table>"
    return table

@app.errorhandler(404)
def page_not_found():
    """Custom 404 error page."""
    return '''
        <h1>404 - Page Not Found</h1>
        <p>Oops, Invalid URL! Please try using proper formatting:</p>
        <ul>
            <li><code>/sightings/year/&lt;year&gt;</code></li>
            <li><code>/sightings/shape/&lt;shape&gt;</code></li>
        </ul>
    ''', 404

if __name__ == '__main__':
    app.run()
