import json
from urllib.request import urlopen
from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.http import HttpResponse

from library.serializers.users_serializer import UserSerializer
from library.serializers.books_serializer import UserBookSerializer, BookSerializer
from library.models.users import User
from library.models.books import Book, UserBook


class BooksViewset(ViewSet):

  permission_classes = []
  authentication_classes = []

  def list(self, request):

    email = request.query_params.get('email', None)
    days = request.query_params.get('days', 0)
    
    if not email:
      Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
      user = User.objects.get(email=email)
    except User.DoesNotExist:
      return Response(status=status.HTTP_401_UNAUTHORIZED)

    if days == 0:
      user_book_list = UserBook.objects.filter(user=user).values_list('book', flat=True)
    else:
      user_book_list = UserBook.objects.filter(user=user, timestamp__gte=datetime.now()-timedelta(days=int(days))).values_list('book', flat=True)

    books = Book.objects.filter(id__in=user_book_list)

    serializer = BookSerializer(books, many=True)

    return Response(status=status.HTTP_200_OK, data=serializer.data) 

  def create(self, request):

    email = request.POST.get('email', None)
    title = request.POST.get('title', None)
    author = request.POST.get('author', None)
    isbn = request.POST.get('isbn', None)

    if not title or not author or not isbn or not email:
      return Response(status=status.HTTP_400_BAD_REQUEST) 


    try: 
      user = User.objects.get(email=email)
    
    except User.DoesNotExist:
      Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
      book = Book.objects.get(isbn=request.data['isbn'])
    
    except Book.DoesNotExist:
     
      if self._validate_in_google(isbn=isbn, title=title, author=author):
        book = self._store_book(isbn, author, title)

        if not book:
          return Response(status.HTTP_400_BAD_REQUEST)

    data = {'user': user.pk, 'book': book.pk}

    serializer = UserBookSerializer(data=data)

    if serializer.is_valid():
      serializer.save()
    else:
      print(serializer.errors)
      return Response(status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_201_CREATED)

  def delete(self, request):
    email = request.POST.get('email', None)
    isbn = request.POST.get('isbn', None)

    user = User.objects.get(email=email)
    book = Book.objects.get(isbn=isbn)

    user_book = UserBook.objects.filter(user=user, book=book)

    if not user_book:
      return Response(status=status.HTTP_400_BAD_REQUEST)

    user_book.delete()

    return Response(status=status.HTTP_200_OK)    

  @staticmethod
  def _store_book(isbn, author, title):
    serializer = BookSerializer(data={'isbn': isbn, 'author': author, 'title': title})

    if serializer.is_valid():
      book = serializer.save() 
      return book

    return None

  @staticmethod
  def _validate_in_google(isbn, author, title):
    url = "https://www.googleapis.com/books/v1/volumes?q=isbn:{}+inauthor:{}+intitle:{}".format(isbn, author, title)

    data = json.loads(urlopen(url).read())

    if data['totalItems'] > 0:
      return True

    return False

