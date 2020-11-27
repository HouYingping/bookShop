from django.db import models


# Create your models here.


# 管理员表
class AdminStrator(models.Model):
    admin_id = models.AutoField(primary_key=True)  # 管理员ID
    admin_pwd = models.CharField(max_length=45)  # 管理员的密码
    admin_name = models.CharField(max_length=45, unique=True)  # 管理员的用户名
    admin_tel = models.IntegerField(unique=True)  # 管理员的电话
    admin_email = models.EmailField(unique=True)   #管理员的邮箱


# 用户表
class User(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    user_id = models.AutoField(primary_key=True)    #用户的ID
    user_name = models.CharField(max_length=200,unique=True)  #用户的昵称
    user_sex = models.CharField(max_length=32,choices=gender,default='男')  #用户的性别，默认为男
    user_pwd = models.CharField(max_length=2000)  #用户的密码
    user_tel = models.CharField(max_length=11,unique=True)  #用户的手机号
    user_email = models.EmailField(unique=True)  #用户名(邮箱)
    user_money = models.DecimalField(max_digits=10,default=0,decimal_places=2)  #用户的余额
    user_score = models.DecimalField(max_digits=5,default=5,decimal_places=2)  #用户收到的评分
    user_img = models.ImageField(upload_to='user_image',null=True)  #用户的头像
    user_decription = models.CharField(max_length=80,default='',null=True)   #用户的个性签名


#收藏表(用户关注的其他用户)
class Collection(models.Model):
    clt_id = models.AutoField(primary_key=True)  #收藏记录的ID
    user_id = models.IntegerField()  #收藏者的ID
    seller_id = models.IntegerField()  #被收藏者的ID


#购物车表
class Car(models.Model):
    car_id = models.AutoField(primary_key=True) #购物车的ID
    user_id = models.IntegerField()  #用户的ID
    book_id = models.IntegerField()  #商品的ID
    car_amount = models.IntegerField(default=1)  #购物车中某本书的数量
    car_total_price = models.DecimalField(max_digits=6,decimal_places=2)  #购物车中某本书的总价


#用户收货地址表
class Addr(models.Model):
    addr_id = models.AutoField(primary_key=True) #收货地址的ID
    user_id = models.IntegerField()  #用户的ID
    addr_name = models.CharField(max_length=45) #收货人姓名
    addr_tel = models.CharField(max_length=11) #收货人的电话
    addr_addr = models.CharField(max_length=80) #收货人的地址


#书籍详细信息表
class Book(models.Model):
    book_id = models.AutoField(primary_key=True) #商品的ID
    book_name = models.CharField(max_length=80) #书名
    book_author = models.CharField(max_length=20) #书的作者
    book_price = models.DecimalField(max_digits=6,decimal_places=2) #书的价格
    book_type = models.CharField(max_length=25) #书籍所属的类别
    book_amount = models.IntegerField(default=1) #书籍剩余的数量
    book_time = models.CharField(max_length=20) #书籍的上架时间
    book_sales = models.IntegerField(default=0) #书籍的销量
    book_decription = models.CharField(max_length=300,null=True) #书籍的描述
    book_img = models.ImageField(upload_to='book_image') #书籍的图片
    seller_id = models.IntegerField() #书籍的卖家的ID


#订单表
class Order(models.Model):
    order_id = models.AutoField(primary_key=True) #订单号
    order_price = models.DecimalField(max_digits=8,decimal_places=2) #订单的总价
    order_addr_id = models.IntegerField() #地址的ID
    order_time = models.CharField(max_length=40)  #订单生成的时间
    buyer_id = models.IntegerField()  #买家的ID


#订单详细信息表
class OrderBy(models.Model):
    orderby_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()  #订单号
    book_id = models.IntegerField()   #书籍的ID
    order_amount = models.IntegerField() #购买的书籍数量
    orderby_price =  models.CharField(max_length=20,default='0') #购买此类书籍的总价格
    orderby_pay_status = models.IntegerField(default=1)  # 订单的状态  1未支付 2取消支付 3支付超时 4未发货 5未收货 6已收货 7申请退款 8已退款
    seller_id = models.IntegerField()  # 书籍的卖家的ID


#评论表
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True) #评论的ID
    user_id = models.IntegerField()   #用户的ID
    orderby_id = models.IntegerField()   # 订单的ID
    comment_info = models.CharField(max_length=600)  #评论的内容
    book_id = models.IntegerField()  #书籍的ID


# #浏览记录表
# class Current(models.Model):
#     current_id = models.AutoField(primary_key=True) #浏览记录的ID
#     user_id = models.IntegerField()  #用户的ID
#     book_id = models.IntegerField()  #浏览书籍的ID
#     current_time = models.CharField(max_length=40) #浏览记录的日期时间
#
#
# #评分表(用户的评分)
# class Grade(models.Model):
#     user_id = models.IntegerField()  #用户的ID
#     grade_score = models.IntegerField() #用户收到的打分
#
#
# #用户的消息表
# class Info(models.Model):
#     info_id = models.AutoField(primary_key=True) #信息的ID
#     user_id = models.IntegerField()  #用户的ID
#     info_content = models.CharField(max_length=40) #信息的内容