#!/bin/bash

# Token of a git hub user with write permissions to the repo
export GITHUB_TOKEN="b75833743082ca4f76226b19d347c0030f792841"
# Label to apply if the PR does not have any approvals
export LABEL_PLUS_1="+1 Pending"
# Label to apply if the PR has only one approval
export LABEL_PLUS_2="+2 Pending"
# Label to apply if the PR has two approvals
export LABEL_APPROVED="Approved"
# Label to apply if a reviewer requested changes to the PR
export LABEL_REQUESTED_CHANGES="Requested Changes"

if [[ `hash pip` -ne 0 ]]; then
	echo 'PIP is required for the deployment'
	exit
fi
if [[ `hash zip` -ne 0 ]]; then
	echo 'ZIP is required for the deployment'
fi
if [[ `hash serverless` -ne 0 ]]; then
	echo 'Serverless is required for the deployment'
fi

pip install -t . -r requirements.txt
serverless deploy