[![CircleCI](https://circleci.com/gh/InternationalTradeAdministration/ita-taxonomy-normalizer/tree/master.svg?style=svg)](https://circleci.com/gh/InternationalTradeAdministration/ita-taxonomy-normalizer/tree/master)
[![Maintainability](https://api.codeclimate.com/v1/badges/0527c50224cb66b8e576/maintainability)](https://codeclimate.com/github/InternationalTradeAdministration/ita-taxonomy-normalizer/maintainability)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=InternationalTradeAdministration/ita-taxonomy-normalizer)](https://dependabot.com)

# ITA Taxonomy Normalizer

This project provides an Azure Function that periodically creates a single JSON document from the custom Taxonomy endpoint at https://api.trade.gov. It uploads that JSON file to a Blob in an Azure Container.

## Prerequisites

- This project is tested against Python 3.7+ in [CircleCI](https://app.circleci.com/github/InternationalTradeAdministration/ita-taxonomy-normalizer/pipelines).

## Getting Started

	git clone git@github.com:InternationalTradeAdministration/ita-taxonomy-normalizer.git
	cd ita-taxonomy-normalizer
	mkvirtualenv -p /usr/local/bin/python3.8 -r requirements-test.txt ita-taxonomy-normalizer

### Tests

```bash
python -m pytest
```

## Environment Variables

Variable Name | Description
------------ | -------------
API_KEY | Your api.trade.gov key
AzureWebJobsStorage | Azure storage connection string e.g. `DefaultEndpointsProtocol=https;AccountName=foo;AccountKey=mykey==;EndpointSuffix=core.windows.net` 
CONTAINER_NAME | Destination container for JSON file
FILE_NAME | Destination file name (defaults to `ita_taxonomy_labels.json`)

## Invocation

The easiest way to invoke the function locally is to set the above environment variables and run it manually:

	python TimerTrigger/taxonomy_io.py
	
Alternatively, you can create a `local.settings.json` file in the root of this project containing the appropriate values:

```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "DefaultEndpointsProtocol=https;AccountName=foo;AccountKey=mykey==;EndpointSuffix=core.windows.net",
    "API_KEY": "your_key",
    "CONTAINER_NAME": "demo"
  }
}
```

This relies on the cron scheduler in `TimerTrigger/function.json` to trigger the function:

    func start

You specify the schedule in the form of a [NCRONTAB expression](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer?tabs=python#ncrontab-expressions). 
 
## Deploy

Create the FunctionApp in Azure and set up the environment variables in `Settings -> Configuration -> Application settings`.
    
Then deploy:

	func azure functionapp publish ita-taxonomy-normalizer
