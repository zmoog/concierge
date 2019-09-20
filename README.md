# Concierge

The Concierge is a serverless application that handles all the boring and repetivive tasks that I can handle to it.

## Features

### IFQ

The Concierge will handle the download of new issues of the Il Fatto Quotidiano newspaper (I'm a paid subscriber!) publishing them to a family owner Dropbox account for ease of use.

https://serverless.com/framework/docs/providers/aws/events/schedule/


## Secrets

This bot use some external service that require some sort of secret credential to use. We're using the Parameter Store from the [AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/APIReference/Welcome.html) service.

See [Managing secrets, API keys and more with Serverless](https://serverless.com/blog/serverless-secrets-api-keys/) on how to access this kind of data with the Serverless Framework.

### IFQ

```bash
$ aws ssm put-parameter --name concierge/dev/ifq-username --type String --value 'me@gmail.com'
$ aws ssm put-parameter --name concierge/dev/ifq-password --type String --value 'secret!'
```

### Dropbox

```bash
$ aws ssm put-parameter --name concierge/dev/dropbox-root-folder --type String --value '/Il Fatto Quotidiano'
$ aws ssm put-parameter --name concierge/dev/dropbox-access-token --type String --value xYz123..
```

### Slack

```bash
$ aws ssm put-parameter --name concierge-dev-skack-webhook-url --type String --value 'https://...'
```

Note: when adding a URL as parameter value the AWS CLI may attempt to follow the link. This behaviour can be overcome, as described in https://github.com/aws/aws-cli/issues/1475 addind a simple entry in the profile section of your `~/.aws/config`:

```
cli_follow_urlparam = false
```

```bash
$ aws ssm put-parameter --name concierge/dev/slack-webhook-url --type String --value 'xyz'
```

### Toggl

```bash
$ aws ssm put-parameter --name concierge/dev/toggl-api-token --type String --value 'xyz'
$ aws ssm put-parameter --name concierge/dev/toggl-user-agent --type String --value 'xyz'
$ aws ssm put-parameter --name concierge/dev/toggl-workspace-id --type String --value 'xyz'
```
