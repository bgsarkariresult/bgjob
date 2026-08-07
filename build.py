# Create index.html (Homepage)
INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BGJob - Latest Sarkari Results & Government Jobs 2026</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #f4f6f9; color: #333; }
        .header { background: #0073e6; color: #fff; padding: 15px; text-align: center; }
        .container { max-width: 900px; margin: 20px auto; padding: 0 15px; }
        .job-card { background: #fff; padding: 15px; border-radius: 6px; margin-bottom: 12px; box-shadow: 0 1px 5px rgba(0,0,0,0.1); }
        .job-card h2 { margin: 0 0 10px 0; font-size: 18px; }
        .job-card a { color: #0073e6; text-decoration: none; font-weight: bold; }
        .job-meta { font-size: 14px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>BGGovtJobs - Latest Jobs Alert</h1>
    </div>
    <div class="container">
        <h2>Latest Recruitment Notifications</h2>
        {job_cards}
    </div>
</body>
</html>
"""

job_cards_html = ""
for job in jobs_data:
    title = job.get("title", "Government Job Alert")
    slug = job.get("slug") or re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    vacancies = job.get("vacancies", "Various")
    last_date = job.get("last_date", "N/A")
    
    job_cards_html += f"""
    <div class="job-card">
        <h2><a href="jobs/{slug}.html">{title}</a></h2>
        <p class="job-meta">Total Posts: {vacancies} | Last Date: {last_date}</p>
    </div>
    """

with open("index.html", "w", encoding="utf-8") as f:
    f.write(INDEX_TEMPLATE.format(job_cards=job_cards_html))

print("✅ Homepage (index.html) created successfully!")
