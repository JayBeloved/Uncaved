from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Dashboard
    path('', views.dashboard_view, name='dashboard'),

    # Showcase URLs
    path('showcase/create/', views.create_showcase_view, name='create_showcase'),
    path('showcase/<int:showcase_id>/edit/', views.edit_showcase_view, name='edit_showcase'),
    path('showcase/<int:showcase_id>/', views.showcase_detail_view, name='showcase_detail'),
    path('showcase/board/', views.showcase_board_view, name='showcase_board'),
    path('showcase/<int:showcase_id>/like/', views.like_showcase, name='like_showcase'),
    path('showcase/my/', views.my_showcases_view, name='my_showcase'),
    # Public profile url
    path('public/profile/<int:user_id>/', views.public_profile_view, name='public_profile'),

    # Community URLs
    path('community/create/', views.create_community_view, name='create_community'),
    path('community/list/', views.community_list_view, name='community_list'),
    path('community/<int:community_id>/', views.community_detail_view, name='community_detail'),
    path('community/<int:community_id>/join/', views.join_community_view, name='join_community'),
    path('community/my/', views.my_communities_view, name='my_communities'),
]