"""Statistics window for EVE Alert System.

Displays alarm statistics including:
- Total and session alarm counts
- Alarm type breakdown
- Recent alarm history
- Session duration
"""

import csv
import json
from tkinter import filedialog

import customtkinter

from evealert.constants import STATUS_CHECK_INTERVAL


class StatisticsWindow(customtkinter.CTkToplevel):
    """Statistics display window.
    
    Shows real-time statistics about alarm events including
    total counts, session counts, recent history, and session duration.
    
    Attributes:
        main: Reference to MainMenu instance
        is_open: Whether window is currently open
    """

    def __init__(self, main) -> None:
        """Initialize statistics window.
        
        Args:
            main: Reference to MainMenu instance
        """
        super().__init__(main)
        self.main = main
        self.is_open = True
        
        self.title("EVE Alert - Statistics")
        self.geometry("500x550")
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        
        self.init_widgets()
        self.update_statistics()

    def init_widgets(self) -> None:
        """Initialize all GUI widgets."""
        # Main container with padding
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = customtkinter.CTkLabel(
            self.main_frame,
            text="Alarm Statistics",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Session Info Frame
        self.session_frame = customtkinter.CTkFrame(self.main_frame)
        self.session_frame.pack(fill="x", pady=(0, 15))
        
        session_title = customtkinter.CTkLabel(
            self.session_frame,
            text="Session Info",
            font=customtkinter.CTkFont(size=16, weight="bold")
        )
        session_title.pack(pady=10)
        
        self.session_duration_label = customtkinter.CTkLabel(
            self.session_frame,
            text="Duration: 0s",
            font=customtkinter.CTkFont(size=14)
        )
        self.session_duration_label.pack(pady=5)
        
        # Totals Frame
        self.totals_frame = customtkinter.CTkFrame(self.main_frame)
        self.totals_frame.pack(fill="x", pady=(0, 15))
        
        totals_title = customtkinter.CTkLabel(
            self.totals_frame,
            text="Total Alarms",
            font=customtkinter.CTkFont(size=16, weight="bold")
        )
        totals_title.pack(pady=10)
        
        self.total_alarms_label = customtkinter.CTkLabel(
            self.totals_frame,
            text="Total: 0",
            font=customtkinter.CTkFont(size=14)
        )
        self.total_alarms_label.pack(pady=5)
        
        self.total_enemy_label = customtkinter.CTkLabel(
            self.totals_frame,
            text="Enemy: 0",
            font=customtkinter.CTkFont(size=14)
        )
        self.total_enemy_label.pack(pady=5)
        
        self.total_faction_label = customtkinter.CTkLabel(
            self.totals_frame,
            text="Faction: 0",
            font=customtkinter.CTkFont(size=14)
        )
        self.total_faction_label.pack(pady=5)
        
        # Session Stats Frame
        self.session_stats_frame = customtkinter.CTkFrame(self.main_frame)
        self.session_stats_frame.pack(fill="x", pady=(0, 15))
        
        session_stats_title = customtkinter.CTkLabel(
            self.session_stats_frame,
            text="Current Session",
            font=customtkinter.CTkFont(size=16, weight="bold")
        )
        session_stats_title.pack(pady=10)
        
        self.session_alarms_label = customtkinter.CTkLabel(
            self.session_stats_frame,
            text="Total: 0",
            font=customtkinter.CTkFont(size=14)
        )
        self.session_alarms_label.pack(pady=5)
        
        self.session_enemy_label = customtkinter.CTkLabel(
            self.session_stats_frame,
            text="Enemy: 0",
            font=customtkinter.CTkFont(size=14)
        )
        self.session_enemy_label.pack(pady=5)
        
        self.session_faction_label = customtkinter.CTkLabel(
            self.session_stats_frame,
            text="Faction: 0",
            font=customtkinter.CTkFont(size=14)
        )
        self.session_faction_label.pack(pady=5)
        
        # Recent History Frame
        self.history_frame = customtkinter.CTkFrame(self.main_frame)
        self.history_frame.pack(fill="both", expand=True)
        
        history_title = customtkinter.CTkLabel(
            self.history_frame,
            text="Recent History (Last 10)",
            font=customtkinter.CTkFont(size=16, weight="bold")
        )
        history_title.pack(pady=10)
        
        self.history_textbox = customtkinter.CTkTextbox(
            self.history_frame,
            height=150,
            width=400
        )
        self.history_textbox.pack(pady=(0, 10), padx=10)
        
        # Buttons Frame
        self.buttons_frame = customtkinter.CTkFrame(self.main_frame)
        self.buttons_frame.pack(fill="x", pady=(10, 0))
        
        self.reset_session_button = customtkinter.CTkButton(
            self.buttons_frame,
            text="Reset Session",
            command=self.reset_session,
            width=120
        )
        self.reset_session_button.pack(side="left", padx=5)
        
        self.clear_history_button = customtkinter.CTkButton(
            self.buttons_frame,
            text="Clear History",
            command=self.clear_history,
            width=120
        )
        self.clear_history_button.pack(side="left", padx=5)
        
        self.export_button = customtkinter.CTkButton(
            self.buttons_frame,
            text="Export History",
            command=self.export_history,
            width=120
        )
        self.export_button.pack(side="left", padx=5)

    def update_statistics(self) -> None:
        """Update all statistics displays with current data."""
        if not self.is_open:
            return
        
        stats = self.main.alert.get_statistics()
        
        # Update session duration
        self.session_duration_label.configure(
            text=f"Duration: {stats.get_session_duration()}"
        )
        
        # Update total statistics
        self.total_alarms_label.configure(
            text=f"Total: {stats.total_alarms}"
        )
        self.total_enemy_label.configure(
            text=f"Enemy: {stats.total_by_type['Enemy']}"
        )
        self.total_faction_label.configure(
            text=f"Faction: {stats.total_by_type['Faction']}"
        )
        
        # Update session statistics
        self.session_alarms_label.configure(
            text=f"Total: {stats.session_alarms}"
        )
        self.session_enemy_label.configure(
            text=f"Enemy: {stats.session_by_type['Enemy']}"
        )
        self.session_faction_label.configure(
            text=f"Faction: {stats.session_by_type['Faction']}"
        )
        
        # Update history
        self.history_textbox.delete("1.0", "end")
        recent = stats.get_recent_history(10)
        if recent:
            for event in recent:
                self.history_textbox.insert(
                    "end",
                    f"[{event.formatted_time()}] {event.alarm_type}\n"
                )
        else:
            self.history_textbox.insert("end", "No alarms yet in this session.")
        
        # Schedule next update
        self.after(STATUS_CHECK_INTERVAL, self.update_statistics)

    def reset_session(self) -> None:
        """Reset session statistics."""
        stats = self.main.alert.get_statistics()
        stats.reset_session()
        self.main.write_message("Statistics: Session reset.", "green")
        self.update_statistics()

    def clear_history(self) -> None:
        """Clear alarm history."""
        stats = self.main.alert.get_statistics()
        stats.clear_history()
        self.main.write_message("Statistics: History cleared.", "green")
        self.update_statistics()

    def export_history(self) -> None:
        """Export alarm history to CSV or JSON file."""
        stats = self.main.alert.get_statistics()
        
        if len(stats.alarm_history) == 0:
            self.main.write_message("Statistics: No history to export.", "yellow")
            return
        
        # Ask user for file format and location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV files", "*.csv"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ],
            title="Export Alarm History"
        )
        
        if not file_path:
            return  # User cancelled
        
        try:
            if file_path.endswith('.json'):
                self._export_json(file_path, stats)
            else:
                self._export_csv(file_path, stats)
            
            self.main.write_message(f"Statistics: History exported to {file_path}", "green")
        except Exception as e:
            self.main.write_message(f"Statistics: Export failed. {str(e)}", "red")

    def _export_csv(self, file_path: str, stats) -> None:
        """Export history to CSV file."""
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(['Timestamp', 'Alarm Type'])
            # Write data
            for event in stats.alarm_history:
                writer.writerow([event.formatted_time(), event.alarm_type])

    def _export_json(self, file_path: str, stats) -> None:
        """Export history to JSON file."""
        data = {
            'export_info': {
                'total_alarms': stats.total_alarms,
                'session_alarms': stats.session_alarms,
                'session_duration': stats.get_session_duration(),
                'total_by_type': stats.total_by_type,
                'session_by_type': stats.session_by_type
            },
            'history': [
                {
                    'timestamp': event.formatted_time(),
                    'alarm_type': event.alarm_type
                }
                for event in stats.alarm_history
            ]
        }
        
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2)

    def close_window(self) -> None:
        """Close the statistics window."""
        self.is_open = False
        self.destroy()
