from django.shortcuts import render, redirect,HttpResponse
from myapp import models
from myapp.views.users import checkUser
import datetime


#查看图书详细信息
def book(request):
    try:
        userid = request.session.get('user_id')
        book_id = request.GET.get('book_id')
        print(book_id)
        data = models.Book.objects.filter(book_id=book_id).first()
        addrdata = models.Addr.objects.filter(user_id=userid)
        # comdata = models.Comment.objects.filter(book_id=book_id)'comdata':comdata,
        return render(request,'bookInfo.html',{'data':data,'addrdata':addrdata,"login_user": request.session.get('login_user')})
    except:
        return HttpResponse("没有找到相应的信息！")

#出售图书
@checkUser
def addBook(request):
    if request.method == 'POST':
        book = models.Book(
            seller_id=int(request.session.get('user_id')),
            book_name = request.POST.get('bookname'),
            book_author = request.POST.get('bookauthor'),
            book_price = request.POST.get('bookprice'),
            book_type = request.POST.get('booktype'),
            book_amount = request.POST.get('bookamount'),
            book_decription = request.POST.get('bookdecription'),
            book_time=datetime.datetime.now().strftime('%Y-%m-%d'),
            book_img=request.FILES.get('img')
        )
        book.save()
        return redirect('/sellerSelectBook')
    return render(request,'addBook.html',{"login_user": request.session.get('login_user')})



#用户查看自己正在出售的书籍
@checkUser
def sellerSelectBook(request):
    sellerid = request.session.get('user_id')
    data = models.Book.objects.filter(seller_id=sellerid)
    if data:
        return render(request,'sellerSelectBook.html',{'data':data,"login_user": request.session.get('login_user'),'message':'当前你正在出售的图书！'})
    else:
        return render(request,'sellerSelectBook.html',{"login_user": request.session.get('login_user'),'message':'您没有上架任何图书！'})


#在图书页面购买图书生成订单
@checkUser
def buyBook(request):
    bookid = request.GET.get('bookid')
    bookdata = models.Book.objects.filter(book_id=bookid).first()
    addrdata = models.Addr.objects.filter(user_id=request.session.get('user_id'))
    return render(request,'payBookOrder.html',{'bookdata':bookdata,'addrdata':addrdata,'login_user':request.session.get('login_user')})


#修改商品图书的信息
@checkUser
def updateBook(request):
    if request.method == 'POST':
        sellerid = request.session.get('user_id')
        bookid = request.POST.get('bookid')
        old_book = models.Book.objects.filter(book_id=bookid).filter().first()
        book_img=request.FILES.get('img')
        if book_img:
            book = models.Book(
                book_name=request.POST.get('bookname'),
                book_author=request.POST.get('bookauthor'),
                book_price=request.POST.get('bookprice'),
                book_type=request.POST.get('booktype'),
                book_amount=request.POST.get('bookamount'),
                book_decription=request.POST.get('bookdecription'),
                book_img=request.FILES.get('img'),
                book_id=old_book.book_id,
                book_time=old_book.book_time,
                book_sales=old_book.book_sales,
                seller_id=sellerid,
            )
            book.save()
        else:
            book = models.Book(
                book_name=request.POST.get('bookname'),
                book_author=request.POST.get('bookauthor'),
                book_price=request.POST.get('bookprice'),
                book_type=request.POST.get('booktype'),
                book_amount=request.POST.get('bookamount'),
                book_decription=request.POST.get('bookdecription'),
                book_img=old_book.book_img,
                book_id=old_book.book_id,
                book_time=old_book.book_time,
                book_sales=old_book.book_sales,
                seller_id=sellerid,
            )
            book.save()
        return redirect('/sellerSelectBook')
    else:
        bookid = request.GET.get('bookid')
        data = models.Book.objects.filter(book_id=bookid).first()
        return render(request,'updateBook.html',{'bookid':bookid,'data':data,"login_user": request.session.get('login_user')})


#删除商品
@checkUser
def delBook(request):
    bookid = request.GET.get('bookid')
    print(bookid)
    models.Book.objects.filter(book_id=bookid).delete()
    return redirect("/sellerSelectBook")
