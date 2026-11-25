from django.shortcuts import render

from .projects import PORTAL_PROJECTS


def home_view(request):
    return render(
        request,
        "portal/home.html",
        {"projects": PORTAL_PROJECTS},
    )
