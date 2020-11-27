from django.shortcuts import render, redirect
from myapp import models
from myapp.views.users import checkUser


#用户添加购物车
@checkUser
def addCar(request):
    if request.method == 'GET':
        userid = request.session.get('user_id')
        bookid = request.GET.get('bookid')
        data = models.Book.objects.filter(book_id=bookid).first()
        error = models.Car.objects.filter(user_id=userid,book_id=bookid)
        if error:
            message = '购物车中已存在该商品！'
            return render(request,'bookInfo.html',{'message':message,'login_user':request.session.get('login_user'),'data':data})
        else:
            message = '加入购物车成功！'
            models.Car.objects.create(user_id=userid,book_id=bookid,car_total_price=data.book_price)
            return render(request,'bookInfo.html',{'message':message,'login_user':request.session.get('login_user'),'data':data})


#用户删除购物车
@checkUser
def delCar(request):
    userid = request.session.get("user_id")
    bookid = request.GET.get('bookid')
    models.Car.objects.filter(user_id=userid,book_id=bookid).delete()
    return redirect('/selectCar')

@checkUser#用户修改购物车的信息
def updateCar(request):
    userid = request.session.get('user_id')
    bookid = request.POST.get('book_id')
    bookamount = request.POST.get('count')
    totalprice = request.POST.get('total')
    models.Car.objects.filter(user_id=userid, book_id=bookid).update(car_amount=bookamount,car_total_price=totalprice)
    return redirect('/')


#用户购买购物车中的书籍
@checkUser
def buyCarBook(request):
    buyerid = request.session.get('user_id')
    addrid = request.POST.get('addrid')
    booklst = request.POST.get('book_lst')
    total_price = 0
    for i in booklst:
        bookdata = models.Book.objects.filter(book_id=i[1]).first
        total_price += bookdata.book_price * int(i[2])
    models.Order.objects.create(order_price=total_price, order_addr_id=addrid, buyer_id=buyerid)
    lastdata = models.Order.objects.all().last()
    for i in booklst:
        bookdata = models.Book.objects.filter(book_id=i[1]).first
        models.OrderBy.objects.create(order_id=lastdata.order_id, book_id=i[1], orderby_price=bookdata.book_price, order_amount=i[2])
    return render(request,'payOrder.html',{'total_price':total_price})


#用户查看购物车
@checkUser
def selectCar(request):
    userid = request.session.get('user_id')
    models.Car.objects.filter(car_amount__lte=0).delete()
    cardata = models.Car.objects.filter(user_id=userid)
    addrdata = models.Addr.objects.filter(user_id=userid)
    lst = []
    for i in cardata:
        bookid = i.book_id
        bookdata = models.Book.objects.filter(book_id=bookid).first()
        lst.append(bookdata)
    return render(request,'selectCar.html',{'cardata':cardata,'bookdata':lst,'addrdata':addrdata,'login_user':request.session.get('login_user')})