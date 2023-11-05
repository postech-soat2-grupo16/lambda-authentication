import json
import psycopg2
import boto3
import os

def main(event, context):
    response = {
        "statusCode": 401,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "Unauthorized: Missing or invalid authentication credentials."
        })
    }
    if 'body' in event:
        request_body = json.loads(event['body'])
        if 'cpf' in request_body:
            cpf = request_body['cpf']
            result = get_cliente(cpf)
            if len(result) > 0:
                jwt = build_jwt(cpf)
                response = {
                    "statusCode": 200,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": json.dumps({
                        "token": jwt
                    }) 
                }
    return response

def get_secrets():
    try:
        # Create a Secrets Manager client
        secret_name = os.environ['SECRET_NAME']
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name='us-east-1'
        )
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(get_secret_value_response['SecretString'])    
        return secret
    except Exception as e:
        print("Error! ", e)
        sys.exit(1) 

def get_cliente(cpf):
    try:
        #Get secrets
        secret = get_secrets()
        db_username = secret['username']
        db_password = secret['password']
        db_name = secret['dbname']
        db_host = secret['host']
        db_port = secret['port']

        #DB connection
        connection = psycopg2.connect(
            host=db_host,
            dbname=db_name,
            user=db_username,
            password=db_password,
            port=db_port
        )
        cursor = connection.cursor()
        print("Connected to the database")

        #Build and Query
        query = "SELECT * FROM clientes WHERE cpf=%s LIMIT 1"
        cursor.execute(query, (cpf,))

        # Fetch the results
        result = cursor.fetchall()
        print('resultado: ', result)

        #Close connection
        cursor.close()
        connection.close()
        print("Database connection closed")

        return result
    except Exception as e:
        print("Error! ", e)
        sys.exit(1)

def build_jwt(cpf):
    try:
        print("build jwt")
        return "123"
    except Exception as e:
        print("Error! ", e)
        sys.exit(1)
    