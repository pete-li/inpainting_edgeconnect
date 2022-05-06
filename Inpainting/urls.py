from django.urls import path
from django.contrib import admin
 
from . import view
 
urlpatterns = [
    path('login/', view.login),
    path('', view.index),
    path('register/', view.register),
    path('index/', view.index),
    path('download/', view.download),
    path('upload/', view.upload),
    path('inpainting/', view.inpainting), 
    path('logout/', view.logout),
    path('admin/', admin.site.urls),
]