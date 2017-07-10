from __future__ import absolute_import
import dateutil.parser
from arxivtimes_indicator.data.github import fetch_issues
from arxivtimes_indicator.data.twitter import fetch_tweets, rank_paper
from arxivtimes_indicator.models.model import Issue, Label


def main():
    issues = fetch_issues()
    tweets = fetch_tweets(count=400)

    # calculate scores
    scores, urls = rank_paper(tweets)
    url_score = dict(zip(urls, scores))
    from pprint import pprint
    pprint(urls)
    cnt = 0
    for issue in issues:
        url        = issue['html_url']
        title      = issue['title']
        body       = issue['body']
        user_id    = issue['user']['login']
        avatar_url = issue['user']['avatar_url']
        labels     = [Label(label['name']) for label in issue['labels']]
        created_at = dateutil.parser.parse(issue['created_at'])
        try:
            score = round(url_score[url])
        except KeyError:
            score = 50
            cnt += 1
            print(url)

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
            Issue.update(score=score).where(Issue.url == url).execute()
        else:
            issue.save()
    print(cnt)


if __name__ == '__main__':
    main()

