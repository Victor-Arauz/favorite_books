from django.urls import path    
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('login', views.login),
    path('logout', views.logout),
    path('create/book', views.create_book),
    path('book/<int:book_id>', views.show_book),
    path('book/edit/<int:book_id>', views.edit_book),
    path('book/update/<int:book_id>', views.update_book),
    path('book/delete/<int:book_id>', views.delete_book),
    path('favorite/<int:book_id>', views.create_favorite_book),
    path('favorite/delete/<int:book_id>', views.delete_favorite_book),
]