import json
import os
import re
from datetime import datetime

# Directories setup
directories = ["jobs", "results", "admit-card", "answer-key", "syllabus", "current-affairs", "admission", "scholarship"]
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
        jobs_data = []
else:
    print(f"⚠️ JSON file not found at {json_path}")
    # Sample data for testing
    jobs_data = [
        {
            "title": "SSC CGL Recruitment 2026",
            "slug": "ssc-cgl-recruitment-2026",
            "vacancies": "17727",
            "qualification": "Graduate",
            "age_limit": "18-32 Years",
            "last_date": "15-09-2026",
            "apply_url": "https://ssc.nic.in",
            "pdf_url": "https://ssc.nic.in/pdf/notification.pdf",
            "content_html": "<p>SSC CGL 2026 notification for 17727 posts has been released.</p>",
            "categories": ["government-jobs", "ssc"],
            "updated_at": "2026-08-07"
        },
        {
            "title": "MPESB Patwari Admit Card 2026",
            "slug": "mpesb-patwari-admit-card-2026",
            "vacancies": "200",
            "qualification": "Graduate",
            "age_limit": "18-40 Years",
            "last_date": "20-08-2026",
            "apply_url": "https://mpesb.gov.in",
            "pdf_url": "https://mpesb.gov.in/admit-card.pdf",
            "content_html": "<p>MPESB Patwari admit card now available for download.</p>",
            "categories": ["admit-card", "mpesb"],
            "updated_at": "2026-08-07"
        },
        {
            "title": "UPSC Civil Services Result 2026",
            "slug": "upsc-civil-services-result-2026",
            "vacancies": "1056",
            "qualification": "Graduate",
            "age_limit": "21-32 Years",
            "last_date": "Check Notification",
            "apply_url": "https://upsc.gov.in",
            "pdf_url": "https://upsc.gov.in/result.pdf",
            "content_html": "<p>UPSC Civil Services 2026 result declared.</p>",
            "categories": ["result", "upsc"],
            "updated_at": "2026-08-07"
        },
        {
            "title": "Bank of India Answer Key 2026",
            "slug": "bank-of-india-answer-key-2026",
            "vacancies": "500",
            "qualification": "Graduate",
            "age_limit": "21-30 Years",
            "last_date": "Check Notification",
            "apply_url": "https://bankofindia.co.in",
            "pdf_url": "https://bankofindia.co.in/answer-key.pdf",
            "content_html": "<p>BOI answer key released for credit officer exam.</p>",
            "categories": ["answer-key", "bank"],
            "updated_at": "2026-08-07"
        },
        {
            "title": "SSC CGL 2026 Syllabus",
            "slug": "ssc-cgl-2026-syllabus",
            "vacancies": "N/A",
            "qualification": "Check Syllabus",
            "age_limit": "Check Syllabus",
            "last_date": "Check Notification",
            "apply_url": "#",
            "pdf_url": "#",
            "content_html": "<p>SSC CGL 2026 syllabus PDF download available.</p>",
            "categories": ["syllabus", "ssc"],
            "updated_at": "2026-08-07"
        },
        {
            "title": "Current Affairs for Government Exams 2026",
            "slug": "current-affairs-2026",
            "vacancies": "N/A",
            "qualification": "N/A",
            "age_limit": "N/A",
            "last_date": "N/A",
            "apply_url": "#",
            "pdf_url": "#",
            "content_html": "<p>Monthly current affairs PDF for competitive exams.</p>",
            "categories": ["current-affairs", "gk"],
            "updated_at": "2026-08-07"
        }
    ]
    print(f"📖 Loaded {len(jobs_data)} sample jobs for testing")

