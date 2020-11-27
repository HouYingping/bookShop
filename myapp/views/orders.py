import datetime
import json

from django.shortcuts import render, redirect,HttpResponse
from myapp import models
from myapp.views.users import checkUser


#从书籍页面购买，生成订单
@checkUser
def addOrder(request):
    buyer_id = request.session.get('user_id')
    book_id = request.POST.get('bookid')
    addr_id = request.POST.get('addrid')
    count = request.POST.get('count')
    order_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    book = models.Book.objects.filter(book_id=book_id).first()
    order_price = book.book_price * int(count)
    models.Order.objects.create(order_price=order_price,order_addr_id=addr_id,order_time=order_time,buyer_id=buyer_id)
    order = models.Order.objects.filter(order_time=order_time,buyer_id=buyer_id).first()
    models.OrderBy.objects.create(order_id=order.order_id,book_id=book_id,order_amount=count,orderby_price=order_price,seller_id=book.seller_id)
    return redirect('/selectOrder')


#从购物车购买，生成订单
def addCarOrder(request):
    buyer_id = request.session.get('user_id')
    total_price = request.POST.get('total_price')
    book_lst = request.POST.get('book_list')
    bookdata = json.loads(book_lst)
    addr_id = request.POST.get('addr')
    order_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    models.Order.objects.create(order_price=total_price, order_addr_id=addr_id, order_time=order_time,buyer_id=buyer_id)
    order = models.Order.objects.filter(order_time=order_time,buyer_id=buyer_id).first()
    for i in bookdata:
        book = models.Book.objects.filter(book_id=i[0]).first()
        order_price = book.book_price * i[1]
        models.OrderBy.objects.create(order_id=order.order_id,book_id=i[0],order_amount=i[1],orderby_price=order_price,seller_id=book.seller_id)
    return HttpResponse('ok')


#确认付费信息
@checkUser
def payOrder(request):
    pass


@checkUser#取消订单
def notPayOrder(request):
    orderbyid = request.GET.get('orderby_id')
    status = request.GET.get('status')
    models.OrderBy.objects.filter(orderby_id=orderbyid).update(orderby_pay_status=status)
    return redirect('/selectOrder')


#查询全部订单
@checkUser
def selectOrder(request):
    buyerid = request.session.get('user_id')
    allOrder = models.Order.objects.filter(buyer_id=buyerid)  #用户的所有订单
    data2 = []  #存储用户这个订单的卖家信息
    data3 = []  #存储用户这个订单的书籍信息
    data1 = []
    for i in allOrder:
        orderbydata = models.OrderBy.objects.filter(order_id=i.order_id)      #一笔订单的信息
        data1.extend(orderbydata)
        for j in orderbydata:       # 订单中的详情
            data = models.Book.objects.filter(book_id=j.book_id).first()        #买一本书的记录
            people = models.User.objects.filter(user_id=data.seller_id).first()    # 卖这本书的商家
            if people not in data2:
                data2.append(people)
            if data not in data3:
                data3.append(data)
    return render(request,'selectOrder.html',{'allOrder':allOrder,'orderdata':data1,'bookdata':data3,'userdata':data2,'login_user':request.session.get('login_user')})


#删除订单
@checkUser
def delOrder(request):
    orderby_id = request.POST.get('orderby_id')
    order_id = request.POST.get('order_id')
    models.OrderBy.objects.filter(orderby_id=orderby_id).delete()
    if models.OrderBy.objects.filter(order_id=order_id):
        models.Order.objects.filter(order_id=order_id).delete()
    print(orderby_id,order_id)
    return HttpResponse("ok")



#修改订单中的收货地址
@checkUser
def updateOrder(request):
    orderid = request.POST.get('orderid')
    addid = request.POST.get('addrid')
    models.Order.objects.filter(order_id=orderid).update(order_addr_id=addid)
    return redirect('/selectOrder/')

@checkUser
def updateOrderStatus(request):
    orderby_id = request.POST.get("orderby_id")
    code = request.POST.get("code")
    if code == 6:
        orderdata = models.OrderBy.objects.filter(orderby_id=orderby_id).first()
        bookdata = models.Book.objects.filter(book_id=orderdata.book_id)
        booksales = bookdata.book_sales + orderdata.order_amount
        bookamount = bookdata.book_amount - orderdata.order_amount
        models.Book.objects.filter(book_id=orderdata.book_id).update(book_sales=booksales,book_amount=bookamount)
    c = models.OrderBy.objects.filter(orderby_id=orderby_id).update(orderby_pay_status=code)
    if c:
        return HttpResponse('ok')
    else:
        return HttpResponse("false")

@checkUser
def showDetails(request):
    order_id = request.GET.get("order_id")
    orderby_id = request.GET.get("orderby_id")
    orderby = models.OrderBy.objects.filter(orderby_id=orderby_id).first()
    order = models.Order.objects.filter(order_id=order_id).first()
    addr = models.Addr.objects.filter(addr_id=order.order_addr_id).first()
    book = models.Book.objects.filter(book_id=orderby.book_id).first()
    return render(request,'details.html',{"orderby":orderby,"order":order,"addr":addr,"book":book,'login_user':request.session.get('login_user')})