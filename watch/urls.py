from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('watch/<id>',views.watch,name='watch'),
    path('comments/watch/<title>',views.comments),
    path('add_video/',views.add_video,name='add_video'),
    path('update_profile/<id>',views.update_profile),
    path('reply/<id>',views.reply)
]

