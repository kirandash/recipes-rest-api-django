from django.urls import path

from user import views

# app name: to identify app using which the url is created. For reverse
app_name = 'user'

urlpatterns = [
    # user/create endpoint, name is used to identify this url for reverse
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
