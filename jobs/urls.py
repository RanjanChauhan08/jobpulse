from django.urls import path

from .views import (
    job_list,
    refresh_jobs,
)


urlpatterns = [

    path(
        "",
        job_list,
        name="job_list"
    ),

    path(
        "refresh/",
        refresh_jobs,
        name="refresh_jobs"
    ),
]