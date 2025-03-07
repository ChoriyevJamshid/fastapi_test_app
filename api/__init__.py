__all__ = (
    "auth_views",
    "users_views",
    "patients_views",
    "hospitalization_views",
    "medical_records_views"
)

from .auth import views as auth_views
from .users import views as users_views
from .patients import views as patients_views
from .hospitalization import views as hospitalization_views
from .medical_records import views as medical_records_views


from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["Api V1"])
router.include_router(auth_views.router, tags=["auth"])
router.include_router(auth_views.router)
router.include_router(users_views.router)
router.include_router(patients_views.router)
router.include_router(hospitalization_views.router)
router.include_router(medical_records_views.router)

