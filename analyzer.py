import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from utils import get_base_url, has_spaces, is_too_long, has_special_chars


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36'
}


def fetch_page(url):
    try:
        start = time.time()
        response = requests.get(url, headers=HEADERS, timeout=10, verify=True)
        response_time = round(time.time() - start, 2)
        response.raise_for_status()
        return response.text, None, response_time
    except requests.exceptions.SSLError:
        try:
            response = requests.get(url, headers=HEADERS, timeout=10, verify=False)
            return response.text, "SSL certificate warning (proceeded anyway)", 0
        except Exception as e:
            return None, f"SSL Error: {str(e)}", 0
    except requests.exceptions.ConnectionError:
        return None, "Connection failed. Please check the URL.", 0
    except requests.exceptions.Timeout:
        return None, "Request timed out. The website took too long to respond.", 0
    except requests.exceptions.HTTPError as e:
        return None, f"HTTP Error: {str(e)}", 0
    except Exception as e:
        return None, f"Unexpected error: {str(e)}", 0


def get_title_info(soup):
    title_tag = soup.find('title')
    if not title_tag or not title_tag.text.strip():
        return {'text': None, 'length': 0, 'status': 'Missing'}
    title = title_tag.text.strip()
    length = len(title)
    if length < 10:
        status = 'Too Short'
    elif length > 60:
        status = 'Too Long'
    else:
        status = 'Good'
    return {'text': title, 'length': length, 'status': status}


def get_meta_description(soup):
    meta = soup.find('meta', attrs={'name': 'description'})
    if not meta or not meta.get('content', '').strip():
        return {'text': None, 'length': 0, 'status': 'Missing'}
    desc = meta['content'].strip()
    length = len(desc)
    if length < 50:
        status = 'Too Short'
    elif length > 160:
        status = 'Too Long'
    else:
        status = 'Good'
    return {'text': desc, 'length': length, 'status': status}


def get_root_domain(netloc):
    parts = netloc.lower().split('.')
    if len(parts) >= 2:
        return parts[-2] + '.' + parts[-1]
    return netloc.lower()


def get_internal_links(soup, base_url):
    all_links = []
    seen_for_dedup = set()
    base_domain = get_root_domain(urlparse(base_url).netloc)

    for tag in soup.find_all('a', href=True):
        href = tag['href'].strip()

        if not href:
            continue
        if href.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:')):
            continue

        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)

        if parsed.scheme not in ('http', 'https'):
            continue

        link_domain = get_root_domain(parsed.netloc)
        if link_domain != base_domain:
            continue

        normalized = parsed._replace(fragment='').geturl().rstrip('/').lower()

        all_links.append(normalized)
        seen_for_dedup.add(normalized)

    unique_links = list(seen_for_dedup)
    return all_links, unique_links


def check_link_status(url):
    try:
        response = requests.head(
            url,
            headers=HEADERS,
            timeout=6,
            allow_redirects=True,
            verify=False
        )

        if response.status_code < 400:
            return response.status_code

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=6,
            allow_redirects=True,
            verify=False
        )

        return response.status_code

    except:
        try:
            response = requests.get(
                url,
                headers=HEADERS,
                timeout=6,
                allow_redirects=True,
                verify=False
            )
            return response.status_code
        except:
            return 0


def check_broken_links(unique_links):
    total_links = len(unique_links)

    if total_links <= 100:
        sample_size = total_links
    else:
        sample_size = min(int(total_links * 0.3), 100)

    if total_links <= sample_size:
        to_check = unique_links
    else:
        step = max(1, total_links // sample_size)
        to_check = unique_links[::step][:sample_size]

    results = []

    for link in to_check:
        status = check_link_status(link)
        is_broken = status == 0 or (status >= 400 and status != 999)

        results.append({
            'url': link,
            'status_code': status,
            'is_broken': is_broken
        })

    return results


def get_url_quality(all_links, unique_links):
    issues = []
    reported = set()

    seen = set()

    for link in unique_links:
        if has_spaces(link):
            key = (link, 'Contains Spaces')
            if key not in reported:
                issues.append({'url': link, 'issue': 'Contains Spaces'})
                reported.add(key)
        if is_too_long(link):
            key = (link, 'Excessively Long URL')
            if key not in reported:
                issues.append({'url': link, 'issue': 'Excessively Long URL'})
                reported.add(key)
        if has_special_chars(link):
            key = (link, 'Contains Special Characters')
            if key not in reported:
                issues.append({'url': link, 'issue': 'Contains Special Characters'})
                reported.add(key)

    return issues


def get_heading_counts(soup):
    return {
        'h1': len(soup.find_all('h1')),
        'h2': len(soup.find_all('h2')),
        'h3': len(soup.find_all('h3'))
    }


def get_image_info(soup):
    images = soup.find_all('img')
    total = len(images)
    missing_alt = sum(1 for img in images if not img.get('alt', '').strip())
    return {'total': total, 'missing_alt': missing_alt}


def analyze_url(url):
    html, error, response_time = fetch_page(url)
    if error and html is None:
        return None, error

    soup = BeautifulSoup(html, 'html.parser')
    base_url = get_base_url(url)

    title = get_title_info(soup)
    meta_desc = get_meta_description(soup)
    all_links, unique_links = get_internal_links(soup, base_url)
    link_results = check_broken_links(unique_links)
    url_issues = get_url_quality(all_links, unique_links)
    headings = get_heading_counts(soup)
    images = get_image_info(soup)

    broken_count = sum(1 for l in link_results if l['is_broken'])
    working_count = len(link_results) - broken_count

    result = {
        'url': url,
        'response_time': response_time,
        'warning': error,
        'title': title,
        'meta_description': meta_desc,
        'links': {
            'total': len(all_links),
            'unique': len(unique_links),
            'details': link_results,
            'broken_count': broken_count,
            'working_count': working_count
        },
        'url_quality': url_issues,
        'headings': headings,
        'images': images
    }

    return result, None
