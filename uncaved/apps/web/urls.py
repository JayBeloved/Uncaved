from django.urls import path
from .views import index_view, beta_signup_view, beta_thanks_view


app_name = 'web'

urlpatterns = [
    path('', index_view, name='index'),
    path('beta/', beta_signup_view, name='beta_landing'),
    path('beta/thanks/', beta_thanks_view, name='beta_thanks'),
]