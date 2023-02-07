from database.models import ProductImage
from django import template


register = template.Library()



@register.filter
def GetImages(id):
    return ProductImage.objects.filter(product_id = id)