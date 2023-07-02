from django.contrib import admin

from django.contrib import admin

from .models import Property, Advertisement, Reservation

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = [
        'property_code',
        'guest_limit',
        'number_of_bathrooms',
        'accepts_animals',
        'cleaning_fee',
        'activation_date',
        'is_available',
        'created',
        'modified'
    ]
    populated_fields = {"slug": ("property_code",)} # Preenche slug de acordo com o o código do imóvel

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['platform', 'platform_fee', 'property', 'created', 'modified']
    list_filter = ['platform', 'created', 'modified']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        'reservation_code',
        'check_in_date',
        'check_out_date',
        'total_price',
        'comment',
        'guest_count',
        'advertisement',
        'created',
        'modified']
    list_filter = ['total_price', 'guest_count', 'created', 'modified']
    list_editable = []
    populated_fields = {"slug": ("mint_address",)}