from django.urls import path
from .views import *

urlpatterns = [
    path('create/', ChitFundCreateView.as_view(), name='create-chit'),
    path('hosted/', HostedFundsView.as_view(), name='hosted-funds'),
    path('joined/', JoinedFundsView.as_view(), name='joined-funds'),
    path('start/<int:pk>/', StartChitFundView.as_view(), name='start-chit'),
    path('join/', JoinChitFundView.as_view(), name='join-chit-fund'),
    path('home/', UserHomeView.as_view(), name='user-home'),
]
