"""Personal portfolio. Edit content.json to customize the page."""
import json
from pathlib import Path
from flask import Flask, render_template

app = Flask(__name__)

@app.get('/')
def index():
    content = json.loads(Path(__file__).with_name('content.json').read_text())
    return render_template('index.html', **content)

@app.get('/healthz')
def health():
    return {'status': 'ok'}, 200
