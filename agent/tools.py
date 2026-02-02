import subprocess
import sys
from pathlib import Path
from langchain.tools import tool
import ast

BASE_DIR = Path(__file__).resolve().parent.parent
UI_JSON_PATH = BASE_DIR / "ui_dump.json"
SELENIUM_SCRIPT_PATH = BASE_DIR / "selenium_action_script.py"


def read_ui_json() -> str:
    """Read the dumped UI JSON file and return its content as a string (local helper)."""
    if not UI_JSON_PATH.exists():
        return "ERROR: ui_dump.json not found."
    return UI_JSON_PATH.read_text(encoding="utf-8")


@tool
def read_ui_json_tool(tool_input: str) -> str:
    """Tool wrapper for LLM usage of read_ui_json."""
    return read_ui_json()


def read_selenium_script() -> str:
    """Read the current selenium_action_script.py and return its content as a string (local helper)."""
    if not SELENIUM_SCRIPT_PATH.exists():
        return "ERROR: selenium_action_script.py not found."
    return SELENIUM_SCRIPT_PATH.read_text(encoding="utf-8")


@tool
def read_selenium_script_tool(tool_input: str) -> str:
    """Tool wrapper for LLM usage of read_selenium_script."""
    return read_selenium_script()


def write_selenium_script(code: str) -> str:
    """
    Write valid Python code to selenium_action_script.py.
    Rejects code that is empty or invalid Python.
    (Local helper)
    """
    if not code.strip():
        return "ERROR: Empty code received."

    # Validate Python syntax
    try:
        ast.parse(code)
    except SyntaxError as e:
        return f"REJECTED: Invalid Python → {e}"

    # Write only valid Python
    SELENIUM_SCRIPT_PATH.write_text(code, encoding="utf-8")
    return "SUCCESS: Selenium script written"


@tool
def write_selenium_script_tool(tool_input: str) -> str:
    """Tool wrapper for LLM usage of write_selenium_script."""
    return write_selenium_script(tool_input)


def run_selenium() -> str:
    """
    Execute selenium_action_script.py only if it is valid Python.
    Returns the STDOUT and STDERR from the script execution. (Local helper)
    """
    if not SELENIUM_SCRIPT_PATH.exists():
        return "ERROR: Selenium script not found"

    code = SELENIUM_SCRIPT_PATH.read_text(encoding="utf-8")

    # Validate syntax before running
    try:
        ast.parse(code)
    except SyntaxError as e:
        return f"ERROR: Script is invalid → {e}"

    try:
        result = subprocess.run(
            [sys.executable, str(SELENIUM_SCRIPT_PATH)],
            capture_output=True,
            text=True,
            timeout=60
        )

        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    except subprocess.TimeoutExpired:
        return "ERROR: Selenium execution timed out."
    except Exception as e:
        return f"ERROR running Selenium: {e}"


@tool
def run_selenium_tool(tool_input: str) -> str:
    """Tool wrapper for LLM usage of run_selenium."""
    return run_selenium()