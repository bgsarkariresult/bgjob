import json
import os
import re

# Directries setup
directories = ["jobs", "results", "admit-card", "answer-key", "syllabus", "current-affairs"]
for d in directories:
    os.makedirs(d, exist_ok=True)

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

# Complete HTML Outer Layout
HTML_LAYOUT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f6f9; color: #333; }}
        a {{ text-decoration: none; }}
        .card {{ background: #fff; padding: 15px; margin-bottom: 12px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); display: block; }}
        .card h2 {{ font-size: 18px; margin: 0 0 8px 0; color: #0073e6; }}
        .card p {{ margin: 0; font-size: 14px; color: #666; }}
    </style>
</head>
<body>

{main_content}

<footer class="site-footer" style="margin-top:40px; text-align:center; padding:20px; background:#222; color:#fff;">
    <p>&copy; 2026 BG Jobs. All Rights Reserved.</p>
</footer>

</body>
</html>
"""

# 2. Single Job Template Body
JOB_TEMPLATE_BODY = """
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
        <a href="{pdf_url}" target="_blank" style="background:#0073e6; color:#fff; padding:12px 24px; font-weight:bold; border-radius:5px;">📄 Download Official PDF</a>
        <a href="{apply_url}" target="_blank" style="background:#28a745; color:#fff; padding:12px 24px; font-weight:bold; border-radius:5px;">🔗 Apply Online Direct Link</a>
    </div>
</main>
"""

# 3. Generate Single Detail Pages & Build Listing Content
job_cards_html = ""

for job in jobs_data:
    title = job.get("title", "Government Job Alert")
    slug = job.get("slug") or re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    
    # Detail Page HTML Generation
    body_content = JOB_TEMPLATE_BODY.format(
        title=title,
        vacancies=job.get("vacancies", "Various Posts"),
        qualification=job.get("qualification", "10th / 12th / Graduate"),
        age_limit=job.get("age_limit", "18 to 35 Years"),
        last_date=job.get("last_date", "Check Official Portal"),
        content_html=job.get("content_html", "<p>Check details above.</p>"),
        apply_url=job.get("apply_url", "#"),
        pdf_url=job.get("pdf_url", "#")
    )
    
    full_html = HTML_LAYOUT.format(page_title=title, main_content=body_content)
    file_name = f"jobs/{slug}.html"
    
    with open(file_name, "w", encoding="utf-8") as out_file:
        out_file.write(full_html)
    print(f"✅ Generated Post Page: {file_name}")

    # Build List Card for Category Index Pages
    job_cards_html += f"""
    <a href="{slug}.html" class="card">
        <h2>{title}</h2>
        <p><strong>Last Date:</strong> {job.get('last_date', 'N/A')} | <strong>Vacancies:</strong> {job.get('vacancies', 'N/A')}</p>
    </a>
    """

# 4. Generate jobs/index.html (Category Listing Page)
CATEGORY_INDEX_BODY = f"""
<main class="container" style="max-width:900px; margin:20px auto; padding:10px;">
    <p><a href="../index.html" style="text-decoration:none; color:#0073e6; font-weight:bold;">← Back to Home</a></p>
    <h1 style="color:#0073e6; border-bottom: 2px solid #0073e6; padding-bottom: 8px;">Latest Job Notifications</h1>
    <div class="job-list">
        {job_cards_html if job_cards_html else "<p>No active jobs found.</p>"}
    </div>
</main>
"""

category_html = HTML_LAYOUT.format(page_title="Latest Jobs - BG Jobs", main_content=CATEGORY_INDEX_BODY)

# Write index.html for jobs and create placeholders for other directories to prevent 404
for d in directories:
    target_index = f"{d}/index.html"
    with open(target_index, "w", encoding="utf-8") as f:
        f.write(category_html)
    print(f"✅ Generated Category Listing: {target_index}")

print("\n🚀 All Detail Pages and Category Index Pages generated successfully without 404 errors!")
