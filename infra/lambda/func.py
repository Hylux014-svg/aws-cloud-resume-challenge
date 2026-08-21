import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cloudresume-test')

def lambda_handler(event, context):
    response = table.update_item(
        Key={
            'id': '0'
        },
        # 使用 #v 代替保留字 views
        UpdateExpression='ADD #v :inc',
        ExpressionAttributeNames={
            '#v': 'views'  # 将 #v 映射到真实的列名 views
        },
        ExpressionAttributeValues={
            ':inc': 1
        },
        ReturnValues='UPDATED_NEW'
    )
    
    # 提取更新后的 views 属性值
    views = int(response['Attributes']['views'])
    
    # 返回 API Gateway 所需的标准 HTTP 响应格式
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        },
        'body': json.dumps({'views': views})
    }