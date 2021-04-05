from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import datetime
from PIL import Image
from django.db.models import CharField, Model

class Users_Master(models.Model):
    Users_unique_id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=30)
    Surname = models.CharField(max_length=30)
    Country = models.CharField(max_length=30)
    State = models.CharField(max_length=30)
    City = models.CharField(max_length=30)
    User_Log = models.DateTimeField(auto_now_add=True , editable= False)
    User_last_Login = models.CharField(max_length=100)
    User_authentication = models.CharField(max_length=10)
    User_tickets = models.CharField(max_length=1000)
    liked_events = models.CharField(max_length=30)
    Contact_Number = models.CharField(max_length=15, default=0)
    Email = models.CharField(max_length = 30, default='-')
    def __str__(self):
        return str(self.Users_unique_id)
# Create your models here.
class Entry(models.Model):
    user_id = models.ForeignKey('Users_Master', on_delete=models.CASCADE, db_column='user_id')
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200, default='1000', editable=False)

def unique_rand():
        while True:
            Event_Unique_Id = int(User.objects.make_random_password(length=4, allowed_chars='123456789'))
            if not Events_Master.objects.filter( Event_Unique_Id = Event_Unique_Id).exists():
                return Event_Unique_Id


class Events_Master(models.Model):
    Event_Unique_Id = models.CharField(max_length=8, unique=True, default=unique_rand)
    Event_By = models.CharField(max_length=100)
    Event_Name = models.CharField(max_length=500)
    Event_Type = models.CharField(max_length =20)
    Event_Organiser = models.CharField(max_length=50)
    Organiser_Unique_Id = models.IntegerField(max_length= 10, default=0)
    Artist_Name = models.CharField(max_length=50)
    Artists_Unique_Id = models.IntegerField(max_length = 10, default=0)
    Event_Venue = models.CharField(max_length=50)
    Venue_Unique_id = models.CharField(max_length=100)
    Event_Authentication= models.CharField(max_length=10, default= False)
    Event_Status = models.CharField(max_length= 10, default="Inactive")
    Event_Description = models.TextField(max_length =1000)
    Event_Poster = models.ImageField()
    Event_Date = models.CharField(default=datetime.date.today, max_length=100)
    Event_Time = models.TimeField(default=0, max_length=20)
    Event_Registration_Time = models.DateTimeField(auto_now_add=True, editable=False)
    Event_Price = models.IntegerField(max_length=6)
    Event_Capacity = models.IntegerField(max_length=6)
    Event_Tickets_Sold = models.IntegerField(max_length=6,default=0)
    Event_Seats_Sold = models.CharField(max_length = 1000, default="")
    Rows = models.IntegerField(max_length=2, default=12)
    Columns = models.IntegerField(max_length=2,default=12)
    Blocked_Seats = models.CharField(max_length = 1000, default=0)


    def save(self):
        super().save()  # saving image first

        img = Image.open(self.Event_Poster.path) # Open image using self

        new_img = (300, 300)
        img.thumbnail(new_img)
        img.save(self.Event_Poster.path)

    def get_absolute_url(self):
        return reverse('details', kwargs = {'event_id':self.Event_Unique_Id})

    def __str__(self):
        return self.Event_Unique_Id
class Venue_Master(models.Model):
    Venue_Unique_Id = models.CharField(max_length=20)
    Venue_name = models.CharField(max_length = 20)
    Venue_Layout_Path = models.CharField(max_length=200)
    Venue_Seats = models.IntegerField(max_length=8)
    Venue_Facilities = models.CharField(max_length=500)
    Events_hosted = models.IntegerField(max_length = 6)
    Venue_Rating = models.IntegerField(max_length = 10)
    Venue_address = models.CharField(max_length=100)
    Venue_City = models.CharField(max_length=20)
    Venue_State = models.CharField(max_length=100)
    Venue_Status = models.CharField(max_length=100)
    Venue_Pics_Paths = models.CharField(max_length = 110)

class Organiser_master(models.Model):
    Organiser_Unique_id = models.CharField(max_length=10)
    Organiser_Points = models.CharField(max_length=2)
    Organiser_Name = models.CharField(max_length=100)
    Organised_Events_id = models.CharField(max_length=100)
    Organiser_Connected_with_Artists = models.CharField(max_length = 100)
    Organiser_Authenication = models.CharField(max_length=10)
    Organiser_Rating = models.IntegerField(max_length=10)

class Artists_Master(models.Model):
    Artist_Unique_Id = models.CharField(max_length=10)
    Artist_Name = models.CharField(max_length=100)
    Artist_location = models.CharField(max_length=10)
    Artist_Birthday = models.CharField(max_length=10)
    Artist_Done_Events = models.CharField(max_length=1000)
    Artist_Registration_Date_time = models.CharField(max_length=100)
    Artist_Authentication = models.CharField(max_length=100)
    Artist_points = models.IntegerField(max_length=10)
    Artist_authenticated = models.CharField(max_length=10)
    Artist_type = models.CharField(max_length=100)
    Artist_field = models.CharField(max_length=100)
    Artist_ratings = models.IntegerField(max_length=10)
    age = models.IntegerField(max_length=2)


class Ticket_master(models.Model):
    Event_Name = models.CharField(max_length=100)
    Event_Unique_Id = models.IntegerField(max_length=10)
    User_Name = models.CharField(max_length=100)
    User_Unique_id = models.IntegerField(max_length=10)
    Organiser_Unique_Id = models.IntegerField(max_length=10)
    Number_of_tickets = models.IntegerField(max_length = 10)
    Seat_no = models.CharField(max_length=100)
    Payment_Method = models.CharField(max_length=10)
    Payment_Reciept_Path = models.CharField(max_length=10)
    Payment_Status = models.CharField(max_length=10)
    Offers_Applied = models.CharField(max_length=10)
    Payment_Amount = models.IntegerField()
    Ticket_Registration_Time = models.DateTimeField(auto_now_add=True, editable=False)
class Artist_Registar(models.Model):
    Unique_Id_Generation = models.IntegerField(max_length = 10) #Id will generate from here
    #Other form requirements
class End_user_registar(models.Model):
    Unique_Id_Generation = models.IntegerField(max_length=10) #id will generate from here
    #other forms requirement
    #password
    #email
    #etc
class Organiser_Registar(models.Model):
    Unique_Id_Generation = models.IntegerField(max_length=10)  # id will generate from here
    # other forms requirement
    # password
    # email
    # etc

class Event_Registar(models.Model):
     organiser_name = models.CharField(max_length=10)#When organiser creates an event
     event_name = models.CharField(max_length=100)
     city = models.CharField(max_length=10)
     state = models.CharField(max_length=10)
     artists = models.CharField(max_length=100) #iF there are any artist
     venue = models.CharField(max_length =100) #if venue is not in the list provided
     event_poster = models.FileField() #Path
     capacity = models.CharField(max_length=100)
     date = models.DateField(max_length=20)
     time = models.TimeField(max_length=20)
     authentication = models.CharField(max_length=10,default="NO")
     registration_time = models.DateTimeField(auto_now_add=True, editable=False)

     def get_absolute_url(self):
         return reverse('details', kwargs={'pk': self.pk})



     #MOre to come




from django.db import models

# Create your models here.
