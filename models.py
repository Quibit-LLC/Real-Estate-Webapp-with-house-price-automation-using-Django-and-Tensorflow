from django.db import models
from django.contrib.auth.models import User
#create your models

class House(models.Model):
    name=models.CharField(max_length=255)

    class Meta:  #metadata description for the class name in plural
        ordering = ("name",) #order them by their names
        verbose_name_plural="Houses"

    def __str__(self): #object name to be displayed
        return self.name
    

class Room(models.Model):
    PROPERTY_TYPES = [
        ('Apartment', 'Apartment'),
        ('House', 'House'),
        ('Loft', 'Loft'),
        ('PentHouse', 'PentHouse'),
        ('Villa', 'Villa'),
        ('Studio Apartment', 'Studio Apartment'),
    ]

    AMENITIES_CHOICES = [
        ('Swimming Pool', 'Swimming Pool'),
        ('Gym', 'Gym'),
        ('Parking', 'Parking'),
        ('Internet','Internet'),
        ('CCTVs', 'CCTVs'),
        # Add more amenities choices as needed
    ]

    PROXIMAL_SERVICES_CHOICES = [
        ('School', 'School'),
        ('Hospital', 'Hospital'),
        ('Supermarket', 'Supermarket'),
        ('Restaurant','Restaurant'),
        ('Recreational Park', 'Recreational Park')
        # Add more proximal services choices as needed
    ]
    house=models.ForeignKey(House,related_name="Rooms", on_delete=models.CASCADE, default='')
    amenities_1 = models.CharField(max_length=50, choices=AMENITIES_CHOICES,blank=True, null=True)
    amenities_2 = models.CharField(max_length=50, choices=AMENITIES_CHOICES,blank=True, null=True)
    amenities_3 = models.CharField(max_length=50, choices=AMENITIES_CHOICES, blank=True, null=True)
    amenities_4 = models.CharField(max_length=50, choices=AMENITIES_CHOICES,blank=True, null=True)
    proximal_services_1 = models.CharField(max_length=50, choices=PROXIMAL_SERVICES_CHOICES,blank=True, null=True )
    proximal_services_2 = models.CharField(max_length=50, choices=PROXIMAL_SERVICES_CHOICES, blank=True, null=True)
    proximal_services_3 = models.CharField(max_length=50, choices=PROXIMAL_SERVICES_CHOICES, blank=True, null=True)
    proximal_services_4 = models.CharField(max_length=50, choices=PROXIMAL_SERVICES_CHOICES, blank=True, null=True)
    is_booked = models.BooleanField(default=False)
    location = models.CharField(max_length=100)
    description = models.TextField()
    cover_image = models.ImageField(upload_to="room_images/")
    image1 = models.ImageField(upload_to="room_images/", blank=True, null=True)
    image2 = models.ImageField(upload_to="room_images/", blank=True, null=True)
    image3= models.ImageField(upload_to="room_images/", blank=True, null=True)
    video = models.FileField(upload_to="room_videos/", blank=True, null=True)
    address = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    size = models.IntegerField()
    bedroom = models.IntegerField(default=0, null=True)
    bathroom = models.IntegerField(default=0, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    created_by=models.ForeignKey(User, related_name="Rooms", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # Add other fields for Room as needed

    class Meta:
        verbose_name_plural="Rooms"

    def __str__(self): #object name to be displayed
        return self.name




class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    description = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('room', 'user')

    def __str__(self):
        return f"{self.user}'s {self.get_rating_display()} rating for {self.room}"
    
    
class Agent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="agents/")
    social_url = models.URLField(blank=True)

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='agents', blank=True, null=True)

    # Add other fields for Agent as needed

    def __str__(self):
        return self.name
    
    

class RealEstateAgent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    full_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    years_of_experience = models.PositiveIntegerField()
    license_number = models.CharField(max_length=50)
    previous_companies = models.TextField()
    additional_skills = models.TextField()
    references = models.TextField()
    class Meta:
        verbose_name_plural="RealEstateAgents"
    def __str__(self):
        return self.full_name
    


class HouseData(models.Model):
    area = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    stories = models.IntegerField()
    mainroad = models.IntegerField()
    guestroom = models.IntegerField()
    basement = models.IntegerField()
    hotwaterheating = models.IntegerField()
    airconditioning = models.IntegerField()
    parking = models.IntegerField()
   
    def __str__(self):
        return f'House #{self.id}'


class Payments(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    def __str__(self):
        return self.name
    
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)
    
class Contact(models.Model):
    room=models.ForeignKey(Room, related_name='contacts', on_delete=models.CASCADE)
    members=models.ManyToManyField(User,related_name='contacts')
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-modified_at',)

class ContactMessage(models.Model):
    contact=models.ForeignKey(Contact, related_name='messages', on_delete=models.CASCADE)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,related_name='created_messages', on_delete=models.CASCADE)