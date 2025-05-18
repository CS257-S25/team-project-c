
from flask import Flask, request, jsonify, render_template
from ProductionCode import processor


app = Flask(__name__)

@app.route('/')
def homepage():
    return  '''
        <h1>Welcome to the UFO Sightings </h1>
        <p>Use the following URL patterns to view sightings data:</p>
        <ul>
            <li><code>/sightings/year/1950</code> – Get sightings from a specific year</li>
            <li><code>/sightings/shape:/circle</code> – Get sightings for a specific shape</li>
        </ul>
    '''

def clean_results(results):
    """Replace None values with empty strings for JSON serialization."""
    cleaned = []
    for row in results:
        cleaned.append({k: (v if v is not None else "") for k, v in row.items()})
    return cleaned

@app.route('/sightings/year/<int:year>')
def sightings_by_year(year):
    """Return UFO sightings for a given year as JSON."""
    if year is None:
        return jsonify({"error": "Missing or invalid 'year' query parameter."}), 400
    
    raw_results = processor.get_sightings_by_year(year)
    results = clean_results(raw_results)
    return jsonify(results)

@app.route('sightings/shape:/<string:shape>')
def sightings_by_shape(shape):
  """Return UFO sightings for a given shape as JSON."""
  raw_results = processor.get_sightings_by_shape(shape)
  results = clean_results(raw_results)
  return jsonify(results)

@app.route('/about')
def about_ufo():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()