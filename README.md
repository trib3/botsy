# Botsy

## Requirements

* [Serverless installed](https://serverless.com/)
* [Python 3.6 installed](https://www.python.org/downloads/release/python-360/)
* [awslogs (optional)](awslogs get /aws/lambda/botsy ALL --watch)

## Setup process
* Follow [this video](https://www.youtube.com/watch?v=mRkUnA3mEt4&list=PLIIjEI2fYC-C3NJF7a4-Cvh5hjdCmrVmN&index=1) for instructions
on installing serverless
* Create a `serverless.env.yaml` file locally and make sure it's added to your `.gitignore`. Place the environment variable values here.

A full summary of all the available properties for `serverless.yaml` for AWS: https://serverless.com/framework/docs/providers/aws/guide/serverless.yml/#serverlessyml-reference

## Packaging and deployment
```
serverless deploy
```
For more information on the deploy function, go [here](https://serverless.com/framework/docs/providers/aws/cli-reference/deploy/)

After running `serverless deploy` the message will prompt you to run the `serverless` command. This will connect your serverless app to the serverless online dashboard.
If you do this you only get 1 million free invocations. It shows stats and such, but be careful before connecting.

## Tail Lambda function logs
I like to use [awslogs](awslogs get /aws/lambda/botsy ALL --watch).
```
awslogs get /aws/lambda/botsy ALL --watch
```

## Cleanup

To remove the deployed service from AWS

```
serverless remove
```
