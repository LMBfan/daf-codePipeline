## Bitbucket

This module creates an IAM user for use with automated deployments via Bitbucket Pipelines.

After creating the user, perform the following to enable Bitbucket deployments:

1. Create an IAM access key for the user.
2. Enable Bitbucket Pipelines for the repo.
3. Configure the `AWS_ACCESS_KEY_ID` & `AWS_SECRET_ACCESS_KEY` environment variables for the Pipeline (Settings -> Pipelines -> Environment variables), selecting the `Secured` option for `AWS_SECRET_ACCESS_KEY` to prevent it from being exportable.
4. Ensure no copies of the credentials are saved anywhere else other than the Secured Environment Variables.
