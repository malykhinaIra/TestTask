from django.urls import path
from .views import SiteListView, ProxySiteView, CreateSiteView, StatisticsView

app_name = 'proxy'
urlpatterns = [
    path('', SiteListView.as_view(), name='site_list'),
    path('create/', CreateSiteView.as_view(), name='create_site'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('<str:site_name>/', ProxySiteView.as_view(), name='proxy_site'),
    path('<str:site_name>/<path:site_url>/', ProxySiteView.as_view(), name='proxy_site_with_url'),
]
