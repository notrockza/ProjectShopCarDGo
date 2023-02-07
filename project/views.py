from django.shortcuts import render,redirect
from .forms import *
from database.models import *
from django.db.models import Q
from django.core.paginator import Paginator
from PIL import Image
import os

# def isLogin(request):
#     if 'id' not in request.session:
#        return redirect('/')
#     return redirect("mem_management")

def isLogin(request):
      chk = True
      if 'id' not in request.session:
         chk = False
      return chk

def login(request):
    if 'id' in request.session:
        return redirect('mem_management')

    # isLogin(request)

    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            data=Member.objects.get(Q(email=email) & Q(password=password))
            if data:
                request.session['id'] = data.id
                request.session['firstname'] = data.firstname
                return redirect('mem_management')



            # email = request.POST.get("email",None)
            # if email=="notrockza@gmail.com":
            #     request.session["email"]=email
            #     return redirect("mem_management")

    else:
        form=LoginForm()
    vars={'form': form}
    return render(request,"member-login.html",vars)

def logout(request):
    del request.session["id"]
    del request.session["firstname"]
    return redirect("/")



def MemberManagement(request):

    #ถ้ายังไม่ login ให้ไปเพจเข้าระบบ
    if not isLogin(request):
        return redirect('/')
    form = SearchForm()
    if request.method == 'POST':
        kw = request.POST.get("name","")
        data = Member.objects.filter(
            Q(firstname__contains = kw) |
            Q(lastname__contains = kw)).order_by("-id")
        count = data.count()
            
    else:
        data = Member.objects.all().order_by("-id")
        count = data.count()

    vars = {'form':form,'data':data,'count':count,}
    return render(request,"member-management.html",vars)

def register(request):
    if request.method == 'POST':
         form = Memberform(request.POST)
         if form.is_valid():
             form.save()
             return redirect('mem_login')
    else:
         form = Memberform()
    vars ={'form':form}
    return render(request,"member-form.html",vars)

def MembarCreate(request):
    if request.method == 'POST':
        form = Memberform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mem_management')
    else:
        form = Memberform()

    vars = {'form':form}
    return render(request,"member-form.html",vars)

def MemberUpdate(request,id=1):
    if request.method == 'POST':
        data1 = Member.objects.get(id=id)
        form = Memberform(instance=data1,data=request.POST)
        if form.is_valid():
            form.save()
        return redirect("mem_management")
    else:
        data = Member.objects.get(id=id)
        form = Memberform(initial=data.__dict__)

    vars = {'form':form}
    return render(request,"member-form.html",vars)

def MemberDelete(request,id):
    data = Member.objects.get(id=id)
    data.delete()
    return redirect("mem_management")

def Productmanagement(request,pg=1):
    #ถ้ายังไม่ login ให้ไปเพจเข้าระบบ
    if not isLogin(request):
        return redirect('mem_login')

    
    prolabel = ProductForm()
    form = SearchForm()
    kw = ('')
    if request.method=='POST':
        kw = request.POST.get('name', '')
       
    rows = Product.objects.filter(Q(name__contains=kw)).order_by('-id')
    pgn = Paginator(rows, 4)
    page = pgn.get_page(pg)
    count = rows.count()

  
    vars = {'form': form, 'page': page,'count':count,'prolabel':prolabel}
    return render(request, 'product-management.html',vars)

def ProductCreate(request):

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            files = request.FILES.getlist('files')
            pd = form.save()    #pd เป็นออบเจ็กต์ผลลัพธ์ของเมธอด save()

            #อ่านค่า id ของสินค่า ที่เพิ่มใหม่
            #เพื่อนำไปเติมลงในโมเดล ProductImage
            pid = pd.id         
            
            #เนื่องจากเราอัปโหลดแบบ multiple 
            #จึงต้องใช้ลูปเพื่อบันทึกข้อมูลตามจำนวนไฟล์
            #แต่เราไม่ได้สร้าง โมเดลฟอร์ม ของ ProductImage
            #ดังนั้น จึงต้องเพิ่มข้อมูลแบบกำหนดค่าให้แก่โมเดลโดยตรง
            for f in files:
                pd_img = ProductImage(product_id=pid, image_file=f)

                #กำหนดข้อมูลของภาพให้แก่แอตทริบิวต์ในคลาส ProductImage
                #เพื่อใช้ในการเปลี่ยนขนาดของภาพ
                #pd_img.file_format = f.image.format
                pd_img.file_format = f.content_type.split('/')[1]
                pd_img.file_name = f.name
                pd_img.content_type = f.content_type
                pd_img.save()

            return redirect('/product/management/')

    else:
        form = ProductForm()
     
    return render(request, 'product-form.html', {'form':form})

def ProductDelete(request,id):
    product = Product.objects.get(id=id)
    product.delete()

    #หมายเหตุ ลบรูปภาพข้างนอกก่อน แล้วค่อยลบในตาราง
    product_image = ProductImage.objects.filter(product_id = id)
    for p in product_image:
        url  = p.image_file.url
        delete_file_product(url)
    product_image.delete()
    return redirect('/product/management/')

def ProductUpdate(request, id,pg):

    if request.method == 'POST':
        row = Product.objects.get(id=id) 
        form = ProductForm(instance=row, data=request.POST, files=request.FILES)
         
        if form.is_valid():
            form.save()    

            #ตรวจสอบมีการส่งรูปภาพเข้ามาหรือไม่
            files = request.FILES.getlist('files')
            if len(files) > 0:
                #หมายเหตุ ลบรูปภาพข้างนอกก่อน แล้วค่อยลบในตาราง
                product_image = ProductImage.objects.filter(product_id = id)
                for p in product_image:
                    url  = p.image_file.url
                    delete_file_product(url)
                product_image.delete()  
            
                #เพิ่มรูปภาพใหม่
                for f in files:
                    pd_img = ProductImage(product_id=id, image_file=f)

                    pd_img.file_format = f.content_type.split('/')[1]
                    pd_img.file_name = f.name
                    pd_img.content_type = f.content_type
                    pd_img.save()

            return redirect(f'/product/management/{pg}')
    else:
        row = Product.objects.get(id=id)
        form = ProductForm(initial=row.__dict__)

        #ซ่อนฟิลด์ที่ไม่ต้องการแก้ไข
        form.fields['id'].widget.attrs['readonly'] = True

    vars = {'form':form,'pg':pg}
    return render(request, 'product-form.html', vars)


def delete_file_product(imagepath):
    img = imagepath[1:]
    if os.path.exists(img):
        print("deleted succesfully")
        os.remove(img)
    else:
        print("The file does not exist")