from django.shortcuts import render, redirect,HttpResponse
from myapp import models
from myapp.views.users import checkUser


#用户添加评论
@checkUser
def addComment(request):
    if request.method == 'POST':
        userid = request.session.get('user_id')
        orderbyid = request.POST.get('orderbyid')
        score = request.POST.get('score')
        remark = request.POST.get('remark')
        orderby = models.OrderBy.objects.filter(orderby_id=orderbyid).first()
        models.Comment.objects.create(user_id=userid,orderby_id=orderbyid,comment_info=remark,book_id=orderby.book_id)
        models.User.objects.filter(user_id=orderby.seller_id).update(user_score=score)
        return HttpResponse('ok')
    else:
        orderbyid = request.GET.get('orderbyid')
        return render(request,'remark.html',{'orderbyid':orderbyid})


#用户删除评论
@checkUser
def delComment(request):
    comid = request.GET.get('comid')
    models.Comment.objects.filter(comment_id=comid).delete()
    return redirect('/userSelectComment')


#用户修改评论
@checkUser
def updateComment(request):
    comid = request.POST.get('comid')
    cominfo = request.POST.get('cominfo')
    models.Comment.objects.filter(comment_id=comid).update(comment_info=cominfo)
    return redirect('/userSelectComment')


#用户查看自己的评论
@checkUser
def userSelectComment(request):
    userid = request.session.get('user_id')
    data = models.Comment.objects.filter(user_id=userid)
    return render(request,'userCom.html',{'userCom':data})


#书籍的评论
def bookSelectComment(request):
    bookid = request.GET.get('bookid')
    data = models.Order.objects.filter(orderby__book_id=bookid)
    lst = []
    for i in data:
        lst.append(models.Comment.objects.filter(order_id=i.order_id))
    return render(request,'bookInfo.html',{'comdata':lst})