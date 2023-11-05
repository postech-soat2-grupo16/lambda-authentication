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
        if 'cpf' not in request_body:
            return response
        else:
            cpf = request_body['cpf']
            result = get_cliente(cpf)
            print('CPFs encontrados: ', len(result))
            if len(result) > 0:
                jwt = build_jwt(cpf)
                return {
                    "statusCode": 200,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": json.dumps({
                        "token": jwt
                    }) 
                }
    else:
        return response

def get_secrets():
    # Create a Secrets Manager client
    secret_name = "rds/fastfood/secret"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-east-1'
    )
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(get_secret_value_response['SecretString'])    
    return secret

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
        query = "SELECT * FROM clientes WHERE cpf=%s"
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
    print("build jwt")
    return "123"
    