HTML_LAYOUT = """<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <meta name="description" content="BG Jobs - {page_title}. Latest Sarkari Jobs, Admit Card, Results and Answer Key 2026.">
    <link rel="canonical" href="https://bgsarkariresult.github.io/bgjob/">
    <link rel="stylesheet" href="../assets/css/style.css">
    {schema_script}
</head>
<body>

<header class="site-header sticky-header">
    <div class="container header-flex">
        <h1 class="logo"><a href="../index.html">BG <span>Jobs</span></a></h1>
        <form action="../search.html" class="search-box" role="search">
            <input type="search" name="q" placeholder="Search Jobs, Results, Admit Card..." aria-label="Search">
            <button type="submit" aria-label="Search">🔍</button>
        </form>
        <button class="dark-mode-toggle" aria-label="Toggle Dark Mode" id="darkModeToggle">🌙</button>
    </div>
    <nav class="main-nav">
        <div class="container nav-links">
            <a href="../index.html">Home</a>
            <a href="../jobs/index.html">Latest Jobs</a>
            <a href="../results/index.html">Results</a>
            <a href="../admit-card/index.html">Admit Card</a>
            <a href="../answer-key/index.html">Answer Key</a>
            <a href="../syllabus/index.html">Syllabus</a>
            <a href="../current-affairs/index.html">Current Affairs</a>
        </div>
    </nav>
</header>

<main class="container" style="margin-top:20px; min-height:60vh;">
    {main_content}
</main>

<footer class="site-footer">
    <div class="container footer-content">
        <div class="footer-grid">
            <div class="footer-section">
                <h3>BG Jobs</h3>
                <p>Your trusted source for latest Sarkari Jobs, Admit Cards, Results and Answer Keys.</p>
            </div>
            <div class="footer-section">
                <h3>Quick Links</h3>
                <ul>
                    <li><a href="../about.html">About Us</a></li>
                    <li><a href="../contact.html">Contact Us</a></li>
                    <li><a href="../privacy-policy.html">Privacy Policy</a></li>
                    <li><a href="../disclaimer.html">Disclaimer</a></li>
                </ul>
            </div>
        </div>
        <p class="copyright">&copy; 2026 BG Jobs. All Rights Reserved.</p>
    </div>
</footer>

<script>
    // Dark Mode Toggle
    document.addEventListener('DOMContentLoaded', function() {{
        const toggle = document.getElementById('darkModeToggle');
        if (toggle) {{
            if (localStorage.getItem('darkMode') === 'enabled') {{
                document.body.classList.add('dark-mode');
                toggle.textContent = '☀️';
            }}
            toggle.addEventListener('click', function() {{
                document.body.classList.toggle('dark-mode');
                if (document.body.classList.contains('dark-mode')) {{
                    localStorage.setItem('darkMode', 'enabled');
                    toggle.textContent = '☀️';
                }} else {{
                    localStorage.setItem('darkMode', 'disabled');
                    toggle.textContent = '🌙';
                }}
            }});
        }}
    }});
</script>

</body>
</html>
"""

JOB_TEMPLATE_BODY = """
<nav aria-label="Breadcrumb" class="breadcrumb">
    <ol>
        <li><a href="../index.html">Home</a></li>
        <li><a href="../jobs/index.html">Jobs</a></li>
        <li aria-current="page">{title}</li>
    </ol>
</nav>

<div style="background:#fff; padding:25px; border-radius:8px; border: 1px solid #dee2e6;">
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
        <a href="{pdf_url}" target="_blank" rel="noopener noreferrer" style="background:#0073e6; color:#fff; padding:12px 24px; font-weight:bold; border-radius:5px; text-decoration:none; display:inline-block;">📄 Download Official PDF</a>
        <a href="{apply_url}" target="_blank" rel="noopener noreferrer" style="background:#28a745; color:#fff; padding:12px 24px; font-weight:bold; border-radius:5px; text-decoration:none; display:inline-block;">🔗 Apply Online Direct Link</a>
    </div>
    
    <div style="margin-top:30px; padding-top:20px; border-top:1px solid #dee2e6;">
        <h3 style="color:#0073e6;">Related Jobs</h3>
        <ul style="list-style:none; padding:0;">
            <li><a href="../jobs/index.html">🔹 Latest Government Jobs</a></li>
            <li><a href="../results/index.html">🔹 Latest Results</a></li>
            <li><a href="../admit-card/index.html">🔹 Admit Cards</a></li>
        </ul>
    </div>
</div>
"""

