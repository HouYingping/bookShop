from django.contrib import admin

# Register your models here.

from myapp.models import AdminStrator
from myapp.models import User
from myapp.models import Collection
from myapp.models import Car
from myapp.models import Addr
from myapp.models import Book
from myapp.models import Order
from myapp.models import OrderBy
from myapp.models import Comment
# from myapp.models import Current
# from myapp.models import Grade
# from myapp.models import Info

admin.site.register(AdminStrator)
admin.site.register(User)
admin.site.register(Collection)
admin.site.register(Car)
admin.site.register(Addr)
admin.site.register(Book)
admin.site.register(Order)
admin.site.register(OrderBy)
admin.site.register(Comment)
# admin.site.register(Current)
# admin.site.register(Grade)
# admin.site.register(Info)