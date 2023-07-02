"""
URL configuration for khanto_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from api.views import *

urlpatterns = [
    # django-admin
    path("admin/", admin.site.urls),
    # Home
    path("", HomePageView.as_view(), name='home'),
    # Imóveis
    path("imoveis/", PropertyListAPIView.as_view(), name="property-list"),
    path("imoveis/<int:pk>/", PropertyRetrieveAPIView.as_view(), name="property-retrieve"),
    path("imoveis/create/", PropertyCreateAPIView.as_view(), name="property-create"),
    path("imoveis/update/<int:pk>/", PropertyUpdateAPIView.as_view(), name="property-update"),
    path("imoveis/destroy/<int:pk>/", PropertyDestroyAPIView.as_view(), name="property-destroy"),
    # Anúncios
    path("anuncios/", AdvertisementListAPIView.as_view(), name="advertisement-list"),
    path("anuncios/create/", AdvertisementCreateAPIView.as_view(), name="advertisement-create"),
    path("anuncios/<int:pk>/", AdvertisementDetailAPIView.as_view(), name="advertisement-detail"),
    # Reservas
    path("reservas/", ReservationListAPIView.as_view(), name="reservation-list"),
    path("reservas/create/", ReservationCreateAPIView.as_view(), name="reservation-create"),
    path("reservas/<int:pk>/", ReservationDetailAPIView.as_view(), name="reservation-detail"),
]
