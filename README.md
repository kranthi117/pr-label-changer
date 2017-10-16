WebHook to change the labels of a PR automatically.

DEPLOYMENT
==========
- Install npm
- Install serverless
- Update environment variables in deploy.sh
- bash deploy.sh
- Set the resultant API Gateway endpoint as webhook in the repository
 - Use `application/json` as content type
 - Select _Pull request_ and _Pull request review_ events to be sent to the webhook
