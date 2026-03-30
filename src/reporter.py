import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import Database

class Reporter:
    def __init__(self, template_dir="templates"):
        self.db = Database()
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template('report_template.html')

    def generate_pdf(self, lead):
        # Data preparation
        data = {
            "business_name": lead['name'],
            "audit_score": lead['audit_score'],
            "rating": lead['rating'],
            "reviews": lead['reviews'],
            "details": lead['status'] if lead['status'] != 'audited' else "Optimización SEO; Seguridad Web; Visibilidad Google Maps; Rendimiento Móvil", # Default fallback
            "fail_count": 3 if lead['audit_score'] < 70 else 1
        }
        
        # Render HTML
        html_content = self.template.render(data)
        
        # Output Path
        report_dir = "data/reports"
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
            
        report_filename = f"{lead['name'].replace(' ', '_')}_Audit.pdf"
        report_path = os.path.join(report_dir, report_filename)
        
        # Save PDF
        HTML(string=html_content).write_pdf(report_path)
        print(f"[+] Report Generated: {report_path}")
        return report_path

    def run_all(self):
        # Get audited leads that don't have reports yet
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM leads WHERE status = 'audited' AND report_path IS NULL")
        leads = cursor.fetchall()
        
        for lead in leads:
            path = self.generate_pdf(dict(lead))
            self.db.update_lead(lead['id'], report_path=path, status='reported')
        conn.close()

if __name__ == "__main__":
    reporter = Reporter()
    reporter.run_all()
