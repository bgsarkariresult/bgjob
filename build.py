import json
import os
import re

os.makedirs("jobs", exist_ok=True)

# 1. Load jobs safely
jobs_data = []
json_path = "data/jobs.json"

if os.path.exists(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            jobs_data = json.load(f)
        print(f"📖 Loaded {len(jobs_data)} jobs")
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")

# 2. Single Job Post Page Template
JOB_TEMPLATE = """<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | BG Jobs</title>
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
    <header class="site-header">
        <div class="container header-flex">
            <a href="../index.html" class="logo">BG <span>Jobs</span></a>
        </div>
    </header>
    <main class="container" style="max-width:900px; margin:20px auto; background:#fff; padding:20px; border-radius:8px;">
        <p><a href="../index.html">← Back to Home</a></p>
        <h1>{title}</h1>
        <div style="background:#e8f4fd; padding:15px; border-left:4px solid #0b7a2f; margin-bottom:20px;">
            <p><strong>Total Vacancies:</strong> {vacancies}</p>
            <p><strong>Qualification:</strong> {qualification}</p>
            <p><strong>Age Limit:</strong> {age_limit}</p>
            <p><strong>Last Date:</strong> {last_date}</p>
        </div>
        <div>{content_html}</div>
        <div style="text-align:center; margin-top:25px;">
            <a href="{pdf_url}" target="_blank" style="padding:10px 20px; background:#0073e6; color:#fff; text-decoration:none; border-radius:5px;">📄 Download PDF</a>
            <a href="{apply_url}" target="_blank" style="padding:10px 20px; background:#28a745; color:#fff; text-decoration:none; border-radius:5px; margin-left:10px;">🔗 Apply Online</a>
        </div>
    </main>
</body>
</html>
"""

# 3. Dynamic Homepage Link Builder
job_list_html = ""

for job in jobs_data:
    title = job.get("title", "Government Job Alert")
    slug = job.get("slug") or re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    vacancies = job.get("vacancies", "Various")
    last_date = job.get("last_date", "Check Portal")
    
    # Generate Post Page
    html_out = JOB_TEMPLATE.format(
        title=title,
        vacancies=vacancies,
        qualification=job.get("qualification", "Check Notice"),
        age_limit=job.get("age_limit", "18-35 Years"),
        last_date=last_date,
        content_html=job.get("content_html", "<p>Check details above.</p>"),
        apply_url=job.get("apply_url", "#"),
        pdf_url=job.get("pdf_url", "#")
    )
    
    file_name = f"jobs/{slug}.html"
    with open(file_name, "w", encoding="utf-8") as out_file:
        out_file.write(html_out)
    
    # Build list item for Index
    job_list_html += f'<li><a href="jobs/{slug}.html">{title} <span class="badge new">New</span></a></li>\n'

print("🚀 Posts generated! Update index.html links with your slugs in data/jobs.json")
