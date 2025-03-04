from django.urls import path
from .views import DocumentClassifierView,BulkVerifyViewZip, BulkVerifyFileView

urlpatterns = [
    path('classify/', DocumentClassifierView.as_view(), name='classify'),
    path('bulk/zip', BulkVerifyViewZip.as_view(), name='bulk-zip'),
    path('bulk/', BulkVerifyFileView.as_view(), name='bulk-file')
    # path('bulk/',)
]