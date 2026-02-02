from dotenv import load_dotenv
from langsmith import traceable
from agent.llm_agent import get_llm
from ui_scraper import scrape_all_elements, clean_element, filter_element
from selenium import webdriver
import json
import time
from langchain_core.messages import HumanMessage
from agent.tools import read_ui_json, read_selenium_script, write_selenium_script, run_selenium
import ast
import re

load_dotenv()


def dump_ui(url: str):
    """Dump all visible and important UI elements into ui_dump.json"""
    driver = webdriver.Chrome()
    driver.get(url)

    elements = scrape_all_elements(driver)
    ui_data = []

    for el in elements:
        try:
            cleaned = clean_element(el)
            if filter_element(cleaned):
                ui_data.append(cleaned)
        except Exception:
            continue

    driver.quit()

    with open("ui_dump.json", "w", encoding="utf-8") as f:
        json.dump(ui_data, f, indent=2, ensure_ascii=False)

    print(f"📄 UI Dumped: {len(ui_data)} elements saved to ui_dump.json")

def run_llm_agent(url: str):
    """Use LLM to fix Selenium script automatically using the dumped UI, with a fix log"""

    ui_data = read_ui_json()
    selenium_code = read_selenium_script()

    # Escape JSON and code for safe LLM input
    safe_ui_json = json.dumps(ui_data)
    safe_selenium_code = repr(selenium_code)  # converts to a Python-safe string literal

    user_prompt = f"""
Website URL: {url}

UI JSON:
{safe_ui_json}

Selenium Script:
{safe_selenium_code}

Instructions:
- Only fix broken locators
- Output valid Python code only
- Include # FIX: comments for each change
"""

    llm_instance = get_llm()
    if llm_instance is None:
        print("❌ LLM not initialized. Exiting...")
        return

    # Rest of your code for retries, syntax validation, writing script, etc.


    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        print(f"\n🔄 LLM Attempt {attempt}...")
        response = llm_instance.invoke([HumanMessage(content=user_prompt)])
        raw = response.content.strip()

        # Extract code from Markdown fenced blocks if present
        code_match = re.search(r"```(?:python)?\s*(.*?)\s*```", raw, re.S | re.I)
        if code_match:
            candidate = code_match.group(1)
        else:
            # Fallback: find first line that looks like Python code and take from there
            lines = raw.splitlines()
            start_index = 0
            for i, line in enumerate(lines):
                if re.match(r'^\s*(import|from|def|class|driver|#)', line):
                    start_index = i
                    break
            candidate = "\n".join(lines[start_index:]).strip()

        fixed_code = candidate

        if not fixed_code:
            print("⚠️ LLM returned no code.")
            if attempt == max_attempts:
                print("❌ Maximum retries reached. Exiting...")
                print("Last LLM response:\n", raw)
                return
            continue

        # Validate Python syntax
        try:
            ast.parse(fixed_code)
        except SyntaxError as e:
            print(f"⚠️ LLM returned invalid Python → {e}")
            if attempt == max_attempts:
                print(" Maximum retries reached. Exiting...")
                print("Last LLM response:\n", raw)
                return
            continue  # retry

        # Write valid Python using safe tool
        result = write_selenium_script(fixed_code)
        print(f"🛠️ {result}")

        # Extract FIX comments to create a progress log
        fix_comments = re.findall(r"^\s*#\s*FIX:.*", fixed_code, re.MULTILINE)
        if fix_comments:
            print("\n Fix Log (changes applied by AI):")
            for comment in fix_comments:
                print(f"- {comment[2:].strip()}")
        else:
            print("\n Fix Log: No specific FIX comments found")

        # Run the script safely
        output = run_selenium()
        print(output)
        break  # success


@traceable(name="selenium_self_healing_main")
def main():
    print("🤖 Selenium Self-Healing Agent")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    url = input("🌐 Enter website URL: ").strip()
    if not url:
        print("❌ URL is required")
        return

    print("\n🔍 Step 1: Dumping UI elements...")
    dump_ui(url)
    print("✅ UI dumped successfully")

    print("\n🛠️ Step 2: Running Selenium agent...")
    start = time.time()
    run_llm_agent(url)
    duration = round(time.time() - start, 2)
    print(f"\n⏱️ Total execution time: {duration} seconds")


if __name__ == "__main__":
    main()
