from django.urls import path
from .views import OCRLabelingView, OCRLabelingBatchView

urlpatterns = [
    path('ocr/', OCRLabelingView.as_view(), name='ocr'),
    path('bulk/',OCRLabelingBatchView.as_view(), name='bulk')
]