from django.shortcuts import render, redirect,reverse
from myapp import models
from myapp.views.users import checkUser


#用户增加收货地址
@checkUser
def addAddr(request):
    if request.method == 'POST':
        userid = request.session.get('user_id')
        addrname = request.POST.get('addr_name')  # 收货人姓名
        addrtel = request.POST.get('addr_tel')  # 收货人的电话
        addraddr = request.POST.get('addr_addr')  # 收货人的地址
        if addrname and addrtel and addraddr:
            models.Addr.objects.create(user_id=userid,addr_name=addrname,addr_tel=addrtel,addr_addr=addraddr)
            return redirect('/selectAddr')


#用户删除收货地址
@checkUser
def delAdddr(request):
    addrid = request.GET.get('addrid')
    models.Addr.objects.filter(addr_id=addrid).delete()
    return redirect('/selectAddr')


#用户查询收货地址
@checkUser
def selectAddr(request):
    userid = request.session.get('user_id')
    data = models.Addr.objects.filter(user_id=userid)
    if data:
        return render(request,'selectAddr.html',{'data':data,'login_user':request.session.get('login_user')})
    else:
        message = '还没有收货地址哦！'
        return render(request,'selectAddr.html',{'message':message,'login_user':request.session.get('login_user')})


#用户修改收货地址
@checkUser
def updateAddr(request):
    addrid = request.POST.get('addrid')
    addrname = request.POST.get('addrname')  # 收货人姓名
    addrtel = request.POST.get('addrtel')  # 收货人的电话
    addraddr = request.POST.get('addr')  # 收货人的地址
    models.Addr.objects.filter(addr_id=addrid).update(addr_name=addrname,addr_tel=addrtel,addr_addr=addraddr)
    return redirect('/selectAddr')