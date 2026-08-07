import json
import os
import re

os.makedirs("jobs", exist_ok=True)

# 1. Load jobs data
jobs_data = []
json_path = "data/jobs.json"

if os.path.exists(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            jobs_data = json.load(f)
        print(f"📖 Loaded {len(jobs_data)} jobs successfully")
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")

# 2. Single Post Template
JOB_TEMPLATE = """<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | BG Jobs</title>
    <link rel="stylesheet" href="../assets/css/style.css">
    <link rel="shortcut icon" href="../favicon.ico" type="image/x-icon">
</head>
<body>
    <header class="site-header">
        <div class="container header-flex">
            <a href="../index.html" class="logo">BG <span>Jobs</span></a>
        </div>
    </header>

    <main class="container" style="max-width:900px; margin:20px auto; background:#fff; padding:25px; border-radius:8px; box-shadow:0 2px 10px rgba(0,0,0,0.1);">
        <p><a href="../index.html" style="text-decoration:none; color:#0073e6; font-weight:bold;">← Back to Home</a></p>
        <h1 style="color:#0073e6; font-size:24px; margin-top:10px;">{title}</h1>
        
        <div style="background:#e8f4fd; padding:15px; border-left:4px solid #0b7a2f; margin-bottom:20px; border-radius:4px;">
            <p><strong>Total Vacancies:</strong> {vacancies}</p>
            <p><strong>Qualification:</strong> {qualification}</p>
            <p><strong>Age Limit:</strong> {age_limit}</p>
            <p><strong>Last Date:</strong> {last_date}</p>
        </div>

        <div class="job-content">
            {content_html}
        </div>

        <div style="text-align:center; margin-top:25px; display:flex; gap:10px; justify-content:center;">
            <a href="{pdf_url}" target="_blank" style="background:#0073e6; color:#fff; padding:12px 24px; text-decoration:none; font-weight:bold; border-radius:5px;">📄 Download Official PDF</a>
            <a href="{apply_url}" target="_blank" style="background:#28a745; color:#fff; padding:12px 24px; text-decoration:none; font-weight:bold; border-radius:5px;">🔗 Apply Online Direct Link</a>
        </div>
    </main>

    <footer class="site-footer" style="margin-top:40px; text-align:center; padding:20px; background:#222; color:#fff;">
        <p>&copy; 2026 BG Jobs. All Rights Reserved.</p>
    </footer>
</body>
</html>
"""

# 3. Generate Job Post Pages
for job in jobs_data:
    title = job.get("title", "Government Job Alert")
    slug = job.get("slug") or re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    
    html_out = JOB_TEMPLATE.format(
        title=title,
        vacancies=job.get("vacancies", "Various Posts"),
        qualification=job.get("qualification", "10th / 12th / Graduate"),
        age_limit=job.get("age_limit", "18 to 35 Years"),
        last_date=job.get("last_date", "Check Official Portal"),
        content_html=job.get("content_html", "<p>Check details above.</p>"),
        apply_url=job.get("apply_url", "#"),
        pdf_url=job.get("pdf_url", "#")
    )
    
    file_name = f"jobs/{slug}.html"
    with open(file_name, "w", encoding="utf-8") as out_file:
        out_file.write(html_out)
    print(f"✅ Generated File: {file_name}")

print("🚀 All job files generated in /jobs/ directory!")
