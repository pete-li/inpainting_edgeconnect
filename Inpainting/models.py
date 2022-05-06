from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    pwd = models.CharField(max_length=255)
    img_type = models.IntegerField(default=1)
    upload_path = models.CharField(max_length=255,default='/static/media/upload.jpg')
    mask_path = models.CharField(max_length=255,default='/static/media/mask.png')
    edge_path = models.CharField(max_length=255,default='/static/media/edge.jpg')
    masked_path = models.CharField(max_length=255,default='/static/media/masked.jpg')
    result_path = models.CharField(max_length=255,default='/static/media/result.jpg')
    ticket = models.CharField(max_length=255,default='')
    create_time = models.DateTimeField(default=timezone.now)




