from collections import Counter
from datetime import datetime


import requests
from dateutil.parser import parse


def get_all_issues():
    url = 'https://api.github.com/repos/arXivTimes/arXivTimes/issues?per_page=100'
    issues = []
    cnt = 0
    while cnt < 20:
        cnt += 1
        res = requests.get(url)
        issues.extend(res.json())
        if 'next' in res.links:
            url = res.links['next']['url']
        else:
            return issues


def tally_by_users(issues):
    c = Counter()
    for issue in issues:
        name = issue['user']['login']
        c[name] += 1
    names = [k for k, _ in c.most_common()]
    counts = [v for _, v in c.most_common()]
    return names, counts


def tally_by_labels(issues):
    c = Counter()
    for issue in issues:
        for label in issue['labels']:
            name = label['name']
            c[name] += 1
    names = [k for k, _ in c.most_common()]
    counts = [v for _, v in c.most_common()]
    return names, counts


def filter_issue_by_ym(issues):
    filtered_issues = []
    now = datetime.now()
    for issue in issues:
        created_at = parse(issue['created_at'])
        if now.year == created_at.year and now.month == created_at.month:
            filtered_issues.append(issue)
    return filtered_issues


def get_icon_url(user_name, issues):
    for issue in issues:
        if issue['user']['login'] == user_name:
            return issue['user']['avatar_url']
    return None