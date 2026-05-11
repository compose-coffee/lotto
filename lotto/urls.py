from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # 메인
    path('buy/', views.buy_lotto, name='buy_lotto'), # 구매
    path('check/', views.check_win, name='check_win'),
]