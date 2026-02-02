import os
from dotenv import load_dotenv

load_dotenv()


GEMINI_API_KEY = os.getenv("API_KEY")


GEMINI_MODEL = "gemini-1.5-flash"


UI_DUMP_PATH = "ui_dump.json"
SELENIUM_SCRIPT_PATH = "selenium_action_script.py"
