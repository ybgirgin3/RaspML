from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('merhaba', views.index),
    path("hakkinda",views.deneme,name="hakkinda"),
    path("",views.anaSayfa,name="anaSayfa"),
    path("ndviolustur",views.ndviolustur,name="ndviolustur"),
    path("ndvihesaplama",views.ndvihesaplama,name="ndvihesaplama"),
    path("mainpage",views.main),
    path("books/", views.book_list, name="book_list"),
    path("class/books/", views.BookListView.as_view(),name="class_book_list"),
    path("books/upload", views.upload_book, name="upload_book"),
    path('books/<int:pk>/', views.delete_book, name="delete_book"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)