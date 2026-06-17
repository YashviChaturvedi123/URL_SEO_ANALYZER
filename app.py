from flask import Flask, render_template, request, redirect, url_for, send_file, session
import os
import json

from utils import is_valid_url, normalize_url
from analyzer import analyze_url
from seo_checker import calculate_seo_score
from report_generator import generate_report

app = Flask(__name__)
app.secret_key = 'seo_analyzer_secret_123'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url', '').strip()

    if not url:
        return render_template('index.html', error="Please enter a URL.")

    url = normalize_url(url)

    if not is_valid_url(url):
        return render_template('index.html', error="Invalid URL format. Please enter a valid URL like https://example.com")

    data, error = analyze_url(url)

    if error and data is None:
        return render_template('index.html', error=error)

    seo = calculate_seo_score(data)
    filepath, filename, df = generate_report(data, seo)

    session['report_file'] = filepath
    session['report_name'] = filename

    return render_template('result.html', data=data, seo=seo, report_table=df.to_html(index=False, classes='report-table'))


@app.route('/download')
def download():
    filepath = session.get('report_file')
    filename = session.get('report_name')
    if not filepath or not os.path.exists(filepath):
        return redirect(url_for('index'))
    return send_file(filepath, as_attachment=True, download_name=filename)


if __name__ == '__main__':
    os.makedirs('reports', exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
