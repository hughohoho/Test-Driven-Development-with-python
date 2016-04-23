from django.shortcuts import render,redirect
from django.http import HttpResponse
from lists.models import Item
def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')
    #else:
     #   new_item_text = ''
    #item = Item()
    #item.text = request.POST.get('item_text','')
    #item.save()

    return render(request, 'home.html',{
        'new_item_text':request.POST.get('item_text','')
    })
