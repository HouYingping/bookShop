from django.shortcuts import render, redirect,reverse
from myapp import models
# from alipay import AliPay
import time
# Create your views here.

# 支付类

class Pay():

    APPID = 2021000118642064
    private_key = '''-----BEGIN RSA PRIVATE KEY-----
    MIIEowIBAAKCAQEAnMfcVHzV5YQhznyh/3n2U3G6isCa964hoElm5fJ50w95dpErd81jXqJLoNuPQBTVS026yWMZW4bVkjPWhE9AiRFx4OMgAcERwr/LMBUcfG8iMKI7XQqS+U7IvuckypcVnWMjcHzb1O1Sd4hB5rL0h+MxgLjGM07/ZtW1FqYnXSoLGxom2F2+kCPdT4+C3qfQ9d3KMNa7tgJslcL4hj3ZSxmKoSQOh9duSifEIRYnMIAn3U7dAqstrV5/Jf/iWIlrj6aAi35rYoTYwO6GgInmgICojeWFWpTD0XDLz4i//9ymWoJ/PNooF1CYKlwOf9zMCWEiAyQGIBxAhHmQA+2lawIDAQABAoIBACi3TuUyNmqQ0ibJ/1hV2D77fjKiqpxAQMNbzLlTK4hAsI62TM+kK3ZcN7/ixWUjA/G2khfTALbgYX7Cr6dU3bG7MhPxaFKMTYyCOsaV9Pvr8LkoqLoVEO5mI4RQiyGB8z8YjA+enYjCyXP5kwPS3eacfjKrye1xSqruPUVQiVCMPpjFGL4Hf+2VpxdS+JHK3RFzFoM2qaqEHQ5SkEJMop4giCx8AKlA0Ln2B2j1Czn34S5YCYrHPaJ4WP+20n5k29FXQYuBOuYybEg5yIFDfCyGe5gB6KtSOBk/mdFOAlzGP5wD1kglGf5uxx+3pKEIZoVqqmCOY2/Ho1DYFVOFGUECgYEAzM5tKtrcsdijwGLi4zM3U/y4Z91NLc30pK+OER5P5mqG0O23AlkN3X3h8JADlVHJTlpXrZI3Kdu3DkUmXri7b5Ju0KzNq7KcR6By0TrG0NSzNp/x0Mq1CUzZyFFshsHrnN2ESrkTMyscAjIKR2QnSBdgAosfNZR1wOjLybWc8mMCgYEAw/hE/0/8ausJo47YyTtch9u5JhEofuhjV1rfEgy05iQXLEyKwGqwYxdgdWyqiuffadAUAX3MRSHDbOgSdO0BZEgEFSU4vpzgaEumeVzs8AIJ2THLgVfwCrmo1h1tsPzVmKVPwPBiJiTtzxa4l/1AFLvmDU+TpTHHTT5AmoMaa1kCgYAElAS6tYPDcf1PGqbJv2ZYOUkCAV9tS7JRUB9T4KKWmwECgJ3brpPxxJOdZgq+dsKSPtDA74jOJbw01HTkHysJdnOFtKcwVGDL9Rk79h1lo6uR6AdmzHE5kP85TCCp7oHO0uDXLsXwGeGZZvb125ZJNUSPKf77mqL7Ofj8PFQS0wKBgQCn2AUocxZrcKFRz7AHMmt/BQbf/sQjZeBn2jHCoNVzY6fhTjFsujQWutfn2sl6rTwhwZDQ8jC5aUCbD213beLKRBATGE0wnOZrDZgozBk3O1e6CbcWMf4rAXcE5DGl6/b5hWT4iCpYJzrzKq+xpbtzxrcz4VtAmpDrrIziibVgCQKBgCFhqRHRRRlcyhcFsdukxisr823DVi69Q3EGTjyJIRpTAME7yytmbMvbmZlyrbGNh4VtdCrKaeLRO2cs+TTmg8JDnhuRIs1N7LuWc3EmEcBqy+yCaYQJDJRw3Zyom14OPb35X8ZASKfye/EhPFgUwjuAdn/4DjvoXe7dWENaVZqj
    -----END RSA PRIVATE KEY-----
    '''
    public_key = '''-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlA+YcyofDdnNXCuJ8dFEwRmpRlYWHRzH/AvSvmMsXq2/Xl1YavAe5mex5S8fFazvrgL60I3QFflkppopON6C7T8jqAGt3LljrTZ7PdBcqKBkXHSFLVRySFopbQ3mIVxFFMIdDBzZrJf0PBg65pTyIm0AdJrvPTuX/GidLTbAk7sZ5wamvj3HwVtrD33q2JJrM7Y8N5W20VHzVb++/S7dyjKRhFE44XQpud1Pw9OMDQeV1dA1JYlcNuIx1kZTdzSrzw6jqK7NmuqcWjJ/RCf4xUFTXStflOF+9ksuNLtRA1hQZS1whEUOueN7OMPZLNPnvAeb7p3Ki56IQpQ6qJ/BUwIDAQAB
    -----END PUBLIC KEY-----'''



    def __init__(self,out_trade_no=5199922211,total_amount=0.01,subject="test"):
        # out_trade_no 账单号：日期：xx年 xx月 xx日 视屏
        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        # total_amount   商品价钱
        self.out_trade_no=out_trade_no
        self.total_amount=total_amount
        self.subject=subject


    def func(self):

        alipay = AliPay(
            appid=self.APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=self.private_key ,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=self.public_key ,
            sign_type="RSA" ,# RSA 或者 RSA2
            debug=False  # 默认False
        )

        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=self.out_trade_no,
        total_amount = self.total_amount,
        subject = self.subject,
        return_url = "http://127.0.0.1:800112/",
        notify_url = "http://127.0.0.1:8000/admin/notify_alipay.jsp"  # 可选, 不填则使用默认notify url

    )
        return "https://openapi.alipaydev.com/gateway.do?" + order_string   # 支付宝付款链接



