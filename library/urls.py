from django.urls import path, include
from rest_framework.routers import DefaultRouter

from library.views.books_viewset import BooksViewset

router = DefaultRouter()

router.register(r'books', BooksViewset, base_name='books')

urlpatterns = [
    path('', include(router.urls)),
]