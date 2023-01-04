
from app import views as appviews
from . import views
from django.urls import path, include




urlpatterns = [

path('<int:user_id>/', views.user_profile, name='user_profile'),
path('messages/', include('postman.urls', namespace='postman')),
path('api/', include('comment.api.urls')),
]