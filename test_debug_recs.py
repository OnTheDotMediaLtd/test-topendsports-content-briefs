import sys
sys.path.insert(0, "scripts")
from prompt_monitor import PromptMonitor, UsageEntry
from datetime import datetime, timedelta

monitor = PromptMonitor.__new__(PromptMonitor)
monitor.entries = []
monitor.config = {
    "category_failure_threshold": 5,
    "session_timeout_minutes": 30,
    "min_entries_for_analysis": 3,
    "trend_window_days": 14,
    "max_entries": 10000,
}

now = datetime.now()
for i in range(15):
    e = UsageEntry(command="validate-phase", status="failure", error_message="test error")
    e.timestamp = (now - timedelta(hours=i)).isoformat()
    e.category = "validation"
    monitor.entries.append(e)
for i in range(3):
    e = UsageEntry(command="validate-phase", status="success")
    e.timestamp = (now - timedelta(hours=i)).isoformat()
    e.category = "validation"
    monitor.entries.append(e)

trends = monitor.get_trends(30)
print("problematic:", trends["problematic"])
recs = monitor.get_recommendations()
print("recommendations count:", len(recs))
for r in recs:
    print(r)
