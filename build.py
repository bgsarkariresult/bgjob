import json
import os
import re

# Ensure required directories exist
os.makedirs("jobs", exist_ok=True)

# 1. Load jobs safely
jobs_data = []
json_path = "data/jobs.json"

if os.path.exists(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            jobs_data = json.load(f)
        print(f"📖 Loaded {len(jobs_data)} jobs from {json_path}")
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")
        jobs_data = []
else:
    print(f"⚠️ {json_path} not found!")

# 2. HTML Template for Single Job Page
JOB_TEMPLATE = """<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - BGJob</title>
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
        <p><a href="../index.html">← Back to Home</a></p>
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

# 3. HTML Template for Homepage (index.html)
INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BGJob - Latest Government Jobs 2026</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; background: #f4f6f9; color: #333; }}
        .header {{ background: #0073e6; color: #fff; padding: 20px; text-align: center; }}
        .container {{ max-width: 900px; margin: 20px auto; padding: 0 15px; }}
        .job-card {{ background: #fff; padding: 18px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
        .job-card h2 {{ margin: 0 0 10px 0; font-size: 18px; }}
        .job-card a {{ color: #0073e6; text-decoration: none; font-weight: bold; }}
        .job-card a:hover {{ text-decoration: underline; }}
        .job-meta {{ font-size: 14px; color: #666; margin: 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>BGGovtJobs - Latest Jobs & Notification Portal</h1>
    </div>
    <div class="container">
        <h2>Latest Recruitment Notifications 2026</h2>
        {job_cards}
    </div>
</body>
</html>
"""

# 4. Generate Job Detail Pages
job_cards_html = ""

for job in jobs_data:
    title = job.get("title", "Government Job Alert 2026")
    slug = job.get("slug") or re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    vacancies = job.get("vacancies", "Various")
    last_date = job.get("last_date", "Check Portal")
    
    # Generate HTML Page for Job
    html_out = JOB_TEMPLATE.format(
        title=title,
        vacancies=vacancies,
        qualification=job.get("qualification", "Check Official Notice"),
        age_limit=job.get("age_limit", "18-35 Years"),
        last_date=last_date,
        content_html=job.get("content_html", "<p>Check details above.</p>"),
        apply_url=job.get("apply_url", "#"),
        pdf_url=job.get("pdf_url", "#")
    )
    
    file_name = f"jobs/{slug}.html"
    with open(file_name, "w", encoding="utf-8") as out_file:
        out_file.write(html_out)
    
    # Prepare Homepage Card
    job_cards_html += f"""
    <div class="job-card">
        <h2><a href="jobs/{slug}.html">{title}</a></h2>
        <p class="job-meta">Total Vacancies: {vacancies} | Last Date: {last_date}</p>
    </div>
    """

# 5. Generate Homepage (index.html)
if not job_cards_html:
    job_cards_html = "<p>No jobs added yet.</p>"

with open("index.html", "w", encoding="utf-8") as index_file:
    index_file.write(INDEX_TEMPLATE.format(job_cards=job_cards_html))

print("🚀 Successfully generated all job pages and index.html!")
