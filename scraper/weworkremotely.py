import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://weworkremotely.com/remote-jobs"

def scrape_weworkremotely():
    jobs = []

    response = requests.get(BASE_URL)
    if response.status_code != 200:
        print("Failed to fetch page")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")

    job_sections = soup.find_all("section", class_="jobs")

    for section in job_sections:
        listings = section.find_all("li", class_="feature")
        for job in listings:
            title = job.find("span", class_="title").text.strip() if job.find("span", class_="title") else None
            company = job.find("span", class_="company").text.strip() if job.find("span", class_="company") else None
            region = job.find("span", class_="region company").text.strip() if job.find("span", class_="region company") else "Worldwide"
            date = job.find("time").text.strip() if job.find("time") else None
            link = "https://weworkremotely.com" + job.find("a")["href"] if job.find("a") else None

            jobs.append({
                "title": title,
                "company": company,
                "location": region,
                "date": date,
                "link": link
            })

    return pd.DataFrame(jobs)

if __name__ == "__main__":
    df = scrape_weworkremotely()
    print(df.head())
