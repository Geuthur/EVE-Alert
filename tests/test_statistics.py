"""Unit tests for EVE Alert statistics module."""

import csv
import json
import os
import tempfile
import time
import unittest

from evealert.statistics import AlarmEvent, AlarmStatistics


class TestAlarmEvent(unittest.TestCase):
    """Test cases for AlarmEvent class."""

    def test_alarm_event_creation(self):
        """Test AlarmEvent initialization."""
        timestamp = time.time()
        event = AlarmEvent("Enemy", timestamp)
        
        self.assertEqual(event.alarm_type, "Enemy")
        self.assertEqual(event.timestamp, timestamp)

    def test_formatted_time(self):
        """Test formatted_time method."""
        timestamp = 1700000000.0  # Fixed timestamp for testing
        event = AlarmEvent("Faction", timestamp)
        
        formatted = event.formatted_time()
        self.assertIsInstance(formatted, str)
        self.assertIn("-", formatted)  # Contains date separator
        self.assertIn(":", formatted)  # Contains time separator


class TestAlarmStatistics(unittest.TestCase):
    """Test cases for AlarmStatistics class."""

    def setUp(self):
        """Set up test statistics instance."""
        self.stats = AlarmStatistics()

    def test_initial_state(self):
        """Test initial statistics state."""
        self.assertEqual(self.stats.total_alarms, 0)
        self.assertEqual(self.stats.session_alarms, 0)
        self.assertEqual(len(self.stats.alarm_history), 0)
        self.assertEqual(self.stats.total_by_type['Enemy'], 0)
        self.assertEqual(self.stats.total_by_type['Faction'], 0)
        self.assertEqual(self.stats.session_by_type['Enemy'], 0)
        self.assertEqual(self.stats.session_by_type['Faction'], 0)

    def test_add_alarm_enemy(self):
        """Test adding Enemy alarm."""
        self.stats.add_alarm('Enemy')
        
        self.assertEqual(self.stats.total_alarms, 1)
        self.assertEqual(self.stats.session_alarms, 1)
        self.assertEqual(self.stats.total_by_type['Enemy'], 1)
        self.assertEqual(self.stats.session_by_type['Enemy'], 1)
        self.assertEqual(self.stats.total_by_type['Faction'], 0)
        self.assertEqual(len(self.stats.alarm_history), 1)

    def test_add_alarm_faction(self):
        """Test adding Faction alarm."""
        self.stats.add_alarm('Faction')
        
        self.assertEqual(self.stats.total_alarms, 1)
        self.assertEqual(self.stats.session_alarms, 1)
        self.assertEqual(self.stats.total_by_type['Faction'], 1)
        self.assertEqual(self.stats.session_by_type['Faction'], 1)
        self.assertEqual(self.stats.total_by_type['Enemy'], 0)
        self.assertEqual(len(self.stats.alarm_history), 1)

    def test_add_multiple_alarms(self):
        """Test adding multiple alarms."""
        self.stats.add_alarm('Enemy')
        self.stats.add_alarm('Enemy')
        self.stats.add_alarm('Faction')
        
        self.assertEqual(self.stats.total_alarms, 3)
        self.assertEqual(self.stats.session_alarms, 3)
        self.assertEqual(self.stats.total_by_type['Enemy'], 2)
        self.assertEqual(self.stats.total_by_type['Faction'], 1)
        self.assertEqual(len(self.stats.alarm_history), 3)

    def test_get_recent_history(self):
        """Test get_recent_history method."""
        # Add some alarms
        for i in range(15):
            alarm_type = 'Enemy' if i % 2 == 0 else 'Faction'
            self.stats.add_alarm(alarm_type)
        
        # Get last 10
        recent = self.stats.get_recent_history(10)
        self.assertEqual(len(recent), 10)
        
        # Check order (newest first)
        self.assertIsInstance(recent[0], AlarmEvent)

    def test_get_recent_history_less_than_count(self):
        """Test get_recent_history when fewer alarms than requested."""
        self.stats.add_alarm('Enemy')
        self.stats.add_alarm('Faction')
        
        recent = self.stats.get_recent_history(10)
        self.assertEqual(len(recent), 2)

    def test_history_maxlen(self):
        """Test that history respects maxlen of 50."""
        for i in range(60):
            self.stats.add_alarm('Enemy')
        
        self.assertEqual(len(self.stats.alarm_history), 50)
        self.assertEqual(self.stats.total_alarms, 60)

    def test_session_duration(self):
        """Test get_session_duration method."""
        duration = self.stats.get_session_duration()
        self.assertIsInstance(duration, str)
        self.assertTrue('s' in duration)  # Contains seconds indicator

    def test_reset_session(self):
        """Test reset_session method."""
        # Add some alarms
        self.stats.add_alarm('Enemy')
        self.stats.add_alarm('Faction')
        self.stats.add_alarm('Enemy')
        
        initial_total = self.stats.total_alarms
        initial_total_enemy = self.stats.total_by_type['Enemy']
        
        # Reset session
        self.stats.reset_session()
        
        # Check session stats are reset
        self.assertEqual(self.stats.session_alarms, 0)
        self.assertEqual(self.stats.session_by_type['Enemy'], 0)
        self.assertEqual(self.stats.session_by_type['Faction'], 0)
        
        # Check total stats are preserved
        self.assertEqual(self.stats.total_alarms, initial_total)
        self.assertEqual(self.stats.total_by_type['Enemy'], initial_total_enemy)

    def test_clear_history(self):
        """Test clear_history method."""
        self.stats.add_alarm('Enemy')
        self.stats.add_alarm('Faction')
        
        self.assertEqual(len(self.stats.alarm_history), 2)
        
        self.stats.clear_history()
        
        self.assertEqual(len(self.stats.alarm_history), 0)
        # Counters should be preserved
        self.assertEqual(self.stats.total_alarms, 2)
        self.assertEqual(self.stats.session_alarms, 2)

    def test_to_dict(self):
        """Test to_dict method."""
        self.stats.add_alarm('Enemy')
        self.stats.add_alarm('Faction')
        
        data = self.stats.to_dict()
        
        self.assertIsInstance(data, dict)
        self.assertIn('total_alarms', data)
        self.assertIn('session_alarms', data)
        self.assertIn('session_duration', data)
        self.assertIn('total_by_type', data)
        self.assertIn('session_by_type', data)
        self.assertIn('recent_history', data)
        
        self.assertEqual(data['total_alarms'], 2)
        self.assertEqual(data['session_alarms'], 2)
        self.assertIsInstance(data['recent_history'], list)
        self.assertEqual(len(data['recent_history']), 2)

    def test_to_dict_recent_history_format(self):
        """Test to_dict recent_history format."""
        self.stats.add_alarm('Enemy')
        
        data = self.stats.to_dict()
        history = data['recent_history']
        
        self.assertEqual(len(history), 1)
        self.assertIn('type', history[0])
        self.assertIn('time', history[0])
        self.assertEqual(history[0]['type'], 'Enemy')


