# Concierge

A Slack bot to handle boring and repetitive stuff.

Here's few examples:

 * Download the latest issue from the [il Fatto Quotidiano](https://www.ilfattoquotidiano.it) website and store it in a Dropbox folder (requires a valid subscription to the newspaper).
 * Fetch the [Toggl](https://toggl.com) summary from the latest working day, and post it to Slack channel.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

 * [Serverless Framework](https://serverless.com) — this may require you to install Node.js depending on how you plan to install Serverless, see the [Serverless Framework Getting Started](https://serverless.com/framework/docs/getting-started/) page for more details.
 * [Python](https://www.python.org) — all the code is written in Python, tested with Python version 3.7.
 * [Pipenv](https://pipenv.kennethreitz.org/en/latest/) — the so called "Python Dev Workflow for Humans", used to handle Python virtual environment and dependencies.
 * An [AWS](https://aws.amazon.com) account — the bot is a serverless application using Lambda, Step Functions, and other services. 

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
$ git clone https://github.com/zmoog/concierge.git

$ cd concierge
```

And install all the Serverless Framework dependencies:

```
$ npm install 
```

Install all the Python dependencies:

```bash
$ pipenv install -dev
```

Set the [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) values:

```bash
# IFQ website
$ aws ssm put-parameter --name "/concierge/dev/ifq-username" --value "" --type String
$ aws ssm put-parameter --name "/concierge/dev/ifq-password" --value "" --type String

# Slack
$ aws ssm put-parameter --name "/concierge/dev/slack-webhook-url" --value "" --type String

# Dropbox
$ aws ssm put-parameter --name "/concierge/dev/dropbox-root-folder" --value "" --type String
$ aws ssm put-parameter --name "/concierge/dev/dropbox-access-token" --value "" --type String

# Toggl
$ aws ssm put-parameter --name "/concierge/dev/toggl-api-token" --value "" --type String
$ aws ssm put-parameter --name "/concierge/dev/toggl-user-agent" --value "" --type String
$ aws ssm put-parameter --name "/concierge/dev/toggl-workspace-id" --value "" --type String
```

Docker — the Python packages are built in a Docker container `lambci/lambda` to maximize the compatibility with the Lambda runtime, especially for those packages that have native libraraies.

```bash
$ docker-machine start default 

$ eval $(docker-machine env default)   

$ docker ps                   
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES

```

Environment variables and aliases:

```bash
$ alias sls='./node_modules/.bin/sls'

$ export PYTHONPATH=`pwd`:$PYTHONPATH 

$ export AWS_PROFILE=<YOUR_PROFILE_NAME>
```


Check if the dev environment is setup properly running these commands:

```bash
$ sls package

Serverless: Generating requirements.txt from Pipfile...
Serverless: Parsed requirements.txt from Pipfile in /Users/mbranca/code/projects/zmoog/concierge/.serverless/requirements.txt...
Serverless: Installing requirements from /Users/mbranca/Library/Caches/serverless-python-requirements/7313ed46dad648a73b2ead6c6f736f4b9912fa69799ddb34d90a268492e66fc9_slspyc/requirements.txt ...
Serverless: Docker Image: lambci/lambda:build-python3.7
Serverless: Using download cache directory /Users/mbranca/Library/Caches/serverless-python-requirements/downloadCacheslspyc
Serverless: Running docker run --rm -v /Users/mbranca/Library/Caches/serverless-python-requirements/7313ed46dad648a73b2ead6c6f736f4b9912fa69799ddb34d90a268492e66fc9_slspyc\:/var/task\:z -v /Users/mbranca/Library/Caches/serverless-python-requirements/downloadCacheslspyc\:/var/useDownloadCache\:z -u 0 lambci/lambda\:build-python3.7 python3.7 -m pip install -t /var/task/ -r /var/task/requirements.txt --cache-dir /var/useDownloadCache...
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Injecting required Python packages to package...
```



End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

```bash
$ pipenv run pytest
```

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
