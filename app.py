'''The Flask app interface for the UFO sightings project.'''

from flask import Flask
from ProductionCode import processor

app = Flask(__name__)

@app.route('/')
def homepage():
    """Display the homepage with usage instructions.

    Returns:
        str: HTML content for the homepage.
    """
    return '''
        <h1>Welcome to the UFO Sightings App</h1>
        <p>Use the following URL patterns to view sightings data:</p>
        <ul> 
             <li><code>/sightings/year/&lt;year&gt;</code></li>
          e.g. /sightings/year/1999
            Year must be between 1941 and 2013.
            <br><br>
            <li><code>/sightings/shape/&lt;shape&gt;</code></li>
            e.g. /sightings/shape/circle
           Shape must be a valid UFO shape as listed below:
            <ul>
                    <li>circle</li>
                    <li>disk</li>
                    <li>light</li>
                    <li>fireball</li>
                    <li>triangle</li>
                    <li>oval</li>
                    <li>cylinder</li>
                    <li>rectangle</li>
                    </ul>
        </ul>
    '''

@app.route('/sightings/year/<int:year>')
def sightings_by_year(year):
    """Display UFO sightings for a given year in an HTML table.

    Args:
        year (int): The year to retrieve sightings for, passed via URL.

    Returns:
        str: HTML page with a table of sightings or a message if none found.
    """
    results = processor.get_sightings_by_year(year)
    count = len(results)
    if not results:
        return f"<p>No sightings found for the year {year}, please try other years.</p>"
    return render_results(f"Sightings from {year}", results, count)

@app.route('/sightings/shape/<string:shape>')
def sightings_by_shape(shape):
    """Display UFO sightings of a given shape in an HTML table.

    Args:
        shape (str): The shape to retrieve sightings for (case-insensitive),
                     passed via URL.

    Returns:
        str: HTML page with a table of sightings or a message if none found.
    """
    results = processor.get_sightings_by_shape(shape)
    count = len(results)
    if not results:
        return f"<p>No sightings found for shape '{shape}'.</p>"
    return render_results(f"Sightings of shape '{shape}'", results, count)

def render_results(title, results, count):
    """Render a list of sighting results into an HTML table format.

    Args:
        title (str): The title to display above the table.
        results (list[dict]): A list of sighting data (dictionaries).
        count (int): The total number of results found.

    Returns:
        str: HTML string containing a title, result count, and a table of the results.
    """
    table = table_constructor(results)
    return f"<h2>{title}</h2><h3>Total Results: {count}</h3>" + table

def table_constructor(results):
    """Construct an HTML table string from a list of sighting results.
    
    Args:
        results (list[dict]): A list of sighting data (dictionaries).
                              Should not be empty.

    Returns:
        str: HTML string representing a table of the results.
    """
    header_row = "".join(f"<th>{key}</th>" for key in results[0].keys())
    table = "<table border='1'><tr>" + header_row + "</tr>"
    for row in results:
        data_row = "".join(f"<td>{val}</td>" for val in row.values())
        table += "<tr>" + data_row + "</tr>"
    table += "</table>"
    return table

@app.errorhandler(404)
def page_not_found(error):
    """Display a custom 404 error page.

    Args:
        error: The error object passed by Flask (unused by the function body
               but required by Flask's errorhandler decorator).

    Returns:
        tuple: A tuple containing the HTML string for the 404 page
               and the 404 status code.
    """
    del error  #had to pass style check
    return '''
        <h1>404 - Page Not Found</h1>
        <p>Oops, invalid URL! Please try using proper formatting:</p>
        <ul> 
             <li><code>/sightings/year/&lt;year&gt;</code></li>
          e.g. /sightings/year/1999
            Year must be between 1941 and 2013.
            <br><br>
            <li><code>/sightings/shape/&lt;shape&gt;</code></li>
            e.g. /sightings/shape/circle
           Shape must be a valid UFO shape as listed below:
            <ul>
                    <li>circle</li>
                    <li>disk</li>
                    <li>light</li>
                    <li>fireball</li>
                    <li>triangle</li>
                    <li>oval</li>
                    <li>cylinder</li>
                    <li>rectangle</li>
                    </ul>
        </ul>
    ''', 404

if __name__ == '__main__':
    app.run()
