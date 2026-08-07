import json
import os
import re
from datetime import datetime

# Set up required directories
directories = ["jobs", "results", "admit-card", "answer-key", "syllabus", "books"]
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

# Master HTML Base Wrapper with Black & Orange Professional Theme
def wrap_html(title, content, is_subfolder=False):
    base_prefix = "../" if is_subfolder else "./"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <title>{title} | BG Jobs</title>
    <meta name="description" content="{title} - Latest Government Job updates, results, admit cards & more.">
    <meta name="theme-color" content="#0d0d0d">
    <meta name="robots" content="index, follow">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Roboto, 'Helvetica Neue', -apple-system, sans-serif;
            background: #f5f5f5;
            color: #1a1a1a;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }}
        header {{
            background: #0d0d0d;
            border-bottom: 3px solid #ff6b00;
            padding: 16px 24px;
            position: sticky;
            top: 0;
            z-index: 50;
        }}
        header a {{
            color: #fff;
            text-decoration: none;
            font-size: 1.8rem;
            font-weight: 800;
        }}
        header span {{
            background: #ff6b00;
            color: #000;
            padding: 4px 14px;
            border-radius: 30px;
        }}
        nav {{
            background: #111;
            padding: 12px 24px;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            overflow-x: auto;
        }}
        nav a {{
            color: #ccc;
            text-decoration: none;
            font-weight: 600;
            padding: 8px 18px;
            border-radius: 30px;
            font-size: 0.9rem;
            white-space: nowrap;
            transition: 0.2s;
        }}
        nav a:hover, nav a.active {{
            background: #ff6b00;
            color: #000;
        }}
        .container {{
            max-width: 950px;
            margin: 30px auto;
            padding: 0 20px;
        }}
        .post {{
            background: #fff;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }}
        h1 {{
            font-size: 1.8rem;
            color: #0d0d0d;
            margin-bottom: 12px;
            line-height: 1.3;
        }}
        .meta {{
            color: #777;
            font-size: 0.9rem;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid #eee;
        }}
        .card {{
            background: #fff;
            border-left: 4px solid #ff6b00;
            padding: 16px 20px;
            margin-bottom: 12px;
            border-radius: 8px;
            display: block;
            text-decoration: none;
            color: #1a1a1a;
            transition: 0.2s;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}
        .card:hover {{
            background: #fff8f3;
            border-left-color: #e65c00;
            box-shadow: 0 4px 16px rgba(255,107,0,0.12);
        }}
        .card h3 {{
            margin: 0 0 6px 0;
            color: #ff6b00;
            font-size: 18px;
        }}
        .card p {{
            margin: 0;
            font-size: 14px;
            color: #666;
        }}
        .btn {{
            display: inline-block;
            padding: 12px 24px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 700;
            transition: 0.2s;
            text-align: center;
        }}
        .btn-primary {{
            background: #0073e6;
            color: #fff;
        }}
        .btn-primary:hover {{ background: #005bb5; }}
        .btn-success {{
            background: #28a745;
            color: #fff;
        }}
        .btn-success:hover {{ background: #1e7e34; }}
        .btn-orange {{
            background: #ff6b00;
            color: #fff;
        }}
        .btn-orange:hover {{ background: #e65c00; }}
        .job-content h2, .job-content h3 {{
            color: #ff6b00;
            margin: 20px 0 10px;
            border-left: 4px solid #ff6b00;
            padding-left: 12px;
        }}
        .job-content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        .job-content table td, .job-content table th {{
            border: 1px solid #ddd;
            padding: 10px 14px;
            text-align: left;
        }}
        .job-content table th {{
            background: #ff6b00;
            color: #fff;
        }}
        .job-content ul, .job-content ol {{
            padding-left: 20px;
            margin: 10px 0;
        }}
        .job-content li {{
            margin: 6px 0;
        }}
        .badge {{
            display: inline-block;
            background: #e8f5e9;
            color: #1b5e20;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.7rem;
            font-weight: 700;
        }}
        footer {{
            margin-top: 40px;
            text-align: center;
            padding: 20px;
            background: #0d0d0d;
            color: #aaa;
            border-top: 3px solid #ff6b00;
        }}
        footer a {{
            color: #ff6b00;
            text-decoration: none;
        }}
        @media (max-width: 600px) {{
            .post {{ padding: 20px 16px; }}
            h1 {{ font-size: 1.4rem; }}
            .btn {{ padding: 10px 18px; font-size: 0.9rem; }}
            header a {{ font-size: 1.4rem; }}
        }}
    </style>
</head>
<body>

<header>
    <a href="{base_prefix}index.html">BG <span>Jobs</span></a>
</header>

<nav>
    <a href="{base_prefix}index.html">Home</a>
    <a href="{base_prefix}jobs/index.html">Latest Jobs</a>
    <a href="{base_prefix}results/index.html">Result</a>
    <a href="{base_prefix}admit-card/index.html">Admit Card</a>
    <a href="{base_prefix}answer-key/index.html">Answer Key</a>
    <a href="{base_prefix}syllabus/index.html">Syllabus</a>
    <a href="{base_prefix}books/index.html">Books</a>
</nav>

<div class="container">
    {content}
</div>

<footer>
    <p>&copy; 2026 BG Jobs. All Rights Reserved. | Professional Government Job Portal</p>
    <p style="margin-top: 8px; font-size: 0.85rem;">
        <a href="{base_prefix}index.html">Home</a> | 
        <a href="{base_prefix}jobs/index.html">All Jobs</a> | 
        <a href="{base_prefix}results/index.html">Results</a>
    </p>
</footer>

</body>
</html>"""


# 2. Generate Single Detail Pages & Prepare Home/Category List
home_job_cards = ""

for job in jobs_data:
    title = job.get("title", "Government Job Alert")
    slug = job.get("slug") or re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    vacancies = job.get("vacancies", "Various Posts")
    qualification = job.get("qualification", "10th/12th/Graduate")
    age_limit = job.get("age_limit", "18-35 Years")
    last_date = job.get("last_date", "Check Official Portal")
    apply_url = job.get("apply_url", "#")
    pdf_url = job.get("pdf_url", "#")
    image = job.get("image", "")
    content_html = job.get("content_html", "")
    categories = job.get("categories", [])
    updated_at = job.get("updated_at", datetime.now().strftime("%Y-%m-%d"))
    
    # Generate category badges
    category_badges = " ".join([f'<span class="badge">{cat}</span>' for cat in categories[:4]])
    
    # ✅ FIX: content_html ko BINA <p> wrap ke directly render karo
    if content_html and len(str(content_html)) > 50:
        full_content = str(content_html)
    else:
        full_content = f"""
        <p>Complete details about <strong>{title}</strong> including eligibility criteria, important dates, 
        application fee, selection process, and step-by-step apply online guide.</p>
        
        <h2>📋 Important Details</h2>
        <table>
            <tr><th>Parameter</th><th>Details</th></tr>
            <tr><td><strong>Total Vacancies</strong></td><td>{vacancies}</td></tr>
            <tr><td><strong>Qualification</strong></td><td>{qualification}</td></tr>
            <tr><td><strong>Age Limit</strong></td><td>{age_limit}</td></tr>
            <tr><td><strong>Last Date</strong></td><td>{last_date}</td></tr>
        </table>
        
        <h2>📝 How to Apply</h2>
        <ol>
            <li>Visit the official website</li>
            <li>Register with valid email & mobile</li>
            <li>Fill the application form carefully</li>
            <li>Upload required documents</li>
            <li>Pay application fee (if applicable)</li>
            <li>Submit and take a printout</li>
        </ol>
        
        <h2>❓ FAQs</h2>
        <p><strong>Q. What is the last date?</strong><br>{last_date}</p>
        <p><strong>Q. How many vacancies?</strong><br>{vacancies} posts</p>
        <p><strong>Q. What is the qualification required?</strong><br>{qualification}</p>
        """
    
    # Detail Page HTML Content
    detail_content = f"""
    <div class="post">
        <p style="margin-bottom:15px;">
            <a href="index.html" style="color:#ff6b00; font-weight:bold; text-decoration:none;">← Back to All Jobs</a>
        </p>
        
        <h1>{title} Notification 2026</h1>
        
        <div class="meta">
            <span>📅 Updated: {updated_at}</span>
            <span style="margin-left:10px;">{category_badges}</span>
        </div>
        
        {f'<div style="text-align:center; margin-bottom:20px;"><img src="{image}" alt="{title}" style="max-width:100%; border-radius:12px; max-height:400px; box-shadow:0 4px 12px rgba(0,0,0,0.1);" loading="lazy" onerror="this.style.display=\'none\'"></div>' if image else ''}
        
        <div style="text-align:center; margin-bottom:25px; display:flex; gap:12px; justify-content:center; flex-wrap:wrap;">
            <a href="{pdf_url}" target="_blank" rel="nofollow" class="btn btn-primary">📄 Download Official PDF</a>
            <a href="{apply_url}" target="_blank" rel="nofollow" class="btn btn-success">🔗 Apply Online Direct Link</a>
        </div>
        
        <div class="job-content">
            {full_content}
        </div>
        
        <div style="text-align:center; margin-top:30px;">
            <a href="{apply_url}" target="_blank" rel="nofollow" class="btn btn-orange">🚀 Apply Now - Direct Official Link</a>
        </div>
    </div>
    """
    
    # Save Subfolder Detail Page
    single_page_html = wrap_html(title, detail_content, is_subfolder=True)
    file_path = f"jobs/{slug}.html"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(single_page_html)
    print(f"✅ Generated Post: {file_path}")

    # Build List Cards
    home_job_cards += f"""
    <a href="jobs/{slug}.html" class="card">
        <h3>{title}</h3>
        <p><strong>Vacancies:</strong> {vacancies} | <strong>Last Date:</strong> {last_date}</p>
    </a>
    """

# 3. Generate Root index.html (Homepage)
home_content = f"""
<div class="post">
    <h1 style="text-align:center;">Latest <span style="color:#ff6b00;">Government Jobs</span> 2026</h1>
    <p style="text-align:center;color:#666;margin-bottom:20px;">Find all Sarkari Naukri notifications, admit cards, results & more</p>
    <div class="job-list">
        {home_job_cards if home_job_cards else "<p style='text-align:center;'>No active jobs found. Check back soon!</p>"}
    </div>
</div>
"""
with open("index.html", "w", encoding="utf-8") as f:
    f.write(wrap_html("BG Jobs - Latest Sarkari Result & Job Updates 2026", home_content, is_subfolder=False))
print("✅ Generated Root index.html")

# 4. Generate Category Listing Pages
category_cards = home_job_cards.replace('href="jobs/', 'href="')

category_content = f"""
<div class="post">
    <p><a href="../index.html" style="color:#ff6b00; font-weight:bold; text-decoration:none;">← Back to Home</a></p>
    <h2 style="margin-top:15px;">All Latest Notifications</h2>
    <div class="job-list">
        {category_cards if category_cards else "<p>No active postings yet.</p>"}
    </div>
</div>
"""

for d in directories:
    target_index = f"{d}/index.html"
    with open(target_index, "w", encoding="utf-8") as f:
        f.write(wrap_html(f"{d.replace('-', ' ').title()} - BG Jobs", category_content, is_subfolder=True))
    print(f"✅ Generated Listing: {target_index}")

# 5. Generate Empty Category Pages (for sections without dynamic data)
static_sections = {
    "results": "📄 Latest Exam Results 2026",
    "admit-card": "🎫 Latest Admit Cards 2026", 
    "answer-key": "🔑 Latest Answer Keys 2026",
    "syllabus": "📋 Latest Exam Syllabus 2026",
    "books": "📚 Recommended Books for Govt Exams 2026"
}

for folder, heading in static_sections.items():
    index_file = f"{folder}/index.html"
    # Only create if not already created above
    if not os.path.exists(index_file) or os.path.getsize(index_file) < 500:
        static_content = f"""
        <div class="post">
            <p><a href="../index.html" style="color:#ff6b00; font-weight:bold; text-decoration:none;">← Back to Home</a></p>
            <h1 style="text-align:center; margin-top:15px;">{heading}</h1>
            <p style="text-align:center; color:#666;">This section will be updated soon with latest updates.</p>
            <div class="job-list">
                {category_cards if category_cards else "<p style='text-align:center;'>Content coming soon...</p>"}
            </div>
        </div>
        """
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(wrap_html(f"{heading} - BG Jobs", static_content, is_subfolder=True))
        print(f"✅ Generated Static Page: {index_file}")

print("\n🚀 Complete Site Build Successful! All pages generated.")
print(f"📊 Total Jobs Processed: {len(jobs_data)}")
