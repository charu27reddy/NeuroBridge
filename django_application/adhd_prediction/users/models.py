from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Profile(models.Model): # why models.Model is used ?
    user=models.OneToOneField(User,on_delete=models.CASCADE)#what is cascade?
    #what is this user excatly is it an element or attribute 
    image=models.ImageField(default='default.jpeg',upload_to='profile_pics')


    #__str__
    def __str__(self):
        return f'{self.user.username} Profile'
    #for this to work pillow has to be installed 
    #what is pillow in python why should it be installed 
    
    #resizing of the image
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img=Image.open(self.image.path)
        if img.height > 300 or img.width >300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

