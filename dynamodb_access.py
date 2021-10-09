import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ToDoTable')


# テーブルデータ全取得
def scan():
    data = table.scan()
    items = data['Items']
    print(items)
    return items


# レコード検索
def query(items):
    data = table.query(
        KeyConditionExpression = Key('userOrTask').eq(items['userOrTask']) & Key('id').eq(items['id'])
    )
    items = data['Items']
    print(items)
    return items


# レコード追加
def put(items):
    res = {}
    if items['userOrTask'] == 'User':
        res = table.put_item(
            Item = {
                'userOrTask': items['userOrTask'],
                'id': items['id'],
                'name': items['name']
            }
        )
    else:
        res = table.put_item(
            Item = {
                'userOrTask': items['userOrTask'],
                'id': items['id'],
                'name': items['name'],
                'workerId': items['workerId']
            }
        )
    if res['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(res)
    else:
        print('PUT Successed.')
    return res


# レコード削除
def delete(items):
    res = table.delete_item(
        Key = {
            'userOrTask': items['userOrTask'],
            'id': items['id']
        }
    )
    if res['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(res)
    else:
        print('DELETE Successed.')
    return res


def lambda_handler(event, context):
    print('Received Event:' + json.dumps(event))
    operation_type = event['operation_type']
    try:
        if operation_type == 'SCAN':
            return scan()

        items = event['items']
        if operation_type == 'QUERY':
            return query(items)
        elif operation_type == 'PUT':
            return put(items)
        elif operation_type == 'DELETE':
            return delete(items)
    except Exception as e:
        print(e)
