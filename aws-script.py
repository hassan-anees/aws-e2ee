import boto3
from dynamodb_encryption_sdk import EncryptedTable
from dynamodb_encryption_sdk.material_providers.aws_kms import AwsKmsCryptographicMaterialsProvider
from environs import Env
from dynamodb_encryption_sdk.structures import AttributeActions, EncryptionContext, TableInfo
from dynamodb_encryption_sdk.identifiers import CryptoAction


table_name = "Patients"
env = Env()
env.read_env('local.env', False)
session = boto3.Session(aws_access_key_id=env('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=env('AWS_SECRET_ACCESS_KEY'),
                        region_name=env('AWS_REGION'))
dynamodb = session.resource('dynamodb')


def create_table(table_name):
    table = dynamodb.Table(table_name)
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'pid',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'pid',
                    'AttributeType': 'N'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }

        )
        print(table)
    except Exception as e:
        print(e)


def print_table(table_name):
    table = dynamodb.Table(table_name)
    print(table)
    items = table.scan()['Items']
    for item in items:
        print(item)


def create_encrypted_table(table_name):
    table = dynamodb.Table(table_name)
    kms_key_id = env('AWS_CMK_ID')
    kms_cmp = AwsKmsCryptographicMaterialsProvider(key_id=kms_key_id)

    # Tell the encrypted table to encrypt and sign all attributes except one.
    actions = AttributeActions(
        default_action=CryptoAction.ENCRYPT_AND_SIGN,
        attribute_actions={
            'lastvisit': CryptoAction.DO_NOTHING,
            'name': CryptoAction.DO_NOTHING
        }
    )

    # Use these objects to create an encrypted table resource.
    encrypted_table = EncryptedTable(
        table=table,
        materials_provider=kms_cmp,
        attribute_actions=actions
    )

    return encrypted_table


def send_encrypted_payload(encrypted_table, plaintext_object):
    encrypted_table.put_item(Item=plaintext_object)


def decrypt_item(encrypted_table, partition_key):
    return encrypted_table.get_item(Key=partition_key)['Item']


def main():
    create_table(table_name)
    encrypted_table = create_encrypted_table(table_name)

    plaintext_object = {
        'pid': 62,
        'name': 'tyler',
        'medicalnotes': 'tendency to have 6 cups of coffee per day',
        'age': 22,
        'lastvisit': '2022-09-12'
    }
    searchItem = {'pid': 62}
    send_encrypted_payload(encrypted_table, plaintext_object)
    plaintext_item = decrypt_item(encrypted_table, searchItem)
    print(plaintext_item)
    print('object sent')


if __name__ == "__main__":
    main()
