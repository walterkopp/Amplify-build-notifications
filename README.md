<!-- markdownlint-disable MD033 MD026 -->
<!-- MD033: No inline HTML | Reason: used for collapsable section(s) -->
<!-- MD026: No trailing punctuation | Reason: used for '# IMPORTANT' heading -->

# Amplify Slack Notifications

Ever wanted simple yet cool AWS Amplify build notifications in Slack?
Well here you go!

(Insert preview)

## Table of contents

<details>
  <summary>Click to expand!</summary>

- [Amplify Slack Notifications](#amplify-slack-notifications)
  - [Table of contents](#table-of-contents)
  - [Architecture](#architecture)
  - [Resources](#resources)
  - [Installation](#installation)
    - [Slack](#slack)
    - [MS Teams (coming soon)](#ms-teams-coming-soon)
  - [Deployment](#deployment)
    - [Prerequisites](#prerequisites)
    - [Makefile](#makefile)
    - [Cleanup](#cleanup)

</details>

## Architecture

(Insert Diagram)

## Resources

(List of resources created)

## Installation

### Slack

(Insert how to create slack app) w/ basics

### MS Teams (coming soon)

...

## Deployment

Deployment is managed using AWS SAM

### Prerequisites

|                                                               Plugin                                                      |  Version  |
|---------------------------------------------------------------------------------------------------------------------------|-----------|
|  [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)                                 |>= v2.7    |
|  [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)|>= v.1.55  |


### Makefile

In order to make deploying a little bit easier a Makefile is provided

Usage:

```bash
make help
```

### Cleanup

Done with playing around and the resources are not needed anymore?

1. Simply delete your created AWS CloudFormation stack via console or `SAM delete`
2. Don't forget to remove the `aws-sam-cli-managed-default` CF stack
