from django.shortcuts import render, redirect
from myapp import models
from myapp.views.users import checkUser


#显示用户的关注列表
@checkUser
def selectCollection(request):
    userid = request.session.get('user_id')
    data = models.Collection.objects.filter(user_id=userid)
    if data:
        lst = []
        message = '已为您展示关注列表'
        for i in data:
            sellerdata = models.User.objects.filter(user_id=i.seller_id).first()
            lst.append(sellerdata)
        return render(request,'selectCollection.html',{'login_user':request.session.get('login_user'),'sellerdata':lst,'message':message})
    else:
        message = '还没有关注任何人噢'
        return render(request,'selectCollection.html',{'login_user':request.session.get('login_user'),'message':message})


#用户添加关注
@checkUser
def addCollection(request):
    userid = request.session.get('user_id')
    bookid = request.GET.get('bookid')
    data = models.Book.objects.filter(book_id=bookid).first()
    sellerid = data.seller_id
    error = models.Collection.objects.filter(user_id=userid, seller_id=sellerid)
    if userid == sellerid:
        message = '不能收藏自己哦！'
        return render(request, 'bookInfo.html',{'message': message, 'login_user': request.session.get('login_user'), 'data': data})
    elif error:
        message = '该商家已在您的收藏列表！'
        return render(request, 'bookInfo.html',{'message': message, 'login_user': request.session.get('login_user'), 'data': data})
    else:
        message = '收藏商家成功！'
        models.Collection.objects.create(user_id=userid, seller_id=sellerid)
        return render(request, 'bookInfo.html',{'message': message, 'login_user': request.session.get('login_user'), 'data': data})


#用户取消关注
@checkUser
def delCollection(request):
    userid = request.session.get('user_id')
    sellerid = request.GET.get('sellerid')
    models.Collection.objects.filter(user_id=userid,seller_id=sellerid).delete()
    return redirect('/selectClt')