"""bookShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import views
from myapp.views import users
from myapp.views import cars
from myapp.views import books
from myapp.views import addr
from myapp.views import orders
from myapp.views import comments
from myapp.views import collections
from myapp.views import grades
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('getcode/',users.getCode),
    path('selectBook/',views.selectBook),
    path('showBook/',views.showBook),
    path('selectBookItem/',views.showBookItem),
    path('login/', users.login),
    path('logout/', users.logout),
    path('register/', users.register),
    path('showUser/',users.showUser),
    path('updateUser/',users.updateUser),
    path('updatePwd/',users.updatePwd),
    path('showSeller/',users.showSeller),
    path('addCar/',books.book),#标记
    path('delCar/',cars.delCar),
    path('buyCarBook/',cars.buyCarBook),
    path('selectCar/',cars.selectCar),
    path('updateCar/',cars.updateCar),
    path('book/',books.book),
    path('addBook/',books.addBook),
    path('sellerSelectBook/',books.sellerSelectBook),
    path('buyBook/',books.buyBook),
    path('delBook/',books.delBook),
    path('updateBook/',books.updateBook),
    path('addAddr/',addr.addAddr),
    path('selectAddr/',addr.selectAddr),
    path('delAddr/',addr.delAdddr),
    path('updateAddr/',addr.updateAddr),
    path('addClt/',collections.addCollection),
    path('selectClt/',collections.selectCollection),
    path('delClt/',collections.delCollection),
    path('addOrder/',orders.addOrder),
    path('addCarOrder/',orders.addCarOrder),
    path('payOrder/',orders.payOrder),
    path('notPayOrder/',orders.notPayOrder),
    path('selectOrder/',orders.selectOrder),
    path('updateOrder/',orders.updateOrder),
    path('delOrder/',orders.delOrder),
    path('addComment/',comments.addComment),
    path('updateComment/',comments.updateComment),
    path('delComment/',comments.delComment),
    path('bookSelectComment/',comments.bookSelectComment),
    path('userSelectComment/',comments.userSelectComment),
    path('addGrade/',grades.addGrade),
    path("updateOrderStatus/",orders.updateOrderStatus),
    path("showDetails/",orders.showDetails),
    path("chat/",users.chat),
    path("shoppay/",views.shoppay),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)