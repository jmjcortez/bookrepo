from django.db import models

from library.models.users import User


class Book(models.Model):
  title = models.CharField(max_length=100)
  author = models.CharField(max_length=100)

  isbn = models.CharField(max_length=13)


class UserBook(models.Model):
  user = models.ForeignKey(
    User,
    on_delete=models.PROTECT,
    related_name="user_books"
  )

  book = models.ForeignKey(
    Book,
    on_delete=models.PROTECT,
    related_name="book_profiles"
  )

  timestamp = models.DateTimeField(auto_now=True)

  class Meta:
    unique_together = ("user", "book")
