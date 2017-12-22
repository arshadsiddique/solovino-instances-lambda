# Solovino Instances - 12/2017
Control EC2 instances from Alexa Skills throw a Lambda in Python

## Step 1
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

## Step 2
* On Lambda create a new function on Python 2.7 (https://console.aws.amazon.com/lambda/home?region=us-east-1#/create)
* Paste the code
* Link your Alexa Skill with your new AWS Lambda ARN

## Step 3
* On IAM Manager Console create a new role (https://console.aws.amazon.com/iam/home?#/roles)
  * The role must have a policy like next:
    * (List) DescribeInstances - All resources
    * (List) DescribeInstanceStatus - All resources
    * (Write) StartInstances - All resources
    * (Write) StopInstances - All resources
* Link the new role to your Lambda function

## Step 4
* Prepare your EC2 enviroments creating 3 instances
* Each instance must have a tag '*enviroment*' with the possible values staging, prod, dev

# Step 5
* Test your Alexa Skill on the tab Test > Service Simulator
* For a better debugging, use the JSON Service Request and create a Test Event directly on Lambda
* If everything is ok, test with your Amazon Echo Dot by using Skills Beta Testing (it requires all the configuration steps completed)

#Step 6
* **Publish!! :D**
