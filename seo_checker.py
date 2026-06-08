def calculate_seo_score(data):
    score = 0
    breakdown = []

    title = data['title']
    if title['status'] == 'Good':
        score += 20
        breakdown.append({'check': 'Title Tag', 'points': 20, 'max': 20, 'status': 'Pass'})
    elif title['status'] in ('Too Short', 'Too Long'):
        score += 10
        breakdown.append({'check': 'Title Tag', 'points': 10, 'max': 20, 'status': 'Partial'})
    else:
        breakdown.append({'check': 'Title Tag', 'points': 0, 'max': 20, 'status': 'Fail'})

    meta = data['meta_description']
    if meta['status'] == 'Good':
        score += 20
        breakdown.append({'check': 'Meta Description', 'points': 20, 'max': 20, 'status': 'Pass'})
    elif meta['status'] in ('Too Short', 'Too Long'):
        score += 10
        breakdown.append({'check': 'Meta Description', 'points': 10, 'max': 20, 'status': 'Partial'})
    else:
        breakdown.append({'check': 'Meta Description', 'points': 0, 'max': 20, 'status': 'Fail'})

    headings = data['headings']
    if headings['h1'] == 1:
        score += 15
        breakdown.append({'check': 'H1 Tag (exactly one)', 'points': 15, 'max': 15, 'status': 'Pass'})
    elif headings['h1'] > 1:
        score += 7
        breakdown.append({'check': 'H1 Tag (exactly one)', 'points': 7, 'max': 15, 'status': 'Partial'})
    else:
        breakdown.append({'check': 'H1 Tag (exactly one)', 'points': 0, 'max': 15, 'status': 'Fail'})

    images = data['images']
    if images['total'] == 0:
        score += 15
        breakdown.append({'check': 'Image Alt Texts', 'points': 15, 'max': 15, 'status': 'N/A'})
    elif images['missing_alt'] == 0:
        score += 15
        breakdown.append({'check': 'Image Alt Texts', 'points': 15, 'max': 15, 'status': 'Pass'})
    elif images['missing_alt'] < images['total']:
        score += 7
        breakdown.append({'check': 'Image Alt Texts', 'points': 7, 'max': 15, 'status': 'Partial'})
    else:
        breakdown.append({'check': 'Image Alt Texts', 'points': 0, 'max': 15, 'status': 'Fail'})

    links = data['links']
    broken = links['broken_count']
    total_checked = len(links['details'])
    if total_checked == 0 or broken == 0:
        score += 15
        breakdown.append({'check': 'No Broken Links', 'points': 15, 'max': 15, 'status': 'Pass'})
    elif broken <= 2:
        score += 7
        breakdown.append({'check': 'No Broken Links', 'points': 7, 'max': 15, 'status': 'Partial'})
    else:
        breakdown.append({'check': 'No Broken Links', 'points': 0, 'max': 15, 'status': 'Fail'})

    url_issues = data['url_quality']
    if len(url_issues) == 0:
        score += 15
        breakdown.append({'check': 'URL Quality', 'points': 15, 'max': 15, 'status': 'Pass'})
    elif len(url_issues) <= 3:
        score += 7
        breakdown.append({'check': 'URL Quality', 'points': 7, 'max': 15, 'status': 'Partial'})
    else:
        breakdown.append({'check': 'URL Quality', 'points': 0, 'max': 15, 'status': 'Fail'})

    score = min(score, 100)

    if score >= 80:
        grade = 'Excellent'
        grade_color = 'green'
    elif score >= 60:
        grade = 'Good'
        grade_color = 'yellow'
    elif score >= 40:
        grade = 'Needs Work'
        grade_color = 'orange'
    else:
        grade = 'Poor'
        grade_color = 'red'

    return {
        'score': score,
        'grade': grade,
        'grade_color': grade_color,
        'breakdown': breakdown
    }
