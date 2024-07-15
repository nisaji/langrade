import os
from dotenv import load_dotenv


def pytest_configure(config):
    load_dotenv()


def get_api_key():
    return os.getenv("OPENAI_API_KEY")
