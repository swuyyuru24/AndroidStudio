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
    password = data['password']
   
    client = boto3.client('cognito-idp')
    
    try:
        resp = client.admin_initiate_auth(UserPoolId=USER_POOL_ID, 
        ClientId=CLIENT_ID,AuthFlow="ADMIN_NO_SRP_AUTH",
        AuthParameters={'USERNAME':username,
        "SECRET_HASH":getsecrethast(username),
        "PASSWORD":password},
        ClientMetadata={'username':username,'password':password})
        
    
    except Exception as e:
        exception = True 
        exceptionstr = str(e);
        print(e)
        resp = {}
        
    # initialize item to an empty dictionary
    item = {}
    
    if exception == True:
        if resp.get("AuthenticationResult"):
             item = {
                "message" :"Success",
                "error" : False,
                "data" : {
                    "id_token" : resp["AuthenticationResult"]["idToken"],
                    "refresh_token" : resp["AuthenticationResult"]["RefreshToken"],
                    "access_token" : resp["AuthenticationResult"]["access_token"],
                    "expires_in" : resp["AuthenticationResult"]["ExpiresIn"],
                    "token_type": resp["AuthenticationResult"]["TokenType"]
                }
            }
        return{
            "item" : {
                "message" :"Failure",
                "error" : True,
                "data" :""
             },
             'statusCode': 400,
             'body': json.dumps(item)
        }
    else:    
        return {
            'statusCode': 200,
            'body': json.dumps({"message":'Login Success'})
        }
