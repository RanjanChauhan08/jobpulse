from django.db import models


class Job(models.Model):

    external_id = models.CharField(
        max_length=255,
        unique=True
    )

    title = models.CharField(
        max_length=255
    )

    company = models.CharField(
        max_length=255
    )

    location = models.CharField(
        max_length=255,
        blank=True
    )

    job_type = models.CharField(
        max_length=100,
        blank=True
    )

    category = models.CharField(
        max_length=150,
        blank=True
    )

    salary = models.CharField(
        max_length=255,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    source_url = models.URLField()

    source = models.CharField(
        max_length=100,
        default="Jobicy"
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True
    )

    fetched_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.title} - {self.company}"