import cohere
from rich import print
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
CohereAPIkey = env_vars.get("CohereAPIkey")
co = cohere.Client(api_key=CohereAPIkey)
