import os

class Meta(type):
	def __new__(cls, name, based, dct):
		return super().__new__(cls, name, based, dct)

class Env(metaclass=Meta):
	def __init__(self):
		self.bot_token = os.environ.get('bot_token')
		self.aws_access_key_id = os.environ.get('aws_access_key_id')
		self.aws_secret_access_key = os.environ.get('aws_secret_access_key')
		self.dynamodb_name = os.environ.get('dynamodb_name')
		self.google_from_url = os.environ.get('google_from_url')
