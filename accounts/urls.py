
from app import views as appviews
from . import views
from django.urls import path, include
from postman import urls




urlpatterns = [
#path('',views.index,name='index'),
#path('login/',views.login_view,name='login_view'),
#path('register',views.register,name='register'),
path('<int:user_id>/', views.user_profile, name='user_profile'),
path('messages/', include('postman.urls', namespace='postman')),
path('api/', include('comment.api.urls')),
#path('investor',views.investor,name='investor'),


]