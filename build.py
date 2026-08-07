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

# 2. HTML Template for Single Job Page with Schema & Header/Footer
JOB_TEMPLATE = """<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | BG Jobs</title>
    <meta name="description" content="{title} - Get eligibility, vacancies, last date, and direct apply link.">
    <link rel="stylesheet" href="../assets/css/style.css">
    <link rel="shortcut icon" href="../favicon.ico" type="image/x-icon">

    <!-- Job Posting Schema -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org/",
      "@type": "JobPosting",
      "title": "{title}",
      "description": "Apply online for {title}...",
      "identifier": {{
        "@type": "PropertyValue",
        "name": "BGJobs",
        "value": "{slug}"
      }},
      "datePosted": "{date_posted}",
      "validThrough": "{last_date}",
      "employmentType": "FULL_TIME",
      "hiringOrganization": {{
        "@type": "Organization",
        "name": "{organization}",
        "sameAs": "https://bgsarkariresult.github.io/bgjob/"
      }},
      "jobLocation": {{
        "@type": "Place",
        "address": {{
          "@type": "PostalAddress",
          "addressCountry": "IN"
        }}
      }}
    }}
    </script>
    <style>
        .container-job {{ max-width: 900px; margin: 20px auto; background: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .info-box {{ background: #e8f4fd; padding: 15px; border-left: 4px solid #0b7a2f; margin-bottom: 20px; border-radius: 4px; }}
        .btn {{ display: inline-block; padding: 12px 24px; color: #fff; text-decoration: none; font-weight: bold; border-radius: 5px; margin: 5px; }}
        .btn-apply {{ background-color: #28a745; }}
        .btn-pdf {{ background-color: #0073e6; }}
    </style>
</head>
<body>
    <header class="site-header">
        <div class="container header-flex">
            <a href="../index.html" class="logo">BG <span>Jobs</span></a>
        </div>
    </header>

    <main class="container-job">
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
    </main>

    <footer class="site-footer" style="margin-top:40px; text-align:center; padding:20px; background:#222; color:#fff;">
        <p>&copy; 2026 BG Jobs. All Rights Reserved.</p>
    </footer>
</body>
</html>
"""

# 3. Generate Job Detail Pages Only
for job in jobs_data:
    title = job.get("title", "Government Job Alert 2026")
    slug = job.get("slug") or re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    vacancies = job.get("vacancies", "Various")
    last_date = job.get("last_date", "2026-12-31")
    date_posted = job.get("date_posted", "2026-08-01")
    organization = job.get("organization", "Govt Organization")
    
    html_out = JOB_TEMPLATE.format(
        title=title,
        slug=slug,
        vacancies=vacancies,
        qualification=job.get("qualification", "Check Official Notice"),
        age_limit=job.get("age_limit", "18-35 Years"),
        last_date=last_date,
        date_posted=date_posted,
        organization=organization,
        content_html=job.get("content_html", "<p>Check official notification details above.</p>"),
        apply_url=job.get("apply_url", "#"),
        pdf_url=job.get("pdf_url", "#")
    )
    
    file_name = f"jobs/{slug}.html"
    with open(file_name, "w", encoding="utf-8") as out_file:
        out_file.write(html_out)
    print(f"Generated: {file_name}")

print("🚀 All job post pages generated successfully in /jobs/ folder!")
