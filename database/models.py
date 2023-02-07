from django.db import models
from django import forms
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

class Member(models.Model):
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=10)

class Memberform(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        labels ={
            'firstname':'ชื่อ',
            'lastname':'นามสกุล',
            'email':'อีเมล์',
            'password': 'รหัส'
        }
        widgets = {
            'password' : forms.PasswordInput(render_value=True)
        }


class Product(models.Model):
    id = models.CharField(primary_key=True,max_length=5)
    name = models.CharField(max_length=100)
    price = models.PositiveSmallIntegerField()
    stock = models.PositiveSmallIntegerField()

class ProductForm(forms.ModelForm):
    files = forms.ImageField(required=False,
         label="รูปภาพ",
        widget=forms.ClearableFileInput(attrs={'multiple':True}))

    class Meta:
        model = Product
        fields = '__all__'
        labels = {'id':'รหัส',
                'name':'ชื่อสินค้า',
                'price':'ราคา',
                'stock':'จำนวน',
                }

class ProductImage(models.Model):
    product_id = models.CharField(max_length=5)
    image_file = models.ImageField(upload_to='product/')

    #แอตทริบิวตเ์ก็บขอ้ มูลเพิ่มเติม ไม่ใช่ฟิ ลด์
    file_format = 'JPEG'
    file_name = 'unnamed.jpg'
    content_type = 'image/jpeg'

    def save(self, *args, **kwargs):
        if self.image_file:
            bio = BytesIO(self.image_file.read())
            img = Image.open(bio)
            max_size = (480, 640)

            img.thumbnail(max_size, Image.ANTIALIAS)
            buffer = BytesIO()
            img.save(buffer, self.file_format, quality=95)
            buffer.seek(0)
            self.image_file = InMemoryUploadedFile(
                buffer,
                'ImageField',
                self.file_name,
                self.content_type,
                buffer.__sizeof__,
                None)

        super(ProductImage, self).save(*args, **kwargs)