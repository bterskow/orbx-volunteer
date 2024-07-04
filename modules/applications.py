import boto3
from modules.interface import Base

class Applications(Base):
	def __init__(self, env):
		aws_access_key_id = env.aws_access_key_id
		aws_secret_access_key = env.aws_secret_access_key
		dynamodb_name = env.dynamodb_name

		dynamodb = boto3.resource('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name='us-east-1')
		self.dynamodb_table = dynamodb.Table(dynamodb_name)

	def select(self, category, _for='military'):
		response_json = {
			'status': 'error',
			'err_description': ''
		}

		try:
			scan = self.dynamodb_table.scan(
				ScanFilter={
			        'for': {
			            'AttributeValueList': [
			                _for,
			            ],
			            'ComparisonOperator': 'EQ'
			        },

			        'category': {
			        	'AttributeValueList': [
			                category,
			            ],
			            'ComparisonOperator': 'EQ'
			        }
			    }
			)

			items = scan.get('Items', [])
			if len(items) == 0:
				response_json['err_description'] = 'Наразі дані відсутні!'
				return response_json

			response_json['items'] = items
			response_json['status'] = 'success'

		except Exception as e:
			response_json['err_descritpion'] = str(e)

		return response_json