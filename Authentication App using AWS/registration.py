import json
import boto3
import hmac
import base64
import hashlib

USER_POOL_ID = 'us-east-2_QuxoUqMzR'
CLIENT_ID='3q1r0m9k1ne1gog3a3kip6rfdd'
CLIENT_SECRET='avae52dj3gdmislacengdcj2t3iomojuidbsbtf24k8srg2mhko'

def getsecrethash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),msg = str(msg).encode('utf-8'),digestmod=hashlib.sha256).digest()
    d2= base64.b64encode(dig).decode()
    return d2


def lambda_handler(event, context):
    exception = False
    print(event)
  

    data = json.loads(event["body"])
    
    username = data['username']
    password = data['password']
    email = data['email']
    name= data['name']
    print(f"{username} and {password}  and {email}")
    user_attributes = [
    {
        'Name': "name",
        'Value': name
    },{
        'Name':"email",
        'Value':email
    }
    ]
    client = boto3.client('cognito-idp')
    
    try:
        response = client.sign_up(
    ClientId=CLIENT_ID,
    Username=username,
    Password=password,
    UserAttributes=user_attributes,SecretHash=getsecrethash(username)
)
        
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
            'body': json.dumps({"message": "Success in Registration"})
        }