import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import dateutil.parser
from arxivtimes_indicator.data.github import fetch_issues
from arxivtimes_indicator.data.twitter import fetch_tweets, rank_paper
from arxivtimes_indicator.models.model import Issue, Label, create_tables


def main():
    create_tables()
    issues = fetch_issues()
    tweets = fetch_tweets(count=400)

    scores, urls = rank_paper(tweets)
    url_score = dict(zip(urls, scores))
    #url_score = {}
    from pprint import pprint
    pprint(urls)
    cnt = 0
    updates = 0
    inserts = 0
    for issue in issues:
        if "number" not in issue:
            print("the issue seems to be broken. can not get issue field.")
            continue
        if "pull_request" in issue:
            continue
        if "state" in issue and issue["state"] != "open":
            continue

        url        = issue['html_url']
        title      = issue['title']
        body       = issue['body']
        user_id    = issue['user']['login']
        avatar_url = issue['user']['avatar_url']
        labels     = [Label(name=label['name']) for label in issue['labels']]
        created_at = dateutil.parser.parse(issue['created_at'])

        try:
            score = round(url_score[url])
        except KeyError:
            score = 50
            cnt += 1
            print("can not calculate score of #{} -> {}".format(issue["number"], url))

        issue = Issue(title=title,
                      url=url,
                      user_id=user_id,
                      avatar_url=avatar_url,
                      score=score,
                      created_at=created_at,
                      body=body,
                      labels=labels)

        query = Issue.select().where(Issue.url == url)
        if query.exists():
            issue = query.get()
            Issue.update(score=score, title=title, body=body).where(Issue.url == url).execute()
            Label.delete().where(Label.issue == issue).execute()
            updates += 1
        else:
            issue.save()
            inserts += 1

        for label in labels:
            label.issue = issue
            label.save()

    print("Inserts={}, Updates={}, score error={}".format(inserts, updates, cnt))


if __name__ == '__main__':
    main()
