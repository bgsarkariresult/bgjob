import json
import os
import re

directories = ["jobs", "results", "admit-card", "answer-key", "syllabus", "current-affairs"]
for d in directories:
    os.makedirs(d, exist_ok=True)

jobs_data = []
json_path = "data/jobs.json"

if os.path.exists(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            jobs_data = json.load(f)
            print(f"📖 Loaded {len(jobs_data)} jobs successfully")
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")

HTML_LAYOUT = """<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <link rel="stylesheet" href="../assets/css/style.css">
    {schema_script}
</head>
<body>

<header class="site-header">
    <div class="container header-flex">
        <h1 class="logo"><a href="../index.html">BG <span>Jobs</span></a></h1>
    </div>
    <nav class="main-nav">
        <div class="container nav-links">
            <a href="../index.html">Home</a>
            <a href="../jobs/index.html">Latest Jobs</a>
            <a href="../results/index.html">Results</a>
            <a href="../admit-card/index.html">Admit Card</a>
        </div>
    </nav>
</header>

<main class="container" style="margin-top:20px;">
    {main_content}
</main>

<footer class="site-footer">
    <p>&copy; 2026 BG Jobs. All Rights Reserved.</p>
</footer>

</body>
</html>
"""

JOB_TEMPLATE_BODY = """
<div style="background:#fff; padding:25px; border-radius:8px; border: 1px solid #dee2e6;">
    <p><a href="../index.html" style="color:#0073e6; font-weight:bold;">← Home पर वापस जाएं</a></p>
    <h1 style="color:#0073e6; font-size:24px; margin-top:10px;">{title}</h1>
    
    <div style="background:#e8f4fd; padding:15px; border-left:4px solid #0b7a2f; margin:20px 0; border-radius:4px;">
        <p><strong>Total Vacancies:</strong> {vacancies}</p>
        <p><strong>Qualification:</strong> {qualification}</p>
        <p><strong>Age Limit:</strong> {age_limit}</p>
        <p><strong>Last Date:</strong> {last_date}</p>
    </div>

    <div class="job-content">
        {content_html}
    </div>

    <div style="text-align:center; margin-top:25px; display:flex; gap:10px; justify-content:center; flex-wrap:wrap;">
        <a href="{pdf_url}" target="_blank" style="background:#0073e6; color:#fff; padding:12px 24px; font-weight:bold; border-radius:5px;">📄 Download Official PDF</a>
        <a href="{apply_url}" target="_blank" style="background:#28a745; color:#fff; padding:12px 24px; font-weight:bold; border-radius:5px;">🔗 Apply Online Direct Link</a>
    </div>
</div>
"""

job_cards_html = ""

for job in jobs_data:
    title = job.get("title", "Government Job Alert")
    slug = job.get("slug") or re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    
    schema_json = f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org/",
      "@type": "JobPosting",
      "title": "{title}",
      "description": "Apply online for {title}. Vacancies: {job.get('vacancies', 'Various')}",
      "datePosted": "{job.get('updated_at', '2026-08-07')}",
      "validThrough": "2026-12-31",
      "employmentType": "FULL_TIME",
      "hiringOrganization": {{
        "@type": "Organization",
        "name": "BG Jobs",
        "sameAs": "https://bgsarkariresult.github.io/bgjob/"
      }}
    }}
    </script>
    """
    
    body_content = JOB_TEMPLATE_BODY.format(
        title=title,
        vacancies=job.get("vacancies", "Various Posts"),
        qualification=job.get("qualification", "Check Official Portal"),
        age_limit=job.get("age_limit", "Check Official Portal"),
        last_date=job.get("last_date", "Check Official Portal"),
        content_html=job.get("content_html", "<p>Check details above.</p>"),
        apply_url=job.get("apply_url", "#"),
        pdf_url=job.get("pdf_url", "#")
    )
    
    full_html = HTML_LAYOUT.format(page_title=title, schema_script=schema_json, main_content=body_content)
    file_name = f"jobs/{slug}.html"
    
    with open(file_name, "w", encoding="utf-8") as out_file:
        out_file.write(full_html)

    job_cards_html += f"""
    <a href="{slug}.html" class="card" style="background:#fff; border:1px solid #dee2e6; margin-bottom:10px; border-radius:4px;">
        <h3 style="color:#0073e6;">{title}</h3>
        <p><strong>Last Date:</strong> {job.get('last_date', 'N/A')} | <strong>Vacancies:</strong> {job.get('vacancies', 'N/A')}</p>
    </a>
    """

CATEGORY_INDEX_BODY = f"""
<div style="background:#fff; padding:20px; border-radius:6px; border:1px solid #dee2e6;">
    <h1 style="color:#0073e6; border-bottom: 2px solid #0073e6; padding-bottom: 8px;">Latest Job Notifications</h1>
    <div class="job-list" style="margin-top:15px;">
        {job_cards_html if job_cards_html else "<p>No active jobs found.</p>"}
    </div>
</div>
"""

category_html = HTML_LAYOUT.format(page_title="Latest Jobs - BG Jobs", schema_script="", main_content=CATEGORY_INDEX_BODY)

for d in directories:
    target_index = f"{d}/index.html"
    with open(target_index, "w", encoding="utf-8") as f:
        f.write(category_html)

print("🚀 Site Build Successful!")