# Category Page Template
CATEGORY_TEMPLATE = """
<div style="background:#fff; padding:20px; border-radius:6px; border:1px solid #dee2e6;">
    <h1 style="color:#0073e6; border-bottom: 2px solid #0073e6; padding-bottom: 8px;">{display_title} Updates</h1>
    <div class="job-list" style="margin-top:15px;">
        {cards}
    </div>
    <div style="margin-top:20px; text-align:center;">
        <a href="../index.html" style="color:#0073e6; font-weight:bold;">← Home Page पर वापस जाएं</a>
    </div>
</div>
"""

# Store categorized jobs
categorized_jobs = {d: [] for d in directories}

# Counter for stats
stats = {
    "total": len(jobs_data),
    "jobs": 0,
    "results": 0,
    "admit-card": 0,
    "answer-key": 0,
    "syllabus": 0,
    "current-affairs": 0,
    "admission": 0,
    "scholarship": 0
}

# Process each job
for job in jobs_data:
    title = job.get("title", "Government Job Alert")
    title_lower = title.lower()
    
    # Generate slug if not present
    slug = job.get("slug")
    if not slug:
        slug = re.sub(r'[^a-z0-9]+', '-', title_lower).strip('-')
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
    
    categories = [c.lower() for c in job.get("categories", [])]
    
    # Create safe values for template
    safe_title = title.replace('"', '&quot;').replace("'", "&#39;")
    safe_vacancies = job.get("vacancies", "Various Posts")
    safe_qualification = job.get("qualification", "Check Official Portal")
    safe_age_limit = job.get("age_limit", "Check Official Portal")
    safe_last_date = job.get("last_date", "Check Official Portal")
    safe_apply_url = job.get("apply_url", "#")
    safe_pdf_url = job.get("pdf_url", "#")
    safe_content = job.get("content_html", "<p>Check official notification for details.</p>")
    
    # 1. Generate Single Detail Page
    schema_json = f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org/",
      "@type": "JobPosting",
      "title": "{safe_title}",
      "description": "Apply online for {safe_title}. Latest government job notification.",
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
        title=safe_title,
        vacancies=safe_vacancies,
        qualification=safe_qualification,
        age_limit=safe_age_limit,
        last_date=safe_last_date,
        content_html=safe_content,
        apply_url=safe_apply_url,
        pdf_url=safe_pdf_url
    )
    
    full_html = HTML_LAYOUT.format(
        page_title=f"{safe_title} - BG Jobs",
        schema_script=schema_json,
        main_content=body_content
    )
    
    # Ensure jobs directory exists
    os.makedirs("jobs", exist_ok=True)
    file_name = f"jobs/{slug}.html"
    
    with open(file_name, "w", encoding="utf-8") as out_file:
        out_file.write(full_html)
    print(f"✅ Generated: {file_name}")

    # 2. Generate Card HTML with proper structure
    card_html = f"""
    <div class="job-card" style="background:#fff; border:1px solid #dee2e6; margin-bottom:15px; border-radius:8px; padding:15px; transition: box-shadow 0.3s;">
        <a href="../jobs/{slug}.html" style="text-decoration:none; color:inherit; display:block;">
            <h3 style="color:#0073e6; margin:0 0 8px 0; font-size:18px;">{safe_title}</h3>
            <div style="display:flex; flex-wrap:wrap; gap:15px; color:#666; font-size:14px;">
                <span><strong>Last Date:</strong> {safe_last_date}</span>
                <span><strong>Vacancies:</strong> {safe_vacancies}</span>
                <span><strong>Qualification:</strong> {safe_qualification}</span>
            </div>
        </a>
    </div>
    """

    # Advanced Smart Categorization
    is_admit = any(k in title_lower for k in ["admit card", "call letter", "hall ticket", "admitcard"]) or any("admit" in c for c in categories)
    is_result = any(k in title_lower for k in ["result", "merit", "marks", "exam date", "score"]) or any("result" in c for c in categories)
    is_key = any(k in title_lower for k in ["answer key", "answerkey", "key"]) or any("key" in c for c in categories)
    is_syllabus = any(k in title_lower for k in ["syllabus", "pattern", "curriculum"]) or any("syllabus" in c for c in categories)
    is_ca = any(k in title_lower for k in ["current affairs", "gk", "general knowledge"]) or any("affairs" in c for c in categories)
    is_admission = any(k in title_lower for k in ["admission", "admission open", "apply for admission"]) or any("admission" in c for c in categories)
    is_scholarship = any(k in title_lower for k in ["scholarship", "scholarship 2026"]) or any("scholarship" in c for c in categories)

    # Assign to category and update stats
    if is_admit:
        categorized_jobs["admit-card"].append(card_html)
        stats["admit-card"] += 1
    elif is_result:
        categorized_jobs["results"].append(card_html)
        stats["results"] += 1
    elif is_key:
        categorized_jobs["answer-key"].append(card_html)
        stats["answer-key"] += 1
    elif is_syllabus:
        categorized_jobs["syllabus"].append(card_html)
        stats["syllabus"] += 1
    elif is_ca:
        categorized_jobs["current-affairs"].append(card_html)
        stats["current-affairs"] += 1
    elif is_admission:
        categorized_jobs["admission"].append(card_html)
        stats["admission"] += 1
    elif is_scholarship:
        categorized_jobs["scholarship"].append(card_html)
        stats["scholarship"] += 1
    else:
        # Default to Latest Jobs
        categorized_jobs["jobs"].append(card_html)
        stats["jobs"] += 1

