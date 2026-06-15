# URL Quality & SEO Analyzer

A web-based SEO analysis tool built using Python, Flask, BeautifulSoup, Requests, and Pandas. The application analyzes webpages for SEO health, detects broken links, evaluates metadata quality, checks heading structure, analyzes image alt tags, and generates downloadable reports.

---

## Features

- URL validation and normalization
- SEO score calculation out of 100
- Title tag analysis
- Meta description analysis
- Internal link discovery
- Adaptive broken-link verification
- URL quality checks
- Heading structure analysis (H1, H2, H3)
- Image alt text analysis
- Downloadable CSV reports
- Interactive dashboard with visual SEO breakdown
- Response time measurement

---

## Tech Stack

### Backend
- Python 3
- Flask

### Data Extraction
- Requests
- BeautifulSoup4

### Data Processing
- Pandas
- Regular Expressions (Regex)

### Frontend
- HTML5
- CSS3

---

## SEO Score Formula

| Category | Points |
|-----------|---------|
| Title Tag | 20 |
| Meta Description | 20 |
| H1 Structure | 15 |
| Image Alt Text | 15 |
| Broken Links | 15 |
| URL Quality | 15 |
| Total | 100 |

---

## Project Workflow

1. User enters a webpage URL.
2. Flask validates and normalizes the URL.
3. Requests fetches webpage content.
4. BeautifulSoup extracts SEO-related information.
5. Internal URLs are discovered and verified.
6. SEO score is calculated based on predefined rules.
7. Results are displayed on a dashboard.
8. A downloadable CSV report is generated.

---

## Project Structure

```text
url_seo_analyzer/
│
├── app.py
├── analyzer.py
├── seo_checker.py
├── report_generator.py
├── utils.py
├── requirements.txt
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── static/
│   └── css/
│       └── style.css
│
└── reports/
```

---

## Sample Analysis Metrics

The analyzer evaluates:

- SEO score
- Page response time
- Internal links
- Unique URLs
- Broken URLs
- Title length
- Meta description length
- Heading hierarchy
- Image accessibility
- URL quality issues

---

## Key Learning Outcomes

- Developed a complete Flask web application from scratch.
- Implemented web scraping using BeautifulSoup.
- Designed custom SEO scoring logic.
- Built adaptive link verification for performance optimization.
- Generated downloadable reports using Pandas.
- Designed a responsive dashboard interface using HTML and CSS.
- Worked with HTTP requests, status codes, and URL parsing.

---

## Future Enhancements

- Open Graph tag analysis
- Twitter Card analysis
- Keyword density analysis
- Sitemap analysis
- Robots.txt validation
- Bulk URL analysis
- Historical report tracking
- User authentication system
- Cloud deployment

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Run Locally

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Resume Description

Developed a web-based URL Quality & SEO Analyzer using Python, Flask, BeautifulSoup, Requests, Regex, and Pandas to evaluate webpage SEO health, detect broken links, analyze metadata, calculate SEO scores, and generate downloadable reports.

---

## Author

Yashvi Chaturvedi

B.Tech Computer Science Engineering (Minor: Data Science)
