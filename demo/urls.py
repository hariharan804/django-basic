from django.urls import path
from .views import home, view_all_users, delete_user, user_form, user_form_edit
urlpatterns = [
    path('', home, name='home'),
    path('view-all-users/', view_all_users, name='view-all-users'),
    path('delete-user/', delete_user, name='delete-user'),
    path('user-form/', user_form, name='user-form'),
    path('user-form-edit/<str:email>/', user_form_edit, name='user-form-edit'),
]
