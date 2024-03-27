import json
import boto3
import hmac
import base64
import hashlib

USER_POOL_ID = 'us-east-2_QuxoUqMzR'
CLIENT_ID='3q1r0m9k1ne1gog3a3kip6rfdd'
CLIENT_SECRET='avae52dj3gdmislacengdcj2t3iomojuidbsbtf24k8srg2mhko'

def getsecrethast(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),msg = str(msg).encode('utf-8'),digestmod=hashlib.sha256).digest()
    d2= base64.b64encode(dig).decode()
    return d2

def lambda_handler(event, context):
    exception = False
    data = json.loads(event['body'])  
    username = data['username']
    code = data['code']
    # email = data['email']
    # print(f"{username} and {password}  and {email}")
    
    client = boto3.client('cognito-idp')
    
    try:
        client.confirm_sign_up(ClientId=CLIENT_ID,SecretHash=getsecrethast(username),Username=username,ConfirmationCode=code,ForceAliasCreation=False)
        
    except Exception as e:
        exception = True 
        exceptionstr = "error"
        print(e)
    # TODO implement
    if exception == True:
        return{
            'statusCode': 200,
            'body': json.dumps({"message" : exceptionstr})
        }
    else:    
        return {
            'statusCode': 200,
            'body': json.dumps({"message":'Success in Confirmation'})
        }
