from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image
from django.shortcuts import reverse
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.conf import settings
import random
import string
from datetime import date
import datetime
from ckeditor.fields import RichTextField
import datetime
from appp.models import Notification
from django.contrib.auth.models import User
# Create your models here.
def arabic_slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str

LABEL_CHOICES = (
    ('A', 'قيد الانتظار'),
    ('B', 'تم التواصل'),
    ('C', 'مغلق')
)
LABEL_CHOICES2 = (
    ('A', 'خدمه جاريه'),
    ('B', 'ستنتهي قريبا'),
    ('C', 'منتهيه')
)
def generate_order_id():
    date_str = date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return date_str + rand_str


class Category(models.Model):
    title = models.CharField(verbose_name='نوع الخدمه',max_length=1000)
    def __str__(self):
        return str(self.title)
    class Meta:
        verbose_name_plural = ('انواع الخدمات')
        verbose_name = ('نوع خدمه')


class Service(models.Model):
    title = models.CharField(max_length=10000,verbose_name='عنوان الخدمه')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name='نوع الخدمه')
    time = models.CharField(max_length=10000,verbose_name='مدة عمل الخدمة')
    price = models.FloatField(verbose_name='تكلفة الخدمه')
    date = models.DateTimeField(default=timezone.now,editable=False)
    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ('-date',)
        verbose_name_plural = ('الخدمات')
        verbose_name = ('خدمه')

class Worker(models.Model):
    name = models.CharField(verbose_name='اسم العامل', max_length=10000, unique=True)
    phone = PhoneNumberField(verbose_name='رقم الهاتف')
    phone2 = PhoneNumberField(null=True, blank=True,verbose_name='رقم هاتف ولي الأمر')
    email = models.EmailField(null=True, blank=True,verbose_name='البريد الالكتروني')
    address = models.TextField(verbose_name='العنوان')
    content = models.TextField(null=True, blank=True, verbose_name=' ملاحظات')
    media = models.FileField(null=True, blank=True, verbose_name='ملفات ميديا')
    date = models.DateTimeField(default=timezone.now,editable=False)
    def get_absolute_url(self):
        return f'/worker/{self.id}'
    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('-date',)
        verbose_name_plural = ('الموظفين')
        verbose_name = ('موظف')

class Client(models.Model):
    name = models.CharField(verbose_name='اسم العميل',max_length=10000,unique=True)
    phone = PhoneNumberField(verbose_name='رقم الهاتف')
    email = models.EmailField(verbose_name='البريد الالكتروني')
    address = models.TextField(verbose_name='العنوان')
    content = models.TextField(null=True,blank=True,verbose_name=' ملاحظات')
    media = models.FileField(null=True,blank=True,verbose_name='ملفات ميديا')
    date = models.DateTimeField(default=timezone.now,editable=False)
    def get_absolute_url(self):
        return f'/client/{self.id}'

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('-date',)
        verbose_name_plural = ('العملاء')
        verbose_name = ('عميل')

class Bond(models.Model):
    title = models.CharField(max_length=10000, verbose_name='اسم الاذن')
    price = models.FloatField(verbose_name='تكلفة الاذن')
    content = models.TextField(null=True,blank=True,verbose_name=' المنصرف اليه')
    id = models.AutoField(primary_key=True,max_length=100,verbose_name='رقم الاذن')
    date = models.DateTimeField(default=timezone.now,editable=False)
    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ('-date',)
        verbose_name_plural = ('الاذونات')
        verbose_name = ('اذن')
