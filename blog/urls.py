from django.urls import path
from blog.views import index, about


app_name = 'blog'
urlpatterns = [
    # path('about/contacts', about, name='about'),
    path('about/', about, name='about'), #Более специфические маршруты выше, чем более общие
    path('', index, name='index'),
]