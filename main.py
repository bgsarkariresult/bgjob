import asyncio
import base64
from datetime import datetime, timezone
import json
import logging
import os
import re

from bs4 import BeautifulSoup
from g4f.client import Client
import requests
from telegram import Bot

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
REPO_OWNER = "गढ़वालभवेश2002-dot"
REPO_NAME = "bgjob"
JSON_FILE_PATH = "data/jobs.json"
SITE_BASE_URL = "https://bgsarkariresult.github.io/bgjob"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "@bglarenup")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0.0.0 Safari/537.36"
}

def push_to_github_api(updated_jobs_list, commit_message):
    if not GITHUB_TOKEN:
        logging.warning("⚠️ GITHUB_TOKEN nahi mila, GitHub Push skip ho gaya.")
        return False

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{JSON_FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    sha = None
    get_res = requests.get(url, headers=headers)
    if get_res.status_code == 200:
        sha = get_res.json().get("sha")

    json_str = json.dumps(updated_jobs_list, ensure_ascii=False, indent=2)
    encoded_content = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")

    payload = {
        "message": commit_message,
        "content": encoded_content,
        "branch": "main"
    }
    if sha:
        payload["sha"] = sha

    put_res = requests.put(url, headers=headers, json=payload)
    return put_res.status_code in [200, 201]

async def process_and_publish(job_source_url):
    logging.info(f"Processing URL: {job_source_url}")
