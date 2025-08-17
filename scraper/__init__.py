import pandas as pd
from .weworkremotely import scrape_weworkremotely
from .remoteok import scrape_remoteok

def get_all_jobs():
    df1 = scrape_weworkremotely()
    df2 = scrape_remoteok()

    # Combine both DataFrames
    all_jobs = pd.concat([df1, df2], ignore_index=True)

    # Drop duplicates (same title+company+location)
    all_jobs.drop_duplicates(subset=["title", "company", "location"], inplace=True)

    # Sort by date if available
    if "date" in all_jobs.columns:
        all_jobs = all_jobs.sort_values(by="date", ascending=False)

    return all_jobs

if __name__ == "__main__":
    jobs = get_all_jobs()
    print(jobs.head(10))
