import pandas as pd
import os
import time


def generate_report(data, seo):
    rows = []

    rows.append({'Category': 'URL', 'Item': 'Analyzed URL', 'Value': data['url'], 'Status': 'Info'})

    rows.append({'Category': 'SEO Score', 'Item': 'Overall Score', 'Value': f"{seo['score']}/100", 'Status': seo['grade']})

    title = data['title']
    rows.append({'Category': 'Title', 'Item': 'Title Text', 'Value': title['text'] or 'N/A', 'Status': title['status']})
    rows.append({'Category': 'Title', 'Item': 'Title Length', 'Value': title['length'], 'Status': title['status']})

    meta = data['meta_description']
    rows.append({'Category': 'Meta Description', 'Item': 'Description Text', 'Value': (meta['text'] or 'N/A')[:80] + ('...' if meta['text'] and len(meta['text']) > 80 else ''), 'Status': meta['status']})
    rows.append({'Category': 'Meta Description', 'Item': 'Description Length', 'Value': meta['length'], 'Status': meta['status']})

    links = data['links']
    rows.append({'Category': 'Links', 'Item': 'Total Internal Links', 'Value': links['total'], 'Status': 'Info'})
    rows.append({'Category': 'Links', 'Item': 'Unique Internal Links', 'Value': links['unique'], 'Status': 'Info'})
    rows.append({'Category': 'Links', 'Item': 'URLs Tested', 'Value': links['working_count'] + links['broken_count'], 'Status': 'Info'})
    rows.append({'Category': 'Links', 'Item': 'Broken URLs Found', 'Value': links['broken_count'], 'Status': 'Fail' if links['broken_count'] > 0 else 'Good'})

    headings = data['headings']
    rows.append({'Category': 'Headings', 'Item': 'H1 Tags', 'Value': headings['h1'], 'Status': 'Good' if headings['h1'] == 1 else 'Check'})
    rows.append({'Category': 'Headings', 'Item': 'H2 Tags', 'Value': headings['h2'], 'Status': 'Info'})
    rows.append({'Category': 'Headings', 'Item': 'H3 Tags', 'Value': headings['h3'], 'Status': 'Info'})

    images = data['images']
    rows.append({'Category': 'Images', 'Item': 'Total Images', 'Value': images['total'], 'Status': 'Info'})
    rows.append({'Category': 'Images', 'Item': 'Missing Alt Text', 'Value': images['missing_alt'], 'Status': 'Fail' if images['missing_alt'] > 0 else 'Good'})

    rows.append({'Category': 'URL Quality', 'Item': 'Total Issues Found', 'Value': len(data['url_quality']), 'Status': 'Fail' if len(data['url_quality']) > 0 else 'Good'})

    df = pd.DataFrame(rows)

    os.makedirs('reports', exist_ok=True)
    filename = f"seo_report_{int(time.time())}.csv"
    filepath = os.path.join('reports', filename)
    df.to_csv(filepath, index=False)

    return filepath, filename, df
