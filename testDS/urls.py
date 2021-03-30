"""testDS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tiaApp.views import indicators, getDepartments, top5, departmentTotalEarnings, timeLine

urlpatterns = [
    # path('departments/',index),
    path('indicators/', indicators),
    path('departments/', getDepartments),
    path('top_5/<str:depart>/',top5),
    path('top_5/',top5),
    path('earnings/',departmentTotalEarnings),
    path('timeline/',timeLine),
    path('admin/', admin.site.urls),
]