#显示主页面
def index(request):
    username = request.session.get('login_user')
    # 显示销量高的图书
    saledata = models.Book.objects.all().order_by('-book_sales')[0:12]  # desc offset 0 limit 10
    # 显示最新上架的图书
    latedata = models.Book.objects.all().order_by('-book_time')[0:12]  # desc offset 0 limit 10
    return render(request,'index.html',{'saledata':saledata,'latedata':latedata,'login_user':username})


def showBookItem(request):
    # 分类查询图书
    select = request.GET.get('selecttype')
    data = models.Book.objects.filter(book_type=select)
    return render(request, 'selectBook.html', {'data': data,'login_user':request.session.get('login_user')})


def selectBook(request):
    #搜索框查询图书
    select = request.POST.get('selectname')
    data1 = models.Book.objects.filter(book_name=select)
    data2 = models.Book.objects.filter(book_author=select)
    if data1:
        message = '已为您挑选以下书籍！'
        return render(request,'selectBook.html',{'data':data1,"select_msg": message,'login_user':request.session.get('login_user')})
    elif data2:
        message = '已为您挑选以下书籍！'
        return render(request, 'selectBook.html', {'data': data2,"select_msg": message,'login_user':request.session.get('login_user')})
    else:
        message = '没有找到宝贝噢！为您推荐以下图书！'
        data = models.Book.objects.all()
        return render(request, 'selectBook.html', {'data':data,"select_msg": message,'login_user':request.session.get('login_user')})


#显示所有图书
def showBook(request):
    data = models.Book.objects.all()
    return render(request,'selectBook.html', {'data': data,'login_user':request.session.get('login_user')})

def shoppay(request):
    if request.GET.get("amount"):
        out_trade_no=time.strftime("%Y%m%d%H%M%S",time.localtime())
        total_amount =request.GET.get("amount")
        subject = request.POST.get("subjct")
        if not subject:
            subject="Read More账单"
        print("*"*120)
        print("支付！%s"%subject)
        pay=Pay(out_trade_no=out_trade_no,total_amount=total_amount,subject=subject)
        url=pay.func()
        return redirect(url)

 


