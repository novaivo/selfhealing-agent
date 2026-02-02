# Selenium Agent

An intelligent automation agent that combines Selenium WebDriver with LLM capabilities to interact with web applications autonomously.

## Project Structure

```
.
├── config.py                 # Configuration settings
├── main.py                   # Main entry point
├── requirements.txt          # Python dependencies
├── tk_ui.py                  # Tkinter UI interface
├── ui_scraper.py             # Web UI scraper
├── selenium_action_script.py # Selenium action executor
├── ui_dump.json              # UI element snapshot
├── index.html                # Web UI template
├── agent/
│   ├── llm_agent.py          # LLM agent logic
│   └── tools.py              # Agent tools and utilities
└── templates/
    └── index.html            # HTML templates
```

## Features

- **LLM-Powered Automation**: Uses an LLM agent to understand and execute web automation tasks
- **Selenium Integration**: Automates browser interactions using Selenium WebDriver
- **Web UI Scraping**: Extracts and analyzes web page structure
- **Desktop UI**: Tkinter-based interface for interaction
- **Tool System**: Extensible tools for various automation tasks

## Installation

1. Clone or extract this project
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # macOS/Linux
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run the main application:
```bash
python main.py
```

### Run the Tkinter UI:
```bash
python tk_ui.py
```

### Configure settings:
Edit `config.py` to adjust configuration parameters such as:
- Browser settings
- LLM model parameters
- Timeout values
- UI scraper options

## Requirements

See `requirements.txt` for all Python package dependencies. Core requirements include:
- Selenium WebDriver
- Web scraping libraries
- LLM integration libraries

## Configuration

Edit `config.py` to customize:
- Selenium WebDriver settings
- LLM model and API keys
- Application behavior and timeouts

## Development

### Adding New Tools
Extend the agent's capabilities by adding new tools in `agent/tools.py`

### Modifying UI Logic
Update UI interaction logic in `selenium_action_script.py` or `ui_scraper.py`

## License

[Add your license information here]

## Support

For issues or questions, please refer to the project documentation or create an issue.
