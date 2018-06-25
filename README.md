# Overview

## Structure

Environments (e.g. 'dev', 'prod') are stored in their respective `ENV-` branches (e.g. `ENV-dev`). The `common` environment can be found in the `master` branch.

## Deploying

Execute `make deploy` at the top of the repo (it will prompt you for which deployments, defined in `runway.yml`, to run.)

## Requirements

1. [pipenv](https://pypi.python.org/pypi/pipenv) & (optionally) [runway](https://pypi.python.org/pypi/runway)
    * pipenv is used in the Makefile to ensure the invoked runway's version matches the constraint in `Pipfile`.
2. Git - See these [installation instructions for Windows specific notes](https://nbdevs.atlassian.net/wiki/display/SG/Install+Git)
3. [ChefDK](https://downloads.chef.io/chefdk)

## Testing

Execute `make test` at the top of the repo.
