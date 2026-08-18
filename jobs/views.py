from django.contrib import messages
from django.shortcuts import redirect, render

from .models import Job
from .services.fetcher import fetch_jobs


def job_list(request):

    search = request.GET.get(
        "search",
        ""
    ).strip()

    jobs = Job.objects.all()

    if search:

        jobs = jobs.filter(
            title__icontains=search
        ) | jobs.filter(
            company__icontains=search
        ) | jobs.filter(
            location__icontains=search
        )

    jobs = jobs.order_by(
        "-published_at",
        "-fetched_at"
    )

    return render(
        request,
        "jobs/index.html",
        {
            "jobs": jobs,
            "search": search,
        }
    )


def refresh_jobs(request):

    if request.method != "POST":

        return redirect("job_list")

    result = fetch_jobs()

    if result["success"]:

        messages.success(
            request,
            f"Fetched {result['count']} jobs."
        )

    else:

        messages.error(
            request,
            "Job source is temporarily unavailable. "
            "Showing cached results."
        )

    return redirect("job_list")