import json
import os
import sys
import requests

token = os.environ['GITHUB_TOKEN']
headers = {"Authorization": "token " + token}
post_headers = {"Authorization": "token " + token, "Content-Type": "application/json"}

# labels - ENV vars later
plus_one_review = os.environ['LABEL_PLUS_1']
plus_two_review = os.environ['LABEL_PLUS_2']
approved = os.environ['LABEL_APPROVED']
requested_ca = os.environ['LABEL_REQUESTED_CHANGES']

def add_label(label, pr_number, url):
    if not label:
        print("No label given. Ignoring")
        return
        
    add_label_request = requests.post(url + "/issues/" + str(pr_number) + "/labels", json=[label], headers=post_headers)
    if add_label_request.status_code != 200:
        print(add_label_request)
        raise Exception("Failed to add label " + label + " to #" + str(pr_number))

def remove_label(label, pr_number, url):
    remove_label_request = requests.delete(url + "/issues/" + str(pr_number) + "/labels/" + label, headers=headers)
    if remove_label_request.status_code not in [200, 404]:
        print(remove_label_request)
        raise Exception("Failed to remove label " + label + " from #" + str(pr_number))

def get_approved_reviews(pr_number, url):
    reviews_request = requests.get(url + "/pulls/" + str(pr_number) + "/reviews", headers=headers)
    if reviews_request.status_code != 200:
        print(reviews_request)
        raise Exception("Failed to get reviewers for #" + str(pr_number))

    reviews = reviews_request.json()
    approvals = set()
    for review in reviews:
        if review["state"] == "APPROVED":
            approvals.add(review["user"]["login"])
    return len(approvals)

def created(pr_number, repo_url):
    label = plus_one_review
    add_label(label, pr_number, repo_url)

def reviewed(pr_number, repo_url):
    number_of_approved_reviews = get_approved_reviews(pr_number, repo_url)
    print("Number of approved reviews for " + str(pr_number) + " are " + str(number_of_approved_reviews))
    if(number_of_approved_reviews == 1):
        remove_label(plus_one_review, pr_number, repo_url)
        add_label(plus_two_review, pr_number, repo_url)
    elif(number_of_approved_reviews > 1):
        remove_label(plus_two_review, pr_number, repo_url)
        add_label(approved, pr_number, repo_url)

def requested_changes(pr_number, repo_url):
    add_label(requested_ca, pr_number, repo_url)


def main(event, context):
    payload = event["body"]
    if 'pull_request' in payload:
        pr_number = payload['pull_request']['number']
        repo_url = payload['pull_request']['base']['repo']['url']
        if payload['action'] == 'opened':
            created(pr_number, repo_url)
        elif payload['action'] == 'reopened':
            pass
        elif payload['action'] == 'closed':
            pass    
        elif payload['action'] == 'submitted':
            if payload['review']['state'] == 'changes_requested':
                requested_changes(pr_number, repo_url) 
            elif payload['review']['state'] == 'approved':
                reviewed(pr_number, repo_url)