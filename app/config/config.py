import os

from dotenv import load_dotenv

dotenv_path = '.env'
load_dotenv(dotenv_path)

OPEN_AI_KEY = os.environ.get("OPEN_AI_KEY")
