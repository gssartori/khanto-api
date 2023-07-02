from model_utils.models import TimeStampedModel
from django.db import models
from django.core.exceptions import ValidationError


class AvailableManager(models.Manager):
    """Classe de gerenciamento de modelos.
    
    Neste projeto, está sendo utilizada para retornar nas consultas apenas
    objetos com a condição is_available=True, o que facilita o manuseio de
    Imóveis 'disponíveis' ou em 'operação' no gerenciamento de dados."""
    def get_queryset(self):
        return super().get_queryset().filter(is_available=True)


class Property(TimeStampedModel):
    """."""
    property_code = models.CharField(max_length=30, unique=True)
    guest_limit = models.PositiveIntegerField()
    number_of_bathrooms = models.PositiveIntegerField()
    accepts_animals = models.BooleanField()
    cleaning_fee = models.DecimalField(max_digits=6, decimal_places=2)
    activation_date = models.DateField()
    is_available = models.BooleanField(default=True)
    
    objects = models.Manager()
    available = AvailableManager()
    
    class Meta():
        verbose_name = 'Imóvel'
        verbose_name_plural = 'Imóveis'
    

PLATFORMS = (('Ab', 'AirBnb'), ('Bk', 'Booking.com'), ('Ss', 'Skyscanner'))
class Advertisement(TimeStampedModel):
    """."""
    platform = models.CharField(max_length=100, choices=PLATFORMS)
    platform_fee = models.DecimalField(max_digits=8, decimal_places=2)
    # ForeignKey
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    
    class Meta():
        ordering = ('platform',)
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        
    def __str__(self):
        return self.platform
    
class Reservation(TimeStampedModel):
    """."""
    reservation_code = models.CharField(max_length=100, unique=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField( max_digits=8, decimal_places=2)
    comment = models.TextField( blank=True)
    guest_count = models.PositiveIntegerField()
    # ForeignKey
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    
    class Meta():
        verbose_name = 'Reserva'

    def clean(self):
        if self.check_in_date >= self.check_out_date:
            raise ValidationError("A data de check-in deve ser anterior à data de check-out")
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)