class TestHistoryExport(unittest.TestCase):
    """Test cases for history export functionality."""

    def setUp(self):
        """Set up test statistics with sample data."""
        self.stats = AlarmStatistics()
        # Add some sample alarms
        self.stats.add_alarm('Enemy')
        time.sleep(0.01)  # Ensure different timestamps
        self.stats.add_alarm('Faction')
        time.sleep(0.01)
        self.stats.add_alarm('Enemy')

    def test_export_csv_format(self):
        """Test CSV export format."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_file = f.name
        
        try:
            # Write CSV
            with open(temp_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Timestamp', 'Alarm Type'])
                for event in self.stats.alarm_history:
                    writer.writerow([event.formatted_time(), event.alarm_type])
            
            # Verify file exists and has content
            self.assertTrue(os.path.exists(temp_file))
            
            # Read and verify
            with open(temp_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
                
                self.assertEqual(len(rows), 4)  # Header + 3 data rows
                self.assertEqual(rows[0], ['Timestamp', 'Alarm Type'])
                self.assertEqual(rows[1][1], 'Enemy')
                self.assertEqual(rows[2][1], 'Faction')
                self.assertEqual(rows[3][1], 'Enemy')
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_export_json_format(self):
        """Test JSON export format."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Write JSON
            data = {
                'export_info': {
                    'total_alarms': self.stats.total_alarms,
                    'session_alarms': self.stats.session_alarms,
                    'session_duration': self.stats.get_session_duration(),
                    'total_by_type': self.stats.total_by_type,
                    'session_by_type': self.stats.session_by_type
                },
                'history': [
                    {
                        'timestamp': event.formatted_time(),
                        'alarm_type': event.alarm_type
                    }
                    for event in self.stats.alarm_history
                ]
            }
            
            with open(temp_file, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2)
            
            # Verify file exists
            self.assertTrue(os.path.exists(temp_file))
            
            # Read and verify
            with open(temp_file, 'r', encoding='utf-8') as jsonfile:
                loaded_data = json.load(jsonfile)
                
                self.assertIn('export_info', loaded_data)
                self.assertIn('history', loaded_data)
                self.assertEqual(loaded_data['export_info']['total_alarms'], 3)
                self.assertEqual(len(loaded_data['history']), 3)
                self.assertEqual(loaded_data['history'][0]['alarm_type'], 'Enemy')
                self.assertEqual(loaded_data['history'][1]['alarm_type'], 'Faction')
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_export_empty_history(self):
        """Test exporting empty history."""
        empty_stats = AlarmStatistics()
        
        # Should handle empty history gracefully
        self.assertEqual(len(empty_stats.alarm_history), 0)


if __name__ == '__main__':
    unittest.main()
