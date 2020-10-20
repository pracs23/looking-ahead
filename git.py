#!/usr/bin/env python2.7
import argparse
import requests
import logging
import sys


def run(args):
    """
    Method to run the Github repo stats
    :param args: arguments provided at the command line
    """
    logging.getLogger().setLevel(logging.INFO)
    level = args.top
    github_username = args.username
    github_token = args.token
    if github_username is None or github_token is None:
        auth = None
    else:
        auth = (github_username, github_token)
    github_base_url = 'https://api.github.com/search/repositories?q=org:' + args.org + '&per_page=100'
    star_url = github_base_url + '&sort=stars&order=desc'
    fork_url = github_base_url + '&sort=forks&order=desc'
    sorted_star_count  = get_repository_stats(star_url, 'stargazers_count', auth)
    get_top_stats(sorted_star_count, 'Number of Stars', level)
    sorted_fork_count  = get_repository_stats(fork_url, 'forks_count', auth)
    get_top_stats(sorted_fork_count, 'Number of Forks', level)
    sorted_pr_count, sorted_percentage_count = get_pr_contibution_percent(github_base_url, auth)
    get_top_stats(sorted_pr_count, 'Number of Pull Requests', level)
    get_top_stats(sorted_percentage_count, 'Contribution Percentage', level)


def get_pr_contibution_percent(url, auth):
    """
    Method to return the Github repo stats for PR count and Contribution Percentage
    :param url: github PR url
    :param auth: basic/oauth credentials passed from command line
    """
    repo_name_list = []
    repo_pr_dict = {}
    repo_contribution_dict = {}
    response = requests.get(url, auth = auth)
    response.raise_for_status()
    for repo in response.json().get('items'):
        repo_name_list.append(repo.get('name'))
    for repo_name in repo_name_list:
        pr_url = 'https://api.github.com/repos/twitter/' + repo_name + '/pulls?state=all&direction=desc'
        pr_response = requests.get(pr_url, auth = auth)
        response.raise_for_status()
        if pr_response.json():
            pr_count = pr_response.json()[0].get('number')
            if pr_response.json()[0].get('head', {}).get('repo', {}) is not None:
                fork_count = pr_response.json()[0].get('head', {}).get('repo', {}).get('forks_count')
            else:
                fork_count = 0
                contri_percentage = 0
            if fork_count !=0:
                contri_percentage = float(pr_count)/float(fork_count)
        else:
            pr_count = 0
            contri_percentage = 0
        repo_pr_dict[repo_name] = pr_count
        repo_contribution_dict[repo_name] =  contri_percentage
    pr_count = sorted(repo_pr_dict.items(), key=lambda x:x[1], reverse=True)
    contribution_count = sorted(repo_contribution_dict.items(), key=lambda x:x[1], reverse=True)
    return pr_count, contribution_count


def get_repository_stats(url, key, auth):
    """
    Method to get the Github repo stats for Stars and Forks
    :param url: github search url
    :param key: stars or forks
    :param auth: basic/oauth credentials passed from command line
    """
    repository_stats_dict = {}
    response = requests.get(url, auth = auth)
    response.raise_for_status()
    for x in response.json().get('items'):
        repository_stats_dict[x.get('name')] =  x.get(key)
        sorted_star_count = sorted(repository_stats_dict.items(), key=lambda z:z[1], reverse=True)
    return sorted_star_count

def get_top_stats(records, stat, level):
    """
    Method to get the top N records
    :param records: first 100 responses return from github api
    :param stat: stars, forks, pr, contribution %
    :param level: top 'N' to be passed from command line
    """
    counter = 0
    logging.info("\n ****** Top '{}' repos sorted by '{}' *********".format(level, stat))
    for record in records:
        logging.info("Github repo: '{}' & '{}': '{}'".format(str(record[0]), stat , str(record[1])))
        counter = counter + 1
        if counter == level:
            break


def main():
    """
    Main method to pass command line arguments
    """
    try:
        parser = argparse.ArgumentParser(description="Get GitHub repos stats for an organization")
        parser.add_argument('-org', help = 'Github organization', dest = 'org', type=str, required=True)
        parser.add_argument('-top', help = 'top nth', dest = 'top', type = int, required=True)
        parser.add_argument('-username', help = 'GitHub username', dest = 'username', type = str, required=False)
        parser.add_argument('-token', help = 'GitHub token', dest = 'token', type = str, required=False)
        parser.set_defaults(func=run)
        args=parser.parse_args()
        args.func(args)
    except AssertionError:
        logging.error('Missed passing in required arguments, like --Github organization!')
        sys.exit(2)

if __name__=="__main__":
    main()