![Themis banner](/docs/img/themis_banner.jpg)

[![Build Status](https://github.com/looker-open-source/themis/workflows/Build%20Status/badge.svg)](https://github.com/looker-open-source/themis/actions)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)
[![CodeFactor](https://www.codefactor.io/repository/github/looker-open-source/themis/badge)](https://www.codefactor.io/repository/github/looker-open-source/themis)

Themis is an open source tool to automate health reporting and bring order in your Looker instance. 

With Themis, your admins and developers now have a report of issues in the instance that require your attention!

> For a free trial of Looker go to [looker.com/free-trial](https://looker.com/free-trial).


### Status and Support
Themis is NOT supported or warranted by Looker in any way. Please do not contact Looker support for issues with Themis. Questions and discussions can be logged via https://github.com/looker-open-source/themis/issues 


----------

### Features

| Area        | Feature           | Covered  |
| ------------- |-------------|:-----:|
| Connectivity      | Test Database Connections | ✅ |
| Connectivity      | Test Integrations    |   ✅  |
| Connectivity      | Test Datagroups     |    ✅  |
| Content      | Validate Looks, Dashboards     |    ✅  |
| Content      | Validate Embed Themes     |    soon...  |
| Performance      | Find Unlimited Downloads     |    ✅  |
| Performance      | Confirm All Nodes Versions     |    ✅  |
| Projects      | Validate LookML     |    soon...  |
| Projects      | Run Git Tests     |    soon...  |
| Projects      | Get Stale Branches     |    soon...  |
| Projects      | Run LookML Tests     |    soon...  |
| Schedules      | Get Failed Schedules     |    ✅  |
| Schedules      | Get Failed Alerts     |    soon...  |
| Schedules      | Get Failed PDTs     |    ✅  |
| Users      | Get LockedOut Users     |    ✅  |
| Users      | Get Inactive Users     |    ✅  |

>Not seeing a feature you'd like? [File a Feature Request!](https://github.com/looker-open-source/themis/issues/new)

### Requirements

- [Looker](https://looker.com) 7.10 or later
- Using the version 4.0 of the API
- API3 user credentials with [`admin` role](https://docs.looker.com/admin-options/settings/roles#default_roles) for that user to be able to get information about users and lockouts.
- Themis pulls a variety of information from your instance metadata, this can impact performance so we recommend you run these during quiet times for your business

----------

### Deployment Options

#### Heroku Deployment

The quickest way to deploy the application is to use Heroku's one-click deploy button, which will provision a server for your application. This will prompt you to give the app a unique name and configure all of the required variables (see "Environment Variables" below).

[Here is a Deployment example for Heroku](/docs/Heroku_Deployment.md)

#### GCP Compute Engine Deployment

[Here is a Deployment example for GCP Compute Engine](/docs/GCP_Deployment.md)

#### Environment Variables

The application variables for Looker can be configured using the looker.ini file [[example](https://github.com/looker-open-source/sdk-codegen/blob/master/looker-sample.ini)] or via environment variables. The variables external to Looker are configured using environment variables. You'll want to set up these variables:

- `LOOKERSDK_BASE_URL` Base URL for API (for Looker instance)

- `LOOKERSDK_CLIENT_ID ` API3 Client ID (for Looker instance user)

- `LOOKERSDK_CLIENT_SECRET` API3 Client Secret (for Looker instance user)

- `SENDGRID_API_KEY` API key for [SendGrid to send report email](https://app.sendgrid.com/login?redirect_to=%2Fsettings%2Fapi_keys)

- `THEMIS_EMAIL_RECIPIENTS` the list of users that receive Themis' report

----------

### Data Access

**Themis does not modify anything in your instance** and only retrieves this data to present it into the report. 
We suggest creating a Looker API user specifically for Themis, and using that user's API credentials. It's worth remembering that the user to create for the application needs to have [`admin` role](https://docs.looker.com/admin-options/settings/roles#default_roles). This is needed in order to access instance wide information such as disabled and locked out users...

**No sensitive information is surfaced by Themis** that is not showed in your Looker instance, only the name of Looker content (Look title, Schedule title, Connection name...). The report will contain direct links to your instance for you to fix these issues and may direct you to user specific information.

### Contributing

Pull Requests are welcome – we'd love to have help expanding Themis' coverage of Looker features and use cases!

If you have any trouble with the application, please [open an issue](https://github.com/looker-open-source/themis/issues/new) on this repo so we can have a look!
Please remember to exclude any sensitive information on the issues filed.