class ClientService(models.Model):
    client = models.ForeignKey(Client,on_delete=models.CASCADE,related_name='services',verbose_name='العميل')
    service = models.ForeignKey(Service,on_delete=models.CASCADE,related_name='clients',verbose_name='الخدمه')
    worker = models.ForeignKey(Worker,on_delete=models.CASCADE,related_name='works',null=True,blank=True,verbose_name='الموظف')
    date1 = models.DateField(default=timezone.now,verbose_name='تاريخ بداية الخدمه')
    date2 = models.DateField(default=timezone.now,verbose_name='تاريخ نهاية الخدمه')
    price = models.FloatField(default=0,help_text='اتركه كما هو وسيتم اضافته تلقائيا حسب سعر الخدمه. أو يمكنك اضافته بنفسك',verbose_name='المبلغ المستحق')
    date = models.DateTimeField(default=timezone.now,editable=False)
    active = models.BooleanField(default=True,verbose_name='خدمه جاريه')
    label = models.CharField(choices=LABEL_CHOICES2,default='A', max_length=1,verbose_name='الحاله',editable=False)
    send = models.BooleanField(editable=False,default=False)
    send2 = models.BooleanField(editable=False,default=False)

    def __str__(self):
        return str(self.client.name+'--'+self.service.title)
    def save(self, *args, **kwargs):
        if self.price <=0:
            self.price = self.service.price
        arr = self.date2.month
        ar = self.date2.replace(month=(arr -1))
        if self.date2 <= datetime.date.today() and self.send==False:
            self.active = False
            self.label = 'C'
            self.send = True

            user = User.objects.get(is_staff = True)

            Notification.send(
                [user],
                f'انتهاء خدمة {self.client.name}',
                'fa-info',
                Notification.COLOR_DANGER,
                url=f'http://site141.pythonanywhere.com/admin/app/clientservice/{self.id}/'
            )

        elif datetime.date.today() >= ar and self.send2==False:
            self.label = 'B'
            self.send2 = True

            user = User.objects.get(is_staff=True)

            Notification.send(
                [user],
                f'سوف تنتهي خدمة {self.client.name}',
                'fa-info',
                Notification.COLOR_WARNING,
                url=f'http://site141.pythonanywhere.com/admin/app/clientservice/{self.id}/')
        super(ClientService, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-date',)
        verbose_name_plural = ('اشتراكات الخدمات')
        verbose_name = (' اشتراك خدمه')


class Help(models.Model):
    name = models.CharField(verbose_name='الاسم  ', max_length=10000)
    phone = PhoneNumberField(verbose_name='رقم الهاتف')
    email = models.EmailField(verbose_name='البريد الالكتروني')
    content = models.TextField( verbose_name=' الرساله')
    label = models.CharField(choices=LABEL_CHOICES,default='A', max_length=1,verbose_name='الحاله')
    date = models.DateTimeField(default=timezone.now,editable=False,verbose_name='تاريخ الارسال')

    def __str__(self):
        return str(self.name)
    class Meta:
        ordering = ('-date',)
        verbose_name_plural = ('طلبات المساعده')
        verbose_name = ('طلب مساعده')

class Posts(models.Model):
    title = models.CharField(verbose_name='عنوان المقال', max_length=10000,unique=True)
    content = models.TextField( verbose_name='وصف المقال')
    المقال = RichTextField(null=True,blank=True)
    img = models.ImageField(default='notfound.png',verbose_name='صورة المقال')
    date = models.DateTimeField(default=timezone.now,verbose_name='تاريخ المقال')
    slug = models.SlugField(null=True, blank=True, unique=True, editable=False)
    active  = models.BooleanField(default=True,help_text='قم بالغاء التفعيل بدلا من الحذف ولن يظهر في الموقع',verbose_name='مفعل')
    def __str__(self):
        return str(self.title)
    def get_absolute_url(self):
        return f'/detail/{self.slug}'

    @property
    def ImageURL(self):
        try:
            url = self.img.url
        except:
            url = ''
        return url

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if not self.slug:
            self.slug = arabic_slugify(self.title)


        super(Posts, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-date',)
        verbose_name_plural = ('المقالات')
        verbose_name = ('مقال')
class SiteEdit(models.Model):
    title = models.CharField(max_length=1000,verbose_name='اسم الموقع')
    content = models.TextField(verbose_name='وصف الموقع')
    script = models.TextField(null=True,blank=True,help_text='هذا حقل اكواد اضافيه لموقعك كحقل تحقق احصائيات جوجل مثلا',verbose_name='اكواد اضافيه')
    about = models.TextField(null=True,blank=True,verbose_name='من نحن')
    img = models.ImageField(default='image.png',verbose_name='صورة من نحن')
    img2 = models.ImageField(default='image.png',verbose_name='لوجو الموقع')
    img3 = models.ImageField(help_text='يفضل ان يكون 543 * 555',default='image.png',verbose_name='صورة وصف الموقع')
    img4 = models.ImageField(help_text='يفضل ان يكون 630 * 1920',default='image.png', verbose_name='صورة السلايدر1')
    img5 = models.ImageField(help_text='يفضل ان يكون 451 * 1920',default='image.png', verbose_name='صورة السلايدر2')
    img6 = models.ImageField(help_text='يفضل ان يكون 630 * 1920',default='image.png', verbose_name='صورة السلايدر3')
    email = models.EmailField(verbose_name='ايميل الموقع')
    phone = models.CharField(max_length=1000,verbose_name='رقم الهاتف للموقع')
    address = models.TextField(verbose_name='عنوان المكتب ')
    active = models.BooleanField(default=True,verbose_name='تفعيل الموقع')
    facebook = models.URLField(default='https://facebook.com', verbose_name='رابط الفيسبوك')
    instagram = models.URLField(default='https://instagram.com',verbose_name='رابط الانستجرام')
    twitter = models.URLField(default='https://twitter.com',verbose_name='رابط تويتر')
    whatsapp = models.CharField(max_length=20,verbose_name='رقم الواتساب')
    whyus1 = models.CharField(default='#',max_length=1000,verbose_name='لماذا نحن -الخبره')
    whyus2 = models.CharField(default='#',max_length=1000,verbose_name='لماذا نحن -الأمانه')
    whyus3 = models.CharField(default='#',max_length=1000,verbose_name='لماذا نحن -الكفاءه')
    roya = models.CharField(default='#',max_length=1000,verbose_name='الرؤيه')
    resala = models.CharField(default='#',max_length=1000,verbose_name='الرساله')
    hadaf = models.CharField(default='#',max_length=1000,verbose_name='الهدف')
    small = models.TextField(null=True,blank=True,verbose_name=' نبذه الفوتر')


    def __str__(self):
        return str(self.title)


    @property
    def ImageURL(self):
        try:
            url = self.img.url
        except:
            url = ''
        return url



    class Meta:
        verbose_name_plural = ('اعدادات الموقع')
        verbose_name = ('اعداد الموقع')


