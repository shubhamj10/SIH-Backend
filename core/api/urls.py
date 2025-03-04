from django.urls import path
from .views import ApplicationListView, ApplicationCreateView,  ApplicationByIdView, ApplicationUpdateView, ApplicationDeleteView

urlpatterns = [
    path('applications/', ApplicationListView.as_view(), name='application-list'),
    path('applications/create', ApplicationCreateView.as_view(), name='application-create'),
    path('applications/<int:app_id>', ApplicationByIdView.as_view(), name='application-by-id'),
    path('applications/update/<int:app_id>', ApplicationUpdateView.as_view(), name='application-update'),
    path('applications/delete/<int:app_id>', ApplicationDeleteView.as_view(), name='application-delete'),
]

