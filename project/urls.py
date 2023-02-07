
from django.contrib import admin
from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('',login,name="mem_login"),
    path('logout',logout,name="logout"),
    path('member/management',MemberManagement,name="mem_management"),
    path('member/register',register,name="mem_register"),
    path('member/create',MembarCreate,name="mem_create"),
    path('member/update/<int:id>',MemberUpdate,name="mem_update"),
    path('member/delete/<int:id>',MemberDelete,name="mem_delete"),

    re_path('product/management/(?P<pg>\d*/?)', Productmanagement, name='pro_management'),
    path('product/create/', ProductCreate, name='pro_create'),
    path('product/update/<int:id>/<int:pg>', ProductUpdate, name='pro_update'),
    path('product/delete/<int:id>/', ProductDelete, name='pro_delete'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)