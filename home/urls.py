from django.conf.urls import url, include
from django.views.static import serve
from django.conf import settings
from home import views



urlpatterns = [
    url('/main/', views.home_page),
    url('/detail/', views.detail_page),
    url('/auth/', views.auth_page),
    # url(r'media/(?<Path>.*)', serve, {'document_root':settings.MEDIA_ROOT})
]
