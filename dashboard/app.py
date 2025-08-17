import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import pandas as pd
from scraper import get_all_jobs

st.set_page_config(page_title="Job Web Scrapper", layout="wide")

st.title("💼 Job Aggregator Web Scraper")

# Fetch job data
st.info("Fetching jobs... please wait.")
jobs_df = get_all_jobs()

if jobs_df.empty:
    st.error("No jobs found. Try again later.")
else:
    st.success(f"Found {len(jobs_df)} job listings!")

    st.sidebar.header("Filters")

    keyword = st.sidebar.text_input("Search by keyword")

    locations = jobs_df["location"].dropna().unique().tolist()
    location_filter = st.sidebar.multiselect("Filter by location", locations)

    companies = jobs_df["company"].dropna().unique().tolist()
    company_filter = st.sidebar.multiselect("Filter by company", companies)

    # Apply filters
    filtered_df = jobs_df.copy()

    if keyword:
        filtered_df = filtered_df[filtered_df["title"].str.contains(keyword, case=False, na=False)]

    if location_filter:
        filtered_df = filtered_df[filtered_df["location"].isin(location_filter)]

    if company_filter:
        filtered_df = filtered_df[filtered_df["company"].isin(company_filter)]

    st.dataframe(filtered_df, use_container_width=True)

    if not filtered_df.empty:
        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="jobs.csv",
            mime="text/csv",
        )
