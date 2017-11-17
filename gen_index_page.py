#!/usr/bin/env python3


# TODO:
# What to do about private repos (so can't get repo info)


import argparse
import json
#import markdown
#html = markdown.markdown(your_text_string)
import pprint
import sys
import urllib.request
import yaml


DEFAULT_REPOS_METADATA_FILE = 'repos.metadata.yml'
DEFAULT_ORG = 'KnowEnG'
# Is this necessary?
# Put something like this at the front matter of the file
#---
#layout: post
#title: Blogging Like a Hacker
#---
#DEFAULT_OUTPUT_FILE = 'index.md'
DEFAULT_OUTPUT_FILE = 'out.md'

GIT_ORG_URL = 'https://github.com/:org:'
GIT_REPO_URL = 'https://github.com/:org:/:repo:'

GIT_ORG_INFO_URL = 'https://api.github.com/search/repositories?q=user::org:'
GIT_REPO_INFO_URL = 'https://api.github.com/search/repositories?q=user::org:+:repo:'



def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-rif', '--repos_info_file')
    parser.add_argument('-rmf', '--repos_metadata_file', default=DEFAULT_REPOS_METADATA_FILE)
    parser.add_argument('-o', '--org', default=DEFAULT_ORG)
    parser.add_argument('-of', '--output_file', default=DEFAULT_OUTPUT_FILE)

    args = parser.parse_args()

    return args


def gen_git_org_url(org):
    return GIT_ORG_URL.replace(':org:', org)


def gen_git_repo_url(org, repo):
    return GIT_REPO_URL.replace(':org:', org).replace(':repo:', repo)


def gen_git_org_info_url(org):
    return GIT_ORG_INFO_URL.replace(':org:', org)


def gen_git_repo_info_url(org, repo):
    return GIT_REPO_INFO_URL.replace(':org:', org).replace(':repo:', repo)


def get_repos_info(args):
    if args.repos_info_file:
        print("Getting repos info from file '%s' ..." % (args.repos_info_file))
        with open(args.repos_info_file, 'r') as f:
            org_info_str = f.read()
    else:
        url = gen_git_org_info_url(args.org)
        print("Getting repos info from url '%s' ..." % (url))
        # https://stackoverflow.com/questions/43259946/github-api-getting-topics-of-a-github-repository
        # Add this header to get topics: "Accept: application/vnd.github.mercy-preview+json"
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/vnd.github.mercy-preview+json")
        #with urllib.request.urlopen(url) as f:
        with urllib.request.urlopen(req) as f:
            org_info_str = f.read().decode('utf-8')
    #print(org_info_str)

    org_info = json.loads(org_info_str)
    #print(org_info)
    #print(type(org_info))
    items = org_info["items"]
    #print(items)
    #print(type(items))
    #print(len(items))

    repos_info = {}

    for item in items:
        name = item["name"]
        print("  Found repo '%s'" % (name))
        repos_info[name] = item

    print()

    return repos_info


def main():
    args = parse_args()

    repos_info = get_repos_info(args)

    print("Getting repos metadata from file '%s' ..." % (args.repos_metadata_file))
    print()
    with open(args.repos_metadata_file, 'r') as f:
        repo_metadata = yaml.load(f)

    # This will be a list of dicts
    # Each of those dicts has one key (the category),
    # whose value is another list of dicts
    # Likewise each of those dicts has one key (the repo),
    # and its value is another list of dicts (the properties of the repo)
    # What about properties of categories?
    #print(repo_metadata)
    #print(type(repo_metadata))
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(repo_metadata)

    outf = open(args.output_file, 'w')

    repos_seen = {}

    for category_data in repo_metadata:
        #print(category_data)
        # category is a dict with one key
        # That comma after the paren belongs there
        # https://stackoverflow.com/questions/20145902/how-to-extract-dictionary-single-key-value-pair-in-variables
        (category, repos_data), = category_data.items()
        print("Processing category '%s' ..." % (category))
        if repos_data:
            print("## %s" % (category), file=outf)
        for repo_data in repos_data:
            #print(repo_data)
            (repo, repo_data_bare), = repo_data.items()
            print("  Processing repo '%s' ..." % (repo))
            repos_seen[repo] = 1
            if "hide" in repo_data_bare and repo_data_bare["hide"]:
                print("  hiding repo '%s'" % (repo))
                continue
            if repo in repos_info:
                # What repo_info to use?
                # private, html_url, description
                # topics, if present
                repo_info = repos_info[repo]
                private = repo_info["private"]
                html_url = repo_info["html_url"]
                description = repo_info["description"]
                if "topics" in repo_info:
                    topics = repo_info["topics"]
                else:
                    topics = None
                #print(repo_info)
                if description is None:
                    print(" - [%s](%s):" % (repo, html_url), file=outf)
                else:
                    description = description.rstrip()
                    print(" - [%s](%s): %s" % (repo, html_url, description), file=outf)
            else:
                print("  repo '%s' is private" % (repo))
    print()

    #repos_not_seen = {}

    #for repo in repos_info:
    #    if repo not in repos_seen:
    #        repos_not_seen[repo] = 1

    repos_not_seen = [r for r in repos_info if not repos_seen[r]]

    if repos_not_seen:
        print("The following repos were in the repos info, but not processed:")
        print(repos_not_seen)
    else:
        print("All of the repos in the repos info were processed.")


if __name__ == "__main__":
    main()
