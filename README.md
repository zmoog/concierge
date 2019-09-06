# concierge

## Secrets

This bot use some external service that require some sort of secret credential to use. We're using the Parameter Store from the [AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/APIReference/Welcome.html) service.

See [Managing secrets, API keys and more with Serverless](https://serverless.com/blog/serverless-secrets-api-keys/) on how to access this kind of data with the Serverless Framework.

### Dropbox

```bash
$ aws ssm put-parameter --name dropboxRootFolder --type String --value '/Il Fatto Quotidiano'
$ aws ssm put-parameter --name dropboxAccessToken --type String --value xYz123..
{
    "Version": 1
}
```