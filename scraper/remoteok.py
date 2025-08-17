import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://remoteok.com/remote-jobs"

def scrape_remoteok():
    jobs = []

    headers = {"User-Agent": "Mozilla/5.0"}  # helps avoid being blocked
    response = requests.get(BASE_URL, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch page")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")

    job_rows = soup.find_all("tr", class_="job")

    for job in job_rows:
        title = job.find("h2", itemprop="title")
        company = job.find("h3", itemprop="name")
        location = job.find("div", class_="location")
        date = job.find("time")
        link = job.find("a", class_="preventLink")

        jobs.append({
            "title": title.text.strip() if title else None,
            "company": company.text.strip() if company else None,
            "location": location.text.strip() if location else "Worldwide",
            "date": date["datetime"] if date and date.has_attr("datetime") else None,
            "link": "https://remoteok.com" + link["href"] if link else None
        })

    return pd.DataFrame(jobs)

if __name__ == "__main__":
    df = scrape_remoteok()
    print(df.head())
