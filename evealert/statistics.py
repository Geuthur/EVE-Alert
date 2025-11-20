"""EVE Alert Statistics and History Tracking.

This module provides statistics tracking for alarm events including:
- Total alarm counts per type
- Session-based alarm counts
- Recent alarm history with timestamps
- Session start time tracking
"""

import time
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict


@dataclass
class AlarmEvent:
    """Represents a single alarm event.

    Attributes:
        alarm_type: Type of alarm ('Enemy' or 'Faction')
        timestamp: Unix timestamp when alarm occurred
    """

    alarm_type: str
    timestamp: float

    def formatted_time(self) -> str:
        """Get formatted timestamp string.

        Returns:
            Human-readable timestamp in format 'YYYY-MM-DD HH:MM:SS'
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))


@dataclass
class AlarmStatistics:
    """Track alarm statistics and history.

    Provides counters for total and session alarms, plus a history
    of recent alarm events with timestamps.

    Attributes:
        total_alarms: Total alarms since installation (persists across sessions)
        session_alarms: Alarms in current session (resets on restart)
        alarm_history: Recent alarm events (max 50 entries)
        session_start_time: Unix timestamp when current session started
        total_by_type: Total alarm count per alarm type
        session_by_type: Session alarm count per alarm type
    """

    total_alarms: int = 0
    session_alarms: int = 0
    alarm_history: Deque[AlarmEvent] = field(default_factory=lambda: deque(maxlen=50))
    session_start_time: float = field(default_factory=time.time)
    total_by_type: Dict[str, int] = field(
        default_factory=lambda: {"Enemy": 0, "Faction": 0}
    )
    session_by_type: Dict[str, int] = field(
        default_factory=lambda: {"Enemy": 0, "Faction": 0}
    )

    def add_alarm(self, alarm_type: str) -> None:
        """Record a new alarm event.

        Args:
            alarm_type: Type of alarm ('Enemy' or 'Faction')
        """
        timestamp = time.time()

        # Increment counters
        self.total_alarms += 1
        self.session_alarms += 1

        # Increment type-specific counters
        if alarm_type in self.total_by_type:
            self.total_by_type[alarm_type] += 1
        if alarm_type in self.session_by_type:
            self.session_by_type[alarm_type] += 1

        # Add to history
        self.alarm_history.append(AlarmEvent(alarm_type, timestamp))

    def get_recent_history(self, count: int = 10) -> list[AlarmEvent]:
        """Get most recent alarm events.

        Args:
            count: Number of recent events to return (default 10)

        Returns:
            List of recent AlarmEvent objects, newest first
        """
        history_list = list(self.alarm_history)
        return history_list[-count:][::-1]  # Return last N items, reversed

    def get_session_duration(self) -> str:
        """Get formatted session duration.

        Returns:
            Human-readable session duration string (e.g., '2h 15m 30s')
        """
        duration = time.time() - self.session_start_time
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        if minutes > 0:
            return f"{minutes}m {seconds}s"
        return f"{seconds}s"

    def reset_session(self) -> None:
        """Reset session statistics.

        Resets session counters and start time, but preserves total statistics.
        """
        self.session_alarms = 0
        self.session_by_type = {"Enemy": 0, "Faction": 0}
        self.session_start_time = time.time()

    def clear_history(self) -> None:
        """Clear alarm history.

        Removes all historical alarm events but preserves counters.
        """
        self.alarm_history.clear()

    def to_dict(self) -> dict:
        """Convert statistics to dictionary format.

        Returns:
            Dictionary containing all statistics data
        """
        return {
            "total_alarms": self.total_alarms,
            "session_alarms": self.session_alarms,
            "session_duration": self.get_session_duration(),
            "total_by_type": self.total_by_type.copy(),
            "session_by_type": self.session_by_type.copy(),
            "recent_history": [
                {"type": event.alarm_type, "time": event.formatted_time()}
                for event in self.get_recent_history(10)
            ],
        }
