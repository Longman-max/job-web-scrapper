from . import get_all_jobs

if __name__ == "__main__":
    jobs = get_all_jobs()
    print(jobs.head(10))
