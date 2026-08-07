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
            <a href="../answer-key/index.html">Answer Key</a>
            <a href="../syllabus/index.html">Syllabus</a>
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

# Category Data Separation Logic
categorized_jobs = {d: "" for d in directories}

for job in jobs_data:
    title = job.get("title", "Government Job Alert")
    title_lower = title.lower()
    slug = job.get("slug") or re.sub(r'[^a-z0-9]+', '-', title_lower).strip('-')
    categories = [c.lower() for c in job.get("categories", [])]
    
    # 1. Single Detail Page Generation
    schema_json = f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org/",
      "@type": "JobPosting",
      "title": "{title}",
      "description": "Apply online for {title}.",
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

    # 2. Card HTML Generation
    card_html = f"""
    <a href="../jobs/{slug}.html" class="card" style="background:#fff; border:1px solid #dee2e6; margin-bottom:10px; border-radius:4px; display:block; padding:12px 15px; text-decoration:none;">
        <h3 style="color:#0073e6; margin:0 0 5px 0;">{title}</h3>
        <p style="margin:0; color:#666; font-size:14px;"><strong>Last Date:</strong> {job.get('last_date', 'N/A')} | <strong>Vacancies:</strong> {job.get('vacancies', 'N/A')}</p>
    </a>
    """

    # Advanced Smart Categorization (Title + Categories Matching)
    is_admit = any(k in title_lower for k in ["admit card", "call letter", "hall ticket"]) or any("admit" in c for c in categories)
    is_result = any(k in title_lower for k in ["result", "merit", "marks", "exam date"]) or any("result" in c for c in categories)
    is_key = any(k in title_lower for k in ["answer key", "key"]) or any("key" in c for c in categories)
    is_syllabus = any(k in title_lower for k in ["syllabus", "pattern"]) or any("syllabus" in c for c in categories)
    is_ca = any(k in title_lower for k in ["current affairs", "gk"]) or any("affairs" in c for c in categories)

    if is_admit:
        categorized_jobs["admit-card"] += card_html
    elif is_result:
        categorized_jobs["results"] += card_html
    elif is_key:
        categorized_jobs["answer-key"] += card_html
    elif is_syllabus:
        categorized_jobs["syllabus"] += card_html
    elif is_ca:
        categorized_jobs["current-affairs"] += card_html
    else:
        # Defaults to Latest Jobs recruitment
        categorized_jobs["jobs"] += card_html

# 3. Generate Category-Specific Listing Pages
for d in directories:
    cards = categorized_jobs[d]
    display_title = d.replace('-', ' ').title()
    
    content_body = f"""
    <div style="background:#fff; padding:20px; border-radius:6px; border:1px solid #dee2e6;">
        <h1 style="color:#0073e6; border-bottom: 2px solid #0073e6; padding-bottom: 8px;">{display_title} Updates</h1>
        <div class="job-list" style="margin-top:15px;">
            {cards if cards else f"<p style='padding:15px; color:#666;'>Abhi {display_title} me koi naya update nahi hai.</p>"}
        </div>
    </div>
    """
    
    target_index = f"{d}/index.html"
    category_html = HTML_LAYOUT.format(page_title=f"{display_title} - BG Jobs", schema_script="", main_content=content_body)
    
    with open(target_index, "w", encoding="utf-8") as f:
        f.write(category_html)

print("🚀 Site Build Successful with Smart Filtering!")
