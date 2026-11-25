import os

# Central registry for clinical applications.
#
# Add future applications here without redesigning the portal.

NEUROLOGY_URL = os.getenv("NEUROLOGY_URL", "/neurology/accounts/login/")
BREAST_REGISTRY_URL = os.getenv("BREAST_REGISTRY_URL", "/login/?next=/app/")
RADIOLOGY_URL = os.getenv("RADIOLOGY_URL", "/radiology/")


PORTAL_PROJECTS = [
    {
        "key": "neurology",
        "name": "Neurology Emergency Department",
        "short_name": "Neurology ED",
        "description": (
            "Emergency neurological assessment, patient encounters, "
            "clinical documentation and investigations."
        ),
        "image": "portal/images/neurology_brain_art.png",
        "url": NEUROLOGY_URL,
        "theme": "neurology",
        "status": "active",
        "button": "Enter Neurology ED",
    },
    {
        "key": "breast-registry",
        "name": "Breast Cancer Registry",
        "short_name": "Breast Cancer Registry",
        "description": (
            "Patient registration, tumor records, clinical episodes, "
            "treatment follow-up, analytics and reports."
        ),
        "image": "portal/images/breast_registry_art.png",
        "url": BREAST_REGISTRY_URL,
        "theme": "breast",
        "status": "active",
        "button": "Enter Breast Cancer Registry",
    },
    {
        "key": "radiology",
        "name": "Radiology",
        "short_name": "Radiology",
        "description": "Clinical reports and imaging studies.",
        "image": "portal/images/radiology_art.png",
        "url": RADIOLOGY_URL,
        "theme": "radiology",
        "status": "active",
        "button": "Enter Radiology",
    },
]
