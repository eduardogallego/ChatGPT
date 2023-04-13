import openai

from utils import Config

config = Config()
openai.api_key = config.get('api_key')
models = openai.Model.list()
pass
