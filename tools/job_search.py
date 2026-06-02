import requests
from config import ADZUNA_APP_ID, ADZUNA_APP_KEY

def remote_job_search(job_title, location=None, experience_level=None, job_type=None, salary_min=None, num_results=5):
    try:
        query = job_title
        if experience_level:
            query += f" {experience_level}"
        if job_type:
            query += f" {job_type}"

        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "what": query,
            "results_per_page": num_results
        }

        response = requests.get(
            "https://api.adzuna.com/v1/api/jobs/us/search/1",
            params=params,
            timeout=10
        )

        data = response.json()
        jobs = []

        for job in data.get("results", []):
            jobs.append({
                "title":       job.get("title"),
                "company":     job.get("company", {}).get("display_name"),
                "location":    job.get("location", {}).get("display_name"),
                "salary_min":  job.get("salary_min"),
                "salary_max":  job.get("salary_max"),
                "description": job.get("description", "")[:300],
                "apply_url":   job.get("redirect_url")
            })

        return jobs

    except requests.exceptions.ReadTimeout:
        return {"error": "Timeout — server not responding"}
    except requests.exceptions.ConnectionError:
        return {"error": "Connection error — can't reach server"}
    except Exception as e:
        return {"error": str(e)}