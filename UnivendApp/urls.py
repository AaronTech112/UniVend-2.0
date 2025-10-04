from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('home/', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_view, name='logout_user'),
    path('profile/', views.profile, name='profile'),
    path('kyc/', views.kyc, name='kyc'),
    path('explore/', views.explore, name='explore'),
    path('add-listing/', views.add_listing, name='add-listing'),
    path('product/<int:listing_id>/', views.product_detail, name='product-detail'),
    path('product/<int:listing_id>/buy/', views.buy_now, name='buy-now'),
    path('chat/', views.chat_list, name='chat-list'),
    path('chat/<int:user_id>/', views.chat_detail, name='chat-detail'),
    path('chat/<int:user_id>/<int:listing_id>/', views.chat_detail, name='chat-detail'),
    path('search/', views.search, name='search'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('settings/', views.settings, name='settings'),
    path('update_notifications/', views.update_notifications, name='update_notifications'),
]