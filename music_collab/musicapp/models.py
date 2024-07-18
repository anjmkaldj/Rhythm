from django.db import models

# Create your models here.
class UserReg(models.Model):
    userid=models.IntegerField()
    fn=models.CharField(max_length=20)
    em=models.CharField(max_length=30)
    ph=models.IntegerField()
    pro_pic=models.ImageField(upload_to='images/')
    password=models.CharField(max_length=20)


class karoakedetails(models.Model):

    song_name=models.CharField(max_length=20)
    price=models.IntegerField()
    image=models.ImageField(upload_to='images/')
    des=models.CharField(max_length=200)
    category=models.CharField(max_length=30)
    mp3_file = models.FileField(upload_to='mp3s/', null=True, blank=True)
    def __str__(self):
        return self.song_name

class CartItem(models.Model):
    userid=models.IntegerField()
    item=models.ForeignKey(karoakedetails, on_delete=models.CASCADE)



class Wishlist(models.Model):
    userid=models.IntegerField()
    item=models.ForeignKey(karoakedetails, on_delete=models.CASCADE)

class order(models.Model):
    userdetails=models.ForeignKey(UserReg,on_delete=models.CASCADE)
    pictures=models.ImageField(upload_to='images/')
    ordered_date=models.DateField()


class OrderItem(models.Model):
    order=models.ForeignKey(order,on_delete=models.CASCADE)
    order_pic=models.ImageField()
    song_name=models.CharField(max_length=20)
    price=models.IntegerField()




# models.py

from django.db import models

from django.db import models

class AudioRecording(models.Model):
    background_file = models.FileField(upload_to='karaoke/')
    voice_recording = models.FileField(upload_to='recordings/')
    combined_file = models.FileField(upload_to='combined/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
