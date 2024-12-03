import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'key.env')
load_dotenv(dotenv_path)

OK = os.environ.get('organization_key')
AK = os.environ.get('api_key')