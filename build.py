import json
import os
import re

# Ensure required directories exist
os.makedirs("jobs", exist_ok=True)

# 1. Load jobs from JSON
jobs_data = []
json_path = "data/jobs.json"

if os.path.exists(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            jobs_data = json.load(f)
        print(f"📖 Loaded {len(jobs_data)} jobs from {json_path}")
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")
else:
    print(f"⚠️ {json_path} not found!")

# 2. Built-in HTML Template (No external template.html needed)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - BGJob</title>
    <link rel="stylesheet" href="../assets/css/style.css">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; background: #f4f6f9; color: #333; }}
        .container {{ max-width: 900px; margin: 20px auto; background: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #0073e6; font-size: 24px; }}
        .info-box {{ background: #e8f4fd; padding: 15px; border-left: 4px solid #0073e6; margin-bottom: 20px; border-radius: 4px; }}
        .btn {{ display: inline-block; padding: 12px 24px; color: #fff; text-decoration: none; font-weight: bold; border-radius: 5px; margin: 5px; }}
        .btn-apply {{ background-color: #28a745; }}
        .btn-pdf {{ background-color: #0073e6; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="info-box">
            <p><strong>Total Vacancies:</strong> {vacancies}</p>
            <p><strong>Qualification:</strong> {qualification}</p>
            <p><strong>Age Limit:</strong> {age_limit}</p>
            <p><strong>Last Date:</strong> {last_date}</p>
        </div>
        <hr>
        <div class="job-content">
            {content_html}
        </div>
        <hr>
        <div style="text-align:center; margin-top: 25px;">
            <a href="{pdf_url}" target="_blank" class="btn btn-pdf">📄 Download Official PDF</a>
            <a href="{apply_url}" target="_blank" class="btn btn-apply">🔗 Apply Online Direct Link</a>
        </div>
    </div>
</body>
</html>
"""

# 3. Generate HTML pages for each job
for job in jobs_data:
    title = job.get("title", "Government Job Alert 2026")
    slug = job.get("slug") or re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    
    html_out = HTML_TEMPLATE.format(
        title=title,
        vacancies=job.get("vacancies", "Various"),
        qualification=job.get("qualification", "Check Official Notice"),
        age_limit=job.get("age_limit", "18-35 Years"),
        last_date=job.get("last_date", "Check Portal"),
        content_html=job.get("content_html", "<p>Check details above.</p>"),
        apply_url=job.get("apply_url", "#"),
        pdf_url=job.get("pdf_url", "#")
    )
    
    file_name = f"jobs/{slug}.html"
    with open(file_name, "w", encoding="utf-8") as out_file:
        out_file.write(html_out)
    print(f"✅ Generated: {file_name}")

print("🚀 All HTML pages built successfully!")
