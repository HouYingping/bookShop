from django.shortcuts import render, redirect
from myapp import models
from myapp.views.users import checkUser

#用户给商品打分
@checkUser
def addGrade(request):
    orderbyid = request.POST.get('orderbyid')
    score = request.POST.get('score')
    orderby = models.OrderBy.objects.filter(orderby_id=orderbyid).first()
    book = models.Book.objects.filter(book_id=orderby.book_id).first()
    models.Grade.objects.create(user_id=book.seller_id,grade_score=score)
    total = models.Grade.objects.filter(user_id=book.seller_id)
    score = 0
    count = 0
    for i in total:
        score += i.grade_score
        count += 1
    grade = score / count
    models.User.objects.filter(user_id=book.seller_id).update(user_score=round(grade,2))
    return redirect('/')