from django.contrib import admin

from library.models.users import User
from library.models.books import Book, UserBook

# Register your models here.
admin.site.register(Book)
admin.site.register(UserBook)
admin.site.register(User)