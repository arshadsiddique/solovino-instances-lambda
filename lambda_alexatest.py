from __future__ import print_function 
import boto3 

def lambda_handler(event, context):
   if event['session']['new']:
       on_session_started({'requestId': event['request']['requestId']}, event['session'])

   if event['request']['type'] == "LaunchRequest": 
       return on_launch(event['request'], event['session']) 
   elif event['request']['type'] == "IntentRequest": 
       return on_intent(event['request'], event['session']) 
   elif event['request']['type'] == "SessionEndedRequest": 
       return on_session_ended(event['request'], event['session']) 

def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId'] + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
   print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])
   return get_welcome_response()

def get_welcome_response():
   session_attributes = {}
   card_title = "Welcome"
   speech_output = "Welcome to the Solovino Instances. " \
                   "Please tell me, What is my purpose?"

   reprompt_text = "What is my purpose?"
    
   should_end_session = False
   return build_response(session_attributes, build_speechlet_response(
      card_title, speech_output, reprompt_text, should_end_session))

def on_intent(intent_request, session): 
   print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId']) 
   intent = intent_request['intent'] 
   intent_name = intent_request['intent']['name'] 
   if intent_name == "startInstanceIntent": 
       return start_ec2(intent, session) 
   elif intent_name == "stopInstanceIntent": 
       return stop_ec2(intent, session) 
   elif intent_name == "getStatusIntent": 
       return getStatus(intent, session) 
   elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent": 
       return handle_session_end_request() 
   else: 
       raise ValueError("Invalid intent") 

def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])

def start_ec2(intent, session): 
   card_title = "Starting" 
   session_attributes = {} 
   instance_value = intent['slots']['Instance']['value'] 
   instanceValue = instance_value.lower() 
   ec2 = boto3.client('ec2', region_name='us-east-1') 
   response = ec2.describe_instances() 
   insId = [] 
   for reservation in response["Reservations"]: 
       for instance in reservation["Instances"]: 
           for i in instance["Tags"]:
               if(i["Key"]=='enviroment' and i["Value"]==instanceValue): 
                  insId.append(instance["InstanceId"])

   ec2.start_instances(InstanceIds=insId) 
   speech_output = "Starting instance "+ instance_value + ". Thank you for using Solovino Instances" 
   should_end_session = True 
   return build_response(session_attributes, build_speechlet_response( 
       card_title, speech_output, None, should_end_session))

def stop_ec2(intent, session): 
   card_title = "Stopping" 
   session_attributes = {} 
   instance_value = intent['slots']['Instance']['value'] 
   instanceValue = instance_value.lower() 
   ec2 = boto3.client('ec2', region_name='us-east-1') 
   response = ec2.describe_instances() 
   insId = [] 
   for reservation in response["Reservations"]: 
       for instance in reservation["Instances"]: 
           for i in instance["Tags"]:
               if(i["Key"]=='enviroment' and i["Value"]==instanceValue): 
                  insId.append(instance["InstanceId"])

   ec2.stop_instances(InstanceIds=insId) 
   speech_output = "Stopping instance "+ instance_value + ". Thank you for using Solovino Instances" 
   should_end_session = True 
   return build_response(session_attributes, build_speechlet_response( 
       card_title, speech_output, None, should_end_session))

def getStatus(intent, session): 
   card_title = "Status" 
   session_attributes = {} 
   instance_value = intent['slots']['Instance']['value'] 
   instanceValue = instance_value.lower() 
   ec2 = boto3.client('ec2', region_name='us-east-1') 
   response = ec2.describe_instances() 
   insId = [] 
   for reservation in response["Reservations"]: 
       for instance in reservation["Instances"]: 
           for i in instance["Tags"]:
               if(i["Key"]=='enviroment' and i["Value"]==instanceValue): 
                  insId.append(instance["InstanceId"])
   print(insId)
   statuses = ec2.describe_instance_status(InstanceIds=insId, IncludeAllInstances=True)
   
   state = statuses["InstanceStatuses"][0]["InstanceState"]["Name"]
   speech_output = "Your instance "+ instanceValue +" is "+ state + ". What is my purpose?" 

   should_end_session = False 
   return build_response(session_attributes, build_speechlet_response( 
       card_title, speech_output, None, should_end_session))

def handle_session_end_request():
   card_title = "Status" 
   session_attributes = {} 
   speech_output = "Good bye!. Thank you for using Solovino Instances" 
   should_end_session = True 
   return build_response(session_attributes, build_speechlet_response( 
       card_title, speech_output, None, should_end_session))

def build_speechlet_response(title, output, reprompt_text, should_end_session): 
   return { 
       'outputSpeech': { 
           'type': 'PlainText', 
           'text': output 
       }, 
       'card': { 
           'type': 'Simple', 
           'title': 'SessionSpeechlet - ' + title, 
           'content': 'SessionSpeechlet - ' + output 
       }, 
       'reprompt': { 
           'outputSpeech': { 
               'type': 'PlainText', 
               'text': reprompt_text 
           } 
       }, 
       'shouldEndSession': should_end_session 
   }

def build_response(session_attributes, speechlet_response): 
   return { 
       'version': '1.0', 
       'sessionAttributes': session_attributes, 
       'response': speechlet_response 
   }