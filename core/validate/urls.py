from django.urls import path
from .views import VerifyView, OCRLabelingBatchView, MatchView, FinalView

urlpatterns = [
    path('', VerifyView.as_view(), name='verify'),
    path('bulk/', OCRLabelingBatchView.as_view(), name='final-bulk0.'),
    path('check/<int:app_id>', MatchView.as_view(), name='check'),
    path("match/",FinalView.as_view(),name='match')
]