#!/bin/bash
# Sample hook script that triggers on critical alerts
# Receives alert data via stdin as JSON

# Read JSON data
alert_data=$(cat)

# Extract alert details
category=$(echo "$alert_data" | python3 -c "import sys, json; print(json.load(sys.stdin).get('category', 'unknown'))")
message=$(echo "$alert_data" | python3 -c "import sys, json; print(json.load(sys.stdin).get('message', 'No message'))")

# Log to a file (in production, could send email, Slack notification, etc.)
echo "[$(date)] CRITICAL ALERT: [$category] $message" >> logs/prompts/critical_alerts.log

# Exit with 0 for success
exit 0
