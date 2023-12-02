import boto3
import uuid

dynamo = boto3.client(service_name='dynamodb')


def lambda_handler(event, context):
    
    unique_id =uuid.uuid4()
    size=event["interpretations"]["intent"]["slots"]["tamanho"]["value"]["resolvedValues"][0]
    flavor= event["interpretations"]["intent"]["slots"]["sabor"]["value"]["resolvedValues"][0]
    item = {
            "unique_id": {"S": unique_id},
            "tamanho": {
                "S": size
            },
            "sabor": {
                "S": flavor
            },
        }
    
    dynamo.put_item(TableName='test-lex', Item=item)

    intent_response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "confirmationState": "Confirmed",
                "name": "pedidoIntent",
                "state": "Fulfilled"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "lambda invocada com sucesso"
            }
        ]
    }

    return intent_response
