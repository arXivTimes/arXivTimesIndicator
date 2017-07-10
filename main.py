import os

from PIL import Image

from arxivtimes_indicator.data.github import filter_issue_by_ym, fetch_issues, get_icon_url, tally_by_labels, tally_by_users
from arxivtimes_indicator.data.twitter import fetch_tweets, rank_paper
from arxivtimes_indicator.data.utils import download, break_line, std_score
from arxivtimes_indicator.visualization.visualize import save_bar_graph, save_graph_with_icon, save_text_graph

TEMPORARY = 'data'
REPORT = 'reports'


def fetch_images(user_names, issues):
    images_urls = [get_icon_url(user_name, issues) for user_name in user_names]
    image_paths = [os.path.join(TEMPORARY, '{}.png'.format(name)) for name in user_names]
    [download(url, path) for url, path in zip(images_urls, image_paths)]
    images = [Image.open(p) for p in image_paths]
    return images


def main():
    # Fetch Issues
    issues = fetch_issues()
    # Process Issues
    filtered_issues = filter_issue_by_ym(issues)
    label_names, label_counts = tally_by_labels(filtered_issues)
    user_names, user_counts = tally_by_users(filtered_issues)
    images = fetch_images(user_names, issues)
    # Save label and user graph
    label_fig_path = os.path.join(REPORT, 'labels.png')
    users_fig_path = os.path.join(REPORT, 'users.png')
    label_names = break_line(label_names)
    save_bar_graph(label_names, label_counts, label_fig_path)
    save_graph_with_icon(list(range(len(user_names))), user_counts, images, users_fig_path)

    # Fetch tweets
    tweets = fetch_tweets()
    # Process tweets
    n = 10  # number of top papers
    scores, titles = rank_paper(tweets)
    scores, titles = scores[:n], titles[:n]
    # Save paper rank graph
    path = os.path.join(REPORT, 'rank.png')
    save_text_graph(titles, scores, path)


if __name__ == '__main__':
    main()