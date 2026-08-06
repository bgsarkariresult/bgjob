import json

with open("data/jobs.json", "r", encoding="utf-8") as f:
    jobs = json.load(f)

with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()

for job in jobs:
    content = template.replace("{{JOB_TITLE}}", job["title"])
    content = content.replace("{{TOTAL_VACANCY}}", str(job["vacancy"]))
    # अन्य फ़ील्ड्स रिप्लेस करें...
    
    file_name = f"jobs/{job['slug']}.html"
    with open(file_name, "w", encoding="utf-8") as out:
        out.write(content)

print("All Job Pages Generated Successfully!")
