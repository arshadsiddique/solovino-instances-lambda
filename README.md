# Solovino Instances - 12/2017
Control EC2 instances from Alexa Skills throw a Lambda in Python

Autor: [Mr.Jack](https://keybase.io/mrjack)

## DEMO

[![Solovino Instances](https://img.youtube.com/vi/Q1_1h3W7SI8/0.jpg)](https://www.youtube.com/watch?v=Q1_1h3W7SI8)

## Step 1 (Alexa Skill Kit)
* Create a new Alexa Skill (https://developer.amazon.com/edw/home.html#/skills)
* On your model create 3 Intents
  * getStatusIntent
  "status server {Instance}"
  * startInstanceIntent
  "start server {Instance}"
  * stopInstanceIntent
  "stop server {Instance}"
* On your model create 1 Slot type: INSTANCE_NAME
  * Add 3 possible values: *staging*, *prod*, *dev* (you can add synonims)
* {Instance} should be type INSTANCE_NAME

## Step 2 (Lambda)
* On Lambda create a new function on Python 2.7 (https://console.aws.amazon.com/lambda/home?region=us-east-1#/create)
* Paste the [code](lambda_function.py)
* Link your Alexa Skill with your new AWS Lambda ARN
* Select Alexa Skill Kit from Designer and add it to your lambda function

## Step 3 (AIM Manager Console)
* On IAM Manager Console create a new role (https://console.aws.amazon.com/iam/home?#/roles)
  * The role must have a policy like next:
    * (List) DescribeInstances - All resources
    * (List) DescribeInstanceStatus - All resources
    * (Write) StartInstances - All resources
    * (Write) StopInstances - All resources
* Link the new role to your Lambda function

## Step 4 (EC2)
* Prepare your EC2 enviroments creating 3 instances
* Each instance must have a tag '*enviroment*' with the possible values staging, prod, dev

## Step 5 (Testing)
* Test your Alexa Skill on the tab Test > Service Simulator
* For a better debugging, use the JSON Service Request and create a Test Event directly on Lambda
* If everything is ok, test with your Amazon Echo Dot by using Skills Beta Testing (it requires all the configuration steps completed)

## Step 6
* **Publish!! :D**
