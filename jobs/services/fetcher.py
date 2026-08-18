import time
import requests

from django.utils.dateparse import parse_datetime
from django.utils import timezone

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

            if response.status_code == 429:

                wait_time = 2 ** attempt

                time.sleep(wait_time)

                continue

            response.raise_for_status()

            data = response.json()

            jobs = data.get("jobs", [])

            saved_count = 0

            for item in jobs:

                external_id = (
                    item.get("id")
                    or item.get("url")
                )

                if not external_id:
                    continue

                published_at = None

                published_value = item.get(
                    "pubDate"
                )

                if published_value:

                    published_at = parse_datetime(
                        published_value
                    )

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

                        "job_type": item.get(
                            "jobType",
                            ""
                        ),

                        "category": item.get(
                            "jobIndustry",
                            ""
                        ),

                        "salary": item.get(
                            "annualSalaryMin",
                            ""
                        ),

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