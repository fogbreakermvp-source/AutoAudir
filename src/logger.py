import os
import time

class AuditLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.log_file = os.path.join(self.log_dir, "audit_history.md")
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", encoding="utf-8") as f:
                f.write("# Elite Audit Team - Global Outreach History\n\n")
                f.write("| Timestamp | Event | Details |\n")
                f.write("| :--- | :--- | :--- |\n")

    def log(self, event, details):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"| {timestamp} | {event} | {details} |\n")

audit_logger = AuditLogger()
