from django.urls import path
from .views import upload_resume, analysis_history, analysis_detail, analysis_api, analysis_detail_api

urlpatterns = [
    path("", upload_resume, name="upload_resume"),
    path("history/", analysis_history, name="analysis_history"),
    path("history/<int:analysis_id>/", analysis_detail, name="analysis_detail"),
    path("api/analyses/", analysis_api, name="analysis_api"),
    path("api/analyses/<int:analysis_id>/", analysis_detail_api, name="analysis_detail_api"),
]
