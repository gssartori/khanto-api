from rest_framework import generics
from django.views.generic import TemplateView
from rest_framework.response import Response
from .serializers import PropertySerializer, AdvertisementSerializer, ReservationSerializer
from .models import Property, Advertisement, Reservation
from django.shortcuts import get_object_or_404


### Property serializers ###
# Busca lista de imóveis
class PropertyListAPIView(generics.ListAPIView):
    queryset = Property.available.all()
    serializer_class = PropertySerializer
# Busca individual de imóvel
class PropertyRetrieveAPIView(generics.RetrieveAPIView): 
    """Busca de imóveis por ID.
    
    A classe RetrieveAPIView foi alterada para permitir a busca apenas
    de imóveis disponíveis para visualização da API."""
    serializer_class = PropertySerializer
    
    def get_queryset(self):
        queryset = Property.available.all()
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        
        if instance.is_available:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({'message': 'Informações do imóvel indisponíveis no momento.'})
# Criação de imóvel
class PropertyCreateAPIView(generics.CreateAPIView):
    queryset = Property.available.all()
    serializer_class = PropertySerializer
# Altera um imóvel existente
class PropertyUpdateAPIView(generics.UpdateAPIView):
    queryset = Property.available.all()
    serializer_class = PropertySerializer   
# Deleta um imóvel
class PropertyDestroyAPIView(generics.DestroyAPIView):
    queryset = Property.available.all()
    serializer_class = PropertySerializer


### Advertisement serializers ###
# Buscando lista de anúncios
class AdvertisementListAPIView(generics.ListAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
# Criação de anúncio
class AdvertisementCreateAPIView(generics.CreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
# Busca ou altera um anúncio existente
class AdvertisementDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer


### Reservation serializers ###
# Buscando lista de anúncios
class ReservationListAPIView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
# Criação de anúncio
class ReservationCreateAPIView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
# Busca ou altera um anúncio existente
class ReservationDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer



class HomePageView(TemplateView):
    template_name = 'home.html'