from django.contrib import admin

# Register your models here.

from .models import Post,Category,Tag

class postAdmin(admin.ModelAdmin):
    list_display = ['title','created_time','modified_time','category','author']

admin.site.register(Category)
admin.site.register(Post,postAdmin)
admin.site.register(Tag)
