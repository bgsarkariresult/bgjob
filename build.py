import json
import os
import re
from datetime import datetime

# Configuration
JSON_FILE = "data/jobs.json"
OUTPUT_DIR = "jobs"
SITE_URL = "https://bgsarkariresult.github.io/bgjob"

# HTML Template for Job Post Pages
def get_job_html(job):
    title = job.get("title", "Government Job 2026")
    slug = job.get("slug", "")
    vacancies = job.get("vacancies", "Various")
    qualification = job.get("qualification", "10th/12th/Graduate")
    age_limit = job.get("age_limit", "18-35 Years")
    last_date = job.get("last_date", "Check Official Notification")
    apply_url = job.get("apply_url", "#")
    pdf_url = job.get("pdf_url", "#")
    image = job.get("image", "")
    content_html = job.get("content_html", "")
    categories = job.get("categories", ["Latest Jobs"])
    updated_at = job.get("updated_at", datetime.now().strftime("%Y-%m-%d"))
    
    # Generate category badges HTML
    category_badges = " ".join([f'<span class="category-badge">{cat}</span>' for cat in categories[:5]])
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <title>{title} Notification 2026 | Apply Online, Vacancy, PDF</title>
    <meta name="description" content="{title}: Check notification, eligibility, important dates, vacancies, age limit, and apply online link. Download official PDF.">
    <meta name="keywords" content="{title}, government jobs 2026, sarkari result, apply online, notification pdf, vacancy">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta name="theme-color" content="#0d0d0d">
    <link rel="canonical" href="{SITE_URL}/jobs/{slug}.html">
    <meta property="og:title" content="{title} Notification 2026">
    <meta property="og:description" content="{title}: Total {vacancies} posts. Last date: {last_date}. Apply online now!">
    <meta property="og:image" content="{image}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{SITE_URL}/jobs/{slug}.html">
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Roboto, 'Helvetica Neue', -apple-system, sans-serif;
            background: #f5f5f5;
            color: #1a1a1a;
            line-height: 1.8;
            -webkit-font-smoothing: antialiased;
        }}
        .header {{
            background: #0d0d0d;
            border-bottom: 3px solid #ff6b00;
            padding: 16px 24px;
            position: sticky;
            top: 0;
            z-index: 50;
        }}
        .header a {{
            color: #fff;
            text-decoration: none;
            font-size: 1.8rem;
            font-weight: 800;
        }}
        .header span {{
            background: #ff6b00;
            color: #000;
            padding: 4px 14px;
            border-radius: 30px;
        }}
        .nav {{
            background: #111;
            padding: 12px 24px;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            overflow-x: auto;
        }}
        .nav a {{
            color: #ccc;
            text-decoration: none;
            font-weight: 600;
            padding: 8px 18px;
            border-radius: 30px;
            font-size: 0.9rem;
            white-space: nowrap;
        }}
        .nav a:hover, .nav a.active {{
            background: #ff6b00;
            color: #000;
        }}
        .container {{
            max-width: 900px;
            margin: 30px auto;
            padding: 0 20px;
        }}
        .post {{
            background: #fff;
            border-radius: 16px;
            padding: 32px;
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
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
        }}
        .category-badge {{
            background: #ff6b00;
            color: #fff;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.7rem;
            font-weight: 600;
        }}
        .featured-image {{
            text-align: center;
            margin-bottom: 25px;
        }}
        .featured-image img {{
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            max-height: 450px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }}
        .job-content {{
            margin-top: 20px;
        }}
        .job-content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .job-content table td, .job-content table th {{
            border: 1px solid #ddd;
            padding: 12px 16px;
            text-align: left;
        }}
        .job-content table th {{
            background: #ff6b00;
            color: #fff;
            font-weight: 600;
        }}
        .job-content h2, .job-content h3 {{
            color: #ff6b00;
            margin: 24px 0 12px;
            border-left: 4px solid #ff6b00;
            padding-left: 14px;
        }}
        .btn-group {{
            text-align: center;
            margin: 25px 0;
            display: flex;
            gap: 12px;
            justify-content: center;
            flex-wrap: wrap;
        }}
        .btn {{
            display: inline-block;
            padding: 14px 28px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 700;
            font-size: 1rem;
            transition: 0.2s;
        }}
        .btn-primary {{
            background: #0073e6;
            color: #fff;
        }}
        .btn-primary:hover {{
            background: #005bb5;
        }}
        .btn-success {{
            background: #28a745;
            color: #fff;
        }}
        .btn-success:hover {{
            background: #1e7e34;
        }}
        .btn-orange {{
            background: #ff6b00;
            color: #fff;
        }}
        .btn-orange:hover {{
            background: #e65c00;
        }}
        footer {{
            background: #0d0d0d;
            color: #aaa;
            text-align: center;
            padding: 24px;
            margin-top: 40px;
            border-top: 3px solid #ff6b00;
        }}
        @media (max-width: 600px) {{
            .post {{
                padding: 20px 16px;
            }}
            h1 {{
                font-size: 1.4rem;
            }}
            .btn {{
                padding: 12px 20px;
                font-size: 0.9rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <a href="../index.html">BG <span>Jobs</span></a>
    </div>
    <div class="nav">
        <a href="../index.html">Home</a>
        <a href="index.html" class="active">Latest Jobs</a>
        <a href="../results/index.html">Result</a>
        <a href="../admit-card/index.html">Admit Card</a>
        <a href="../answer-key/index.html">Answer Key</a>
        <a href="../syllabus/index.html">Syllabus</a>
        <a href="../books/index.html">Books</a>
    </div>
    
    <div class="container">
        <article class="post">
            <h1>{title} Notification 2026</h1>
            <div class="meta">
                <span>📅 Updated: {updated_at}</span>
                {category_badges}
            </div>
            
            <div class="featured-image">
                <img src="{image}" alt="{title} Official Notification PDF" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&auto=format&fit=crop';">
            </div>
            
            <div class="btn-group">
                <a href="{pdf_url}" target="_blank" rel="nofollow" class="btn btn-primary">📄 Download Official PDF</a>
                <a href="{apply_url}" target="_blank" rel="nofollow" class="btn btn-success">🔗 Apply Online Link</a>
            </div>
            
            <div class="job-content">
                {content_html}
            </div>
            
            <div class="btn-group" style="margin-top: 30px;">
                <a href="{apply_url}" target="_blank" rel="nofollow" class="btn btn-orange">🚀 Apply Now - Direct Official Link</a>
            </div>
        </article>
    </div>
    
    <footer>
        <p>&copy; 2026 BG Jobs. All Rights Reserved. | Professional Government Job Portal</p>
        <p style="margin-top: 8px; font-size: 0.85rem;">
            <a href="../index.html" style="color: #ff6b00;">Home</a> | 
            <a href="index.html" style="color: #ff6b00;">All Jobs</a> | 
            <a href="{apply_url}" style="color: #ff6b00;" target="_blank">Official Apply Link</a>
        </p>
    </footer>
</body>
</html>"""


def generate_job_pages():
    """Generate HTML pages from data/jobs.json"""
    
    # Check if JSON file exists
    if not os.path.exists(JSON_FILE):
        print(f"❌ {JSON_FILE} not found! Skipping page generation.")
        return
    
    # Load jobs data
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        jobs = json.load(f)
    
    print(f"📊 Found {len(jobs)} job(s) in {JSON_FILE}")
    
    # Create jobs directory if not exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    generated_count = 0
    
    for job in jobs:
        slug = job.get("slug", "")
        if not slug:
            print(f"⚠️ Skipping job (no slug): {job.get('title', 'Unknown')}")
            continue
        
        # Generate HTML content
        html_content = get_job_html(job)
        
        # Write to file
        file_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        generated_count += 1
        print(f"✅ Generated: {file_path}")
    
    print(f"\n🎉 Total {generated_count} job pages generated successfully!")
    
    # Also generate the jobs listing page (index.html)
    generate_jobs_index_page(jobs)


def generate_jobs_index_page(jobs):
    """Generate jobs/index.html listing page"""
    
    job_list_items = ""
    for job in jobs[:50]:  # Limit to 50 jobs
        title = job.get("title", "Government Job")
        slug = job.get("slug", "")
        vacancies = job.get("vacancies", "Various")
        last_date = job.get("last_date", "Check Official")
        categories = job.get("categories", [])
        badge = ""
        if "New" in str(categories) or datetime.now().strftime("%Y-%m") in job.get("updated_at", ""):
            badge = '<span class="badge new">New</span>'
        
        job_list_items += f"""
                <li>
                    <a href="{slug}.html">
                        <span>{title}</span>
                        {badge}
                    </a>
                    <small style="color:#888;display:block;margin-top:4px;">📌 {vacancies} Posts | ⏰ Last Date: {last_date}</small>
                </li>"""
    
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Latest Government Jobs 2026 | BG Jobs</title>
    <meta name="description" content="Latest Government Jobs 2026 - SSC, Railway, Bank, Army, Police, MPESB & more. Find all Sarkari Naukri notifications.">
    <meta name="theme-color" content="#0d0d0d">
    <style>
        *{{margin:0;padding:0;box-sizing:border-box}}
        body{{font-family:'Segoe UI',Roboto,sans-serif;background:#f5f5f5;color:#1a1a1a;line-height:1.6}}
        .header{{background:#0d0d0d;border-bottom:3px solid #ff6b00;padding:16px 24px}}
        .header a{{color:#fff;text-decoration:none;font-size:1.8rem;font-weight:800}}
        .header span{{background:#ff6b00;color:#000;padding:4px 14px;border-radius:30px}}
        .nav{{background:#111;padding:12px 24px;display:flex;flex-wrap:wrap;gap:8px}}
        .nav a{{color:#ccc;text-decoration:none;font-weight:600;padding:8px 18px;border-radius:30px;font-size:0.9rem}}
        .nav a:hover,.nav a.active{{background:#ff6b00;color:#000}}
        .container{{max-width:1100px;margin:30px auto;padding:0 20px}}
        h1{{font-size:2rem;margin-bottom:8px;color:#0d0d0d}}
        h1 span{{color:#ff6b00}}
        .job-list{{list-style:none;display:flex;flex-direction:column;gap:12px}}
        .job-list li{{background:#fff;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,0.06);transition:0.2s;padding:18px 24px}}
        .job-list li:hover{{box-shadow:0 6px 20px rgba(255,107,0,0.15);border-left:4px solid #ff6b00}}
        .job-list a{{text-decoration:none;color:#1a1a1a;font-weight:600;font-size:1rem}}
        .job-list a:hover{{color:#ff6b00}}
        .badge{{background:#e8f5e9;color:#1b5e20;padding:2px 10px;border-radius:15px;font-size:0.7rem;font-weight:700;margin-left:8px}}
        .badge.hot{{background:#ffebee;color:#b71c1c}}
        footer{{background:#0d0d0d;color:#aaa;text-align:center;padding:24px;margin-top:40px;border-top:3px solid #ff6b00}}
        @media(max-width:600px){{h1{{font-size:1.5rem}}.job-list li{{padding:14px 16px}}}}
    </style>
</head>
<body>
    <div class="header"><a href="../index.html">BG <span>Jobs</span></a></div>
    <div class="nav">
        <a href="../index.html">Home</a>
        <a href="index.html" class="active">Latest Jobs</a>
        <a href="../results/index.html">Result</a>
        <a href="../admit-card/index.html">Admit Card</a>
        <a href="../answer-key/index.html">Answer Key</a>
        <a href="../syllabus/index.html">Syllabus</a>
        <a href="../books/index.html">Books</a>
    </div>
    <div class="container">
        <h1>⭐ <span>Latest Government Jobs</span> 2026</h1>
        <p style="color:#555;margin-bottom:24px">Total Jobs: {len(jobs)} | Auto-updated by BG Jobs Bot</p>
        <ul class="job-list">
            {job_list_items}
        </ul>
    </div>
    <footer>&copy; 2026 BG Jobs. All Rights Reserved.</footer>
</body>
</html>"""
    
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    
    print(f"✅ Generated jobs listing page: {OUTPUT_DIR}/index.html")


if __name__ == "__main__":
    generate_job_pages()
