from django.urls import path
from django.contrib import admin
from rest_framework import routers
from trading import views as trading_views
from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()
router.register(r'trade', trading_views.TradeViewSet, basename='trade')
router.register(r'summary', trading_views.SummaryViewSet, basename='summary')


urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('sign-in/', obtain_auth_token), #gives us access to token auth
    path('sign-up/', trading_views.UserRegister.as_view(), name='sign-up'),
]