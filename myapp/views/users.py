from django.shortcuts import render, redirect ,HttpResponse
from myapp import models
import http.client as httplib
import urllib.parse as urllib
from random import randint
from captcha.image import ImageCaptcha
import hashlib
u_id = None
alt='1314520我爱你'
def verify():
    list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V',
            'W', 'X', 'Y', 'Z']
    chars = ''
    for i in range(4):
        chars += list[randint(0, 35)]
    image = ImageCaptcha().generate_image(chars)
    image.save('static/yanzheng.png')
    return chars


#短信验证码
class SMS():
    #设定程序短信发送基本参数
    host = "106.ihuyi.com"
    sms_send_uri = "/webservice/sms.php?method=Submit"
    account = "C85767681"
    password = "d2f72bd3ebb92d68c43e32c68ec2310b"

    def __init__(self, mobile):
        self.mobile=mobile
        self.digit = str(randint(0,999999)).zfill(6)
        self.text="您的验证码是：%s。请不要把验证码泄露给其他人。"%self.digit

    def send_sms(self):
        params = urllib.urlencode({'account': self.account, 'password' : self.password, 'content': self.text, 'mobile':self.mobile,'format':'json' })
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPConnection(self.host, port=80, timeout=30)
        conn.request("POST", self.sms_send_uri, params, headers)
        response = conn.getresponse()
        response_str = response.read()
        conn.close()
        return response_str.decode('utf-8')


#判断是否登录的装饰器
def checkUser(func):
    def warpper(request, *args, **kwargs):
        if request.session.get('login_user', False):
            u_id = request.session.get("usre_id")
            return func(request, *args, **kwargs)
        else:
            return redirect('/login')
    return warpper


#登录功能
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password') + alt
        shal = hashlib.sha1()
        shal.update(password.encode('utf-8'))
        password = shal.hexdigest()
        print("--用户账号与密码--"*12)
        print(username,password)

        checkcode = request.POST.get('checkcode')

        if checkcode == request.session.get('check_code'):
            if username and password:  # 确保用户名和密码都不为空
                username = username.strip()
                # 用户名字符合法性验证
                # 密码长度验证
                data1 = models.User.objects.filter(user_tel=username).first()
                data2 = models.User.objects.filter(user_email=username).first()
                if not data1 and not data2:
                    request.session['check_code'] = verify()
                    message = "用户名错误！"
                elif data1 and data1.user_pwd==password:
                    user = data1.user_name
                    id = data1.user_id
                    pwd = data1.user_pwd
                    request.session['login_user'] = user
                    request.session['user_id'] = id
                    request.session['user_pwd'] = pwd
                    return redirect('/')
                elif data2 and data2.user_pwd==password:
                    user = data2.user_name
                    id = data2.user_id
                    pwd = data1.user_pwd
                    request.session['login_user'] = user
                    request.session['user_id'] = id
                    request.session['user_pwd'] = pwd
                    return redirect('/')
                else:
                    request.session['check_code'] = verify()
                    message = '密码错误！'
            else:
                request.session['check_code'] = verify()
                message = '请输入用户名和密码！'
        else:
            message = "验证码错误！"
            request.session['check_code'] = verify()
        return render(request, 'login.html', {"login_error": message})
    else:
        request.session['check_code'] = verify()
    return render(request, 'login.html')


#登出功能
def logout(request):
    request.session.flush()
    return redirect('/')


#短信验证码
def getCode(request):

    usertel = request.POST.get('usertel')
    sms = SMS(usertel)
    str1 = sms.send_sms()
    print("短信验证码")
    print(str1)

    request.session['sms_digit'] = sms.digit
    return HttpResponse('ok')


#注册页面
def register(request):
    global alt

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')+alt
        shal=hashlib.sha1()
        shal.update(password.encode('utf-8'))
        password =shal.hexdigest()
        usertel = request.POST.get('usertel')
        useremail = request.POST.get('useremail')
        checkcode = request.POST.get('checkcode')
        if checkcode == request.session.get('sms_digit'):
            if username and password and usertel and useremail:
                error1 = models.User.objects.filter(user_name=username)
                error2 = models.User.objects.filter(user_tel=usertel)
                error3 = models.User.objects.filter(user_email=useremail)
                if error1:
                    message = '该用户名已存在！'
                    return render(request,'register.html',{'register_error':message})
                elif error2:
                    message = '该手机号已注册！请去找回密码'
                    return render(request, 'register.html', {'register_error': message})
                elif error3:
                    message = '该邮箱已注册！'
                    return render(request, 'register.html', {'register_error': message})
                else:
                    models.User.objects.create(user_name=username, user_pwd=password, user_tel=usertel,user_email=useremail)
                    return redirect('/login')
            else:
                message = "信息没有填写完整！"
        else:
            message = '验证码错误！'
        return render(request, 'register.html', {'register_error': message})
    return render(request, 'register.html')



#显示用户的信息
@checkUser
def showUser(request):
    userid = request.session.get('user_id')
    data = models.User.objects.filter(user_id=userid).first()
    return render(request,'showUser.html',{'data':data,"login_user": request.session.get('login_user')})


@checkUser
def showSeller(request):
    userid = request.GET.get('userid')
    sellerdata = models.User.objects.filter(user_id=userid).first()
    bookdata = models.Book.objects.filter(seller_id=userid)
    return render(request,'seller.html',{'bookdata':bookdata,'sellerdata':sellerdata,"login_user": request.session.get('login_user')})


#修改用户的信息
@checkUser
def updateUser(request):
    if request.method == 'POST':
        old_user = models.User.objects.filter(user_id=request.session.get('user_id')).first()
        user_img = request.FILES.get('img')
        if user_img:
            user = models.User(
                user_id=request.session.get('user_id'),
                user_pwd=request.session.get('user_pwd'),
                user_name = request.POST.get('username'),
                user_tel = request.POST.get('usertel'),
                user_sex = request.POST.get('usersex'),
                user_email = request.POST.get('useremail'),
                user_decription = request.POST.get('userdecription'),
                user_score= old_user.user_score,
                user_money= old_user.user_money,
                user_img = request.FILES.get('img')
            )
            user.save()
        else:
            user = models.User(
                user_id=request.session.get('user_id'),
                user_pwd=request.session.get('user_pwd'),
                user_name=request.POST.get('username'),
                user_tel=request.POST.get('usertel'),
                user_sex=request.POST.get('usersex'),
                user_email=request.POST.get('useremail'),
                user_decription=request.POST.get('userdecription'),
                user_score=old_user.user_score,
                user_money=old_user.user_money,
                user_img=old_user.user_img,
            )
            user.save()
        return redirect('/')


#用户通过短信验证码修改密码
def updatePwd(request):
    if request.method == 'POST':
        usertel = request.POST.get('usertel')
        checkcode = request.POST.get('checkcode')
        pwd1 = request.POST.get('userpwd1')
        pwd2 = request.POST.get('userpwd2')
        if checkcode == request.session.get('sms_digit'):
            if pwd1 == pwd2:
                models.User.objects.filter(user_tel=usertel).update(user_pwd=pwd1)
                return redirect('/login')
            else:
                message = '两次输入的密码不一致！'
                return render(request, 'updatePwd.html', {'message': message})
        else:
            message = '验证码错误！'
            return render(request, 'updatePwd.html',{'message':message})
    return render(request, 'updatePwd.html')



def chat(request):
    seller_id = request.GET.get("seller_id")
    user_id = request.session.get("user_id")
    return render(request,"chat.html",{"user_id":user_id})