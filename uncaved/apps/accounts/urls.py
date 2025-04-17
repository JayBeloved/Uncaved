from django.urls import path
from .views import login_view, logout_view, sign_up, view_profile, edit_profile, update_profile_image

app_name = 'accounts'
urlpatterns = [
    path('signin/', login_view, name='signin'),
    path('logout/', logout_view, name='logout'),
    path('sign_up/', sign_up, name='signup'),
    path('profile/', view_profile, name='view_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/update-image/', update_profile_image, name='update_profile_image')
]