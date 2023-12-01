from django.contrib import admin
from .models import House, Room, Review, Agent,RealEstateAgent, HouseData, Payments, Contact, ContactMessage

# Register your models here.
admin.site.register(House)
admin.site.register(Room)
admin.site.register(Review)
admin.site.register(Agent)
admin.site.register(RealEstateAgent)
admin.site.register(Contact)
admin.site.register(ContactMessage)
admin.site.register(HouseData)
admin.site.register(Payments)