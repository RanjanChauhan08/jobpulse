import time
import requests

from django.utils.dateparse import parse_datetime

from jobs.models import Job


API_URL = "https://jobicy.com/api/v2/remote-jobs"


def fetch_jobs():

    max_attempts = 3

    for attempt in range(max_attempts):

        try:
            response = requests.get(
                API_URL,
                params={
                    "count": 20,
                    "industry": "engineering",
                },
                timeout=10,
            )

            # Handle rate limiting
            if response.status_code == 429:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
                continue

            response.raise_for_status()

            data = response.json()

            jobs = data.get("jobs", [])

            saved_count = 0

            for item in jobs:

                # Get unique job ID
                external_id = (
                    item.get("id")
                    or item.get("url")
                )

                if not external_id:
                    continue

                # Parse published date
                published_at = None

                published_value = item.get("pubDate")

                if published_value:
                    published_at = parse_datetime(
                        published_value
                    )

                # -------------------------
                # Salary handling
                # -------------------------

                salary_min = item.get("salaryMin")
                salary_max = item.get("salaryMax")
                salary_currency = item.get(
                    "salaryCurrency",
                    ""
                )

                if salary_min and salary_max:
                    salary = (
                        f"{salary_min} - "
                        f"{salary_max} "
                        f"{salary_currency}"
                    ).strip()
                elif salary_min:
                    salary = (
                        f"{salary_min} "
                        f"{salary_currency}"
                    ).strip()
                elif salary_max:
                    salary = (
                        f"{salary_max} "
                        f"{salary_currency}"
                    ).strip()
                else:
                    salary = "Not disclosed"

                # -------------------------
                # Save / update job
                # -------------------------

                Job.objects.update_or_create(

                    external_id=external_id,

                    defaults={

                        "title": item.get(
                            "jobTitle",
                            "Untitled job"
                        ),

                        "company": item.get(
                            "companyName",
                            "Unknown company"
                        ),

                        "location": item.get(
                            "jobGeo",
                            ""
                        ),

                        "job_type": ", ".join(
                            item.get("jobType", [])
                        ),

                        "category": ", ".join(
                            item.get("jobIndustry", [])
                        ),

                        "salary": salary,

                        "description": item.get(
                            "jobDescription",
                            ""
                        ),

                        "source_url": item.get(
                            "url",
                            ""
                        ),

                        "source": "Jobicy",

                        "published_at": published_at,
                    }
                )

                saved_count += 1

            return {
                "success": True,
                "count": saved_count,
                "message": "Jobs fetched successfully."
            }

        except requests.RequestException as error:

            if attempt == max_attempts - 1:

                return {
                    "success": False,
                    "count": 0,
                    "message": str(error),
                }

            wait_time = 2 ** attempt

            time.sleep(wait_time)

    return {
        "success": False,
        "count": 0,
        "message": "Unable to fetch jobs."
    }