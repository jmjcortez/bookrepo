from rest_framework import serializers

from library.models.books import Book, UserBook
from library.serializers.users_serializer import UserSerializer


class BookSerializer(serializers.ModelSerializer):

  class Meta:
    model = Book

    fields = (
      'title', 'author', 'isbn',
    )


class UserBookSerializer(serializers.ModelSerializer):

  class Meta:
    model = UserBook
    fields = (
      'book', 'user', 'timestamp',
    )

  def create(self, validated_data):
    return UserBook.objects.create(book=validated_data['book'], user=validated_data['user'])