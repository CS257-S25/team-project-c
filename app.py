'''The Flask app interface for the UFO sightings project.'''

from flask import Flask, render_template, request
from ProductionCode import processor

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("homepage.html")

@app.route('/search')
def search():
    query = request.args.get('query', '').strip().lower()
    if query.isdigit():
        return sightings_by_year(int(query))
    else:
        return sightings_by_shape(query)

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
        return f"<h3>Total Results: {count}</h3>" + \
               f"<p>No sightings found for the year {year}, please try other years.</p>" + \
               "<br><p><a href='/'>Back to Homepage</a></p>"
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
        return f"<h3>Total Results: {count}</h3>" + \
               f"<p>No sightings found for shape '{shape}'.</p>" + \
               "<br><p><a href='/'>Back to Homepage</a></p>"
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
    return (f"<h2>{title}</h2><h3>Total Results: {count}</h3>"
            + table
            + "<br><p><a href='/'>Back to Homepage</a></p>")

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
            <br>
            <li><code>/sightings/topdata</code> - View top 5 years and shapes by sightings</li>
        </ul>
        <br><p><a href='/'>Back to Homepage</a></p>
    ''', 404

# --- Helper function to render top data lists ---
def render_top_list(title, data_list):
    """Helper function to render a list of (item, count) tuples as an HTML list.

    Args:
        title (str): The title for the list.
        data_list (list[tuple]): A list of (item, count) tuples.

    Returns:
        str: HTML string containing a title and an ordered list.
             Returns an error message if data_list is None or empty.
    """
    if data_list is None:
        return f"<h3>{title}</h3><p>Error retrieving data.</p>"
    if not data_list:
        return f"<h3>{title}</h3><p>No data available.</p>"

    list_items = "".join([f"<li>{item}: {count} sightings</li>" for item, count in data_list])
    return f"<h3>{title}</h3><ol>{list_items}</ol>"

# --- New route for top data ---
@app.route('/sightings/topdata')
def top_data():
    """Displays the top 5 years and top 5 shapes by sighting count.

    Returns:
        str: HTML page with the top data lists.
    """
    top_years = processor.get_top_years(5)
    top_shapes = processor.get_top_shapes(5)

    html = "<h1>Top UFO Sightings Data</h1>"
    html += render_top_list("Top 5 Years by Sightings", top_years)
    html += render_top_list("Top 5 Shapes by Sightings", top_shapes)
    html += "<br><p><a href='/'>Back to Homepage</a></p>"
    return html

if __name__ == '__main__':
    app.run()