# 3. Generate Category-Specific Listing Pages
for d in directories:
    cards = "".join(categorized_jobs[d]) if categorized_jobs[d] else ""
    display_title = d.replace('-', ' ').title()
    
    if cards:
        content_body = CATEGORY_TEMPLATE.format(
            display_title=display_title,
            cards=cards
        )
    else:
        content_body = CATEGORY_TEMPLATE.format(
            display_title=display_title,
            cards=f"<p style='padding:20px; color:#666; text-align:center;'>📢 No {display_title} updates available at the moment. Check back soon!</p>"
        )
    
    target_index = f"{d}/index.html"
    category_html = HTML_LAYOUT.format(
        page_title=f"{display_title} - BG Jobs",
        schema_script="",
        main_content=content_body
    )
    
    with open(target_index, "w", encoding="utf-8") as f:
        f.write(category_html)
    print(f"✅ Generated category page: {target_index}")

# Print Summary
print("\n" + "="*50)
print("🚀 SITE BUILD SUCCESSFUL!")
print("="*50)
print(f"📊 Total Jobs Processed: {stats['total']}")
print(f"   ├── Latest Jobs: {stats['jobs']}")
print(f"   ├── Results: {stats['results']}")
print(f"   ├── Admit Cards: {stats['admit-card']}")
print(f"   ├── Answer Keys: {stats['answer-key']}")
print(f"   ├── Syllabus: {stats['syllabus']}")
print(f"   ├── Current Affairs: {stats['current-affairs']}")
print(f"   ├── Admission: {stats['admission']}")
print(f"   └── Scholarship: {stats['scholarship']}")
print("="*50)
print(f"✅ {len(jobs_data)} job pages generated successfully!")
print(f"✅ {len(directories)} category pages generated successfully!")
print("="*50)
