"""
Modern minimalistic UI for Selenium self-healing agent using CustomTkinter.

Features:
- Enter URL and Dump UI
- Run LLM agent
- Run Selenium script
- View ui_dump.json and selenium_action_script.py
- Colorful, responsive layout with modern look
"""

import threading
import time
import customtkinter as ctk
from main import dump_ui, run_llm_agent
from agent.tools import run_selenium, read_ui_json, read_selenium_script

ctk.set_appearance_mode("Light")  # "Dark" for dark mode
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

class ModernApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Selenium Self-Healing Agent")
        self.geometry("950x750")
        self.minsize(900, 700)

        # Top frame: URL input and buttons
        self.top_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        self.top_frame.pack(fill="x", padx=15, pady=10)

        self.url_var = ctk.StringVar()
        ctk.CTkLabel(self.top_frame, text="Website URL:", font=("Roboto", 12, "bold")).pack(side="left", padx=(10, 5))
        self.url_entry = ctk.CTkEntry(self.top_frame, textvariable=self.url_var, width=500)
        self.url_entry.pack(side="left", padx=(0,10))

        self.dump_btn = ctk.CTkButton(self.top_frame, text="Dump UI", width=90, command=self.start_dump)
        self.dump_btn.pack(side="left", padx=5)
        self.agent_btn = ctk.CTkButton(self.top_frame, text="Run Agent", width=100, command=self.start_agent)
        self.agent_btn.pack(side="left", padx=5)
        self.run_btn = ctk.CTkButton(self.top_frame, text="Run Script", width=100, command=self.start_run_script)
        self.run_btn.pack(side="left", padx=5)

        # Middle frame: Logs
        self.log_frame = ctk.CTkFrame(self, fg_color="#f7f7f7")
        self.log_frame.pack(fill="both", expand=True, padx=15, pady=(0,10))
        ctk.CTkLabel(self.log_frame, text="Status Log:", font=("Roboto", 12, "bold")).pack(anchor="w", padx=10, pady=5)
        self.log_area = ctk.CTkTextbox(self.log_frame, height=200, wrap="word", font=("Consolas", 10))
        self.log_area.pack(fill="both", expand=True, padx=10, pady=(0,10))
        self.log_area.configure(state="disabled")

        # Bottom frame: UI dump and Selenium script
        self.bottom_frame = ctk.CTkFrame(self, fg_color="#f7f7f7")
        self.bottom_frame.pack(fill="both", expand=True, padx=15, pady=(0,10))

        # UI dump
        self.ui_frame = ctk.CTkFrame(self.bottom_frame)
        self.ui_frame.pack(side="left", fill="both", expand=True, padx=(0,7))
        ctk.CTkLabel(self.ui_frame, text="UI Dump (ui_dump.json)", font=("Roboto", 12, "bold")).pack(anchor="w", padx=5, pady=5)
        self.ui_area = ctk.CTkTextbox(self.ui_frame, wrap="word", font=("Consolas", 10))
        self.ui_area.pack(fill="both", expand=True, padx=5, pady=(0,5))
        self.ui_refresh_btn = ctk.CTkButton(self.ui_frame, text="Refresh UI Dump", width=120, command=self.show_ui_dump)
        self.ui_refresh_btn.pack(pady=5)

        # Selenium script
        self.script_frame = ctk.CTkFrame(self.bottom_frame)
        self.script_frame.pack(side="left", fill="both", expand=True, padx=(7,0))
        ctk.CTkLabel(self.script_frame, text="Selenium Script", font=("Roboto", 12, "bold")).pack(anchor="w", padx=5, pady=5)
        self.script_area = ctk.CTkTextbox(self.script_frame, wrap="word", font=("Consolas", 10))
        self.script_area.pack(fill="both", expand=True, padx=5, pady=(0,5))
        self.script_refresh_btn = ctk.CTkButton(self.script_frame, text="Refresh Script", width=120, command=self.show_script)
        self.script_refresh_btn.pack(pady=5)

        # Initial load
        self.show_ui_dump()
        self.show_script()

    # Logging
    def append_log(self, text):
        self.log_area.configure(state="normal")
        self.log_area.insert("end", f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {text}\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    def set_buttons_state(self, state="normal"):
        self.dump_btn.configure(state=state)
        self.agent_btn.configure(state=state)
        self.run_btn.configure(state=state)
        self.ui_refresh_btn.configure(state=state)
        self.script_refresh_btn.configure(state=state)

    # Tasks
    def start_dump(self):
        url = self.url_var.get().strip()
        if not url:
            ctk.CTkMessageBox.show_error("Error", "URL is required")
            return
        threading.Thread(target=self._dump_task, args=(url,), daemon=True).start()

    def _dump_task(self, url):
        self.append_log(f"Starting UI dump for {url}")
        self.set_buttons_state("disabled")
        try:
            dump_ui(url)
            self.append_log("✅ UI dump completed")
            self.show_ui_dump()
        except Exception as e:
            self.append_log(f"❌ Error during UI dump: {e}")
        finally:
            self.set_buttons_state("normal")

    def start_agent(self):
        url = self.url_var.get().strip()
        if not url:
            ctk.CTkMessageBox.show_error("Error", "URL is required")
            return
        threading.Thread(target=self._agent_task, args=(url,), daemon=True).start()

    def _agent_task(self, url):
        self.append_log(f"Running LLM agent for {url}")
        self.set_buttons_state("disabled")
        try:
            dump_ui(url)
            self.append_log("UI dumped — invoking agent")
            run_llm_agent(url)
            self.append_log("✅ LLM agent finished")
            self.show_script()
        except Exception as e:
            self.append_log(f"❌ Error during agent run: {e}")
        finally:
            self.set_buttons_state("normal")

    def start_run_script(self):
        threading.Thread(target=self._run_script_task, daemon=True).start()

    def _run_script_task(self):
        self.append_log("Running Selenium script...")
        self.set_buttons_state("disabled")
        try:
            output = run_selenium()
            self.append_log("✅ Selenium run completed — output below:")
            self.append_log(output)
        except Exception as e:
            self.append_log(f"❌ Error running script: {e}")
        finally:
            self.set_buttons_state("normal")

    # Show UI dump
    def show_ui_dump(self):
        try:
            data = read_ui_json()
        except Exception as e:
            data = f"❌ Error reading ui_dump.json: {e}"
        self.ui_area.delete("1.0", "end")
        self.ui_area.insert("end", data)

    # Show Selenium script
    def show_script(self):
        try:
            data = read_selenium_script()
        except Exception as e:
            data = f"❌ Error reading selenium_action_script.py: {e}"
        self.script_area.delete("1.0", "end")
        self.script_area.insert("end", data)


if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()
