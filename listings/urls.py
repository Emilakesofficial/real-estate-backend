from django.urls import path
from .views import *

urlpatterns = [
    path('create/property/', MyPropertyDetailView.as_view()),
    path('get/properties/', PropertyView.as_view()),
    path('get/my/properties/', MyPropertiesView().as_view()),
    path('get/property/<int:pk>/', MyPropertyDetailView.as_view()),
    path('update/property/<int:pk>/', MyPropertyDetailView.as_view()),
    path('delete/property/<int:pk>/', MyPropertyDetailView.as_view()),
    path('restore/property/<int:pk>/', AdminPropertyView.as_view()),
    path('delete/property/<int:pk>/', AdminPropertyView.as_view()),
    path('enquire/<int:property_id>/', MakeEnquiryView.as_view()),
    path('reply/enquiry/<int:enquiry_id>/', EnquiryReplyView.as_view()),
    path('view/enquiries/', AgentEnquiriesView.as_view()),
    path('view/response/renter/buyer/', UserEnquiriesView.as_view()),
]