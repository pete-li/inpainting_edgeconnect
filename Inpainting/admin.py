from django.contrib import admin

# Register your models here.
from Inpainting.models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','pwd','img_type','upload_path','mask_path','edge_path','masked_path','result_path','ticket','create_time')


admin.site.register(User,UserAdmin)
