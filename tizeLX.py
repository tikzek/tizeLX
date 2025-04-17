#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TizeLX v2.1 - Terminal Weaponizer
# By: DarkHacker (Improved Version)

import os
import gi
import json
import subprocess
import hashlib
import logging
from datetime import datetime
from cryptography.fernet import Fernet
from getpass import getuser

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

# Configure logging
logging.basicConfig(
    filename=os.path.expanduser("~/.tizelx/tizelx.log"),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class CyberTerminal(Gtk.Window):
    def __init__(self):
        super().__init__(title=f"TizeLX // {getuser()}@darknet")
        self.set_default_size(1100, 750)
        self.set_position(Gtk.WindowPosition.CENTER)

        # Security configuration
        self.encryption_key = self.load_or_create_key()
        self.terminal = self.detect_terminal()
        self.hacker_font = "Monospace 10"

        # Initialize UI
        self.set_style()
        self.create_ui()
        self.load_config()

    def set_style(self):
        """Set advanced hacker-style UI with animations."""
        css = """
        * {
            background-color: #0A0A0A;
            color: #20C20E;
            font: Monospace 10;
            border-color: #20C20E;
        }
        .danger {
            color: #FF0000;
            text-shadow: 0 0 3px #FF0000;
        }
        .hacker-mode {
            background-image: linear-gradient(to right, 
                            rgba(32, 194, 14, 0.1), 
                            rgba(32, 194, 14, 0.05));
            border: 1px solid #20C20E;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def create_ui(self):
        """Create the main UI with tabs and status bar."""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        # Header
        header = Gtk.Label(label=f"┌─[TizeLX @ Kali Linux]─[Mode: HACKER]─[Term: {self.terminal}]")
        header.set_xalign(0)
        header.set_margin_start(10)

        # Notebook for tabs
        self.notebook = Gtk.Notebook()
        self.notebook.set_border_width(5)

        # Tabs
        self.create_terminal_tab()
        self.create_exploit_tab()

        # Status bar
        self.status = Gtk.Statusbar()
        self.status_id = self.status.get_context_id("system")
        self.update_status("READY")

        # Assemble UI
        main_box.pack_start(header, False, False, 0)
        main_box.pack_start(self.notebook, True, True, 0)
        main_box.pack_end(self.status, False, False, 0)

        self.add(main_box)

    def create_terminal_tab(self):
        """Create the terminal customization tab."""
        tab_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        # Theme selector
        theme_box = Gtk.Box(spacing=10)
        self.theme_combo = Gtk.ComboBoxText()
        for theme in ["DarkMatrix", "MrRobot", "CyberPunk", "StealthMode"]:
            self.theme_combo.append_text(theme)
        theme_box.pack_start(Gtk.Label(label="SELECT THEME:"), False, False, 0)
        theme_box.pack_start(self.theme_combo, False, False, 0)

        # Config editor
        scrolled = Gtk.ScrolledWindow()
        self.config_editor = Gtk.TextView()
        self.config_editor.set_monospace(True)
        self.config_editor.set_wrap_mode(Gtk.WrapMode.NONE)
        scrolled.add(self.config_editor)

        # Action buttons
        btn_box = Gtk.Box(spacing=5)
        apply_btn = Gtk.Button(label="APPLY CONFIG")
        apply_btn.connect("clicked", self.apply_terminal_config)
        apply_btn.get_style_context().add_class("hacker-mode")
        btn_box.pack_end(apply_btn, False, False, 0)

        # Assemble tab
        tab_box.pack_start(theme_box, False, False, 5)
        tab_box.pack_start(scrolled, True, True, 0)
        tab_box.pack_end(btn_box, False, False, 5)

        self.notebook.append_page(tab_box, Gtk.Label(label=">_ TERMINAL"))

    def create_exploit_tab(self):
        """Create the exploit tools tab."""
        tab_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        # Tool buttons
        tools = [
            ("NETSCAN", "nmap -T4 -A -v"),
            ("CRACK", "john --format=sha256"),
            ("SNIFF", "tcpdump -i eth0"),
            ("BRUTE", "hydra -l admin -P pass.txt ssh://")
        ]

        grid = Gtk.Grid(column_homogeneous=True, row_spacing=5, column_spacing=5)
        for i, (name, cmd) in enumerate(tools):
            btn = Gtk.Button(label=name)
            btn.connect("clicked", self.run_hacker_tool, cmd)
            btn.get_style_context().add_class("hacker-mode")
            grid.attach(btn, i % 2, i // 2, 1, 1)

        tab_box.pack_start(grid, False, False, 5)
        self.notebook.append_page(tab_box, Gtk.Label(label=">_ EXPLOITS"))

    def apply_terminal_config(self, widget):
        """Apply the terminal configuration."""
        try:
            theme = self.theme_combo.get_active_text()
            config = self.config_editor.get_buffer().get_text(
                self.config_editor.get_buffer().get_start_iter(),
                self.config_editor.get_buffer().get_end_iter(),
                False
            )
            # Log the applied configuration
            logging.info(f"Applying theme: {theme}")
            self.update_status(f"CONFIG APPLIED: {theme}")
        except Exception as e:
            logging.error(f"Error applying config: {e}")
            self.update_status(f"ERROR: {str(e)}", True)

    def run_hacker_tool(self, widget, command):
        """Run a hacking tool."""
        try:
            subprocess.Popen(["x-terminal-emulator", "-e", command])
            self.update_status(f"RUNNING: {command.split()[0]}")
        except Exception as e:
            logging.error(f"Error running tool: {e}")
            self.update_status(f"TOOL ERROR: {str(e)}", True)

    def update_status(self, message, error=False):
        """Update the status bar."""
        context = self.status.get_style_context()
        if error:
            context.add_class("danger")
            GLib.timeout_add(3000, lambda: context.remove_class("danger"))
        self.status.push(self.status_id, f"STATUS: {message} | {datetime.now().strftime('%H:%M:%S')}")

    def load_or_create_key(self):
        """Load or create a cryptographic key."""
        key_dir = os.path.expanduser("~/.tizelx")
        os.makedirs(key_dir, mode=0o700, exist_ok=True)
        key_path = os.path.join(key_dir, "tizelx.key")

        if os.path.exists(key_path):
            with open(key_path, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_path, "wb") as f:
                f.write(key)
            os.chmod(key_path, 0o600)
            return key

    def detect_terminal(self):
        """Detect the current terminal emulator."""
        try:
            term = os.environ.get('TERM_PROGRAM', '')
            if not term:
                term = subprocess.check_output(["ps", "-p", str(os.getppid()), "-o", "comm="]).decode().strip()
            return term.split('/')[-1] if '/' in term else term
        except Exception as e:
            logging.error(f"Error detecting terminal: {e}")
            return "unknown-terminal"

if __name__ == "__main__":
    app = CyberTerminal()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()