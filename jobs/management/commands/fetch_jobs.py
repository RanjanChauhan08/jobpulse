from django.core.management.base import BaseCommand

from jobs.services.fetcher import fetch_jobs


class Command(BaseCommand):

    help = "Fetch jobs from Jobicy"

    def handle(self, *args, **options):

        self.stdout.write(
            "Fetching jobs..."
        )

        result = fetch_jobs()

        if result["success"]:

            self.stdout.write(
                self.style.SUCCESS(
                    f"{result['message']} "
                    f"Saved: {result['count']}"
                )
            )

        else:

            self.stdout.write(
                self.style.ERROR(
                    result["message"]
                )
            )