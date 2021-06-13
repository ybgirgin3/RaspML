from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from todo_app.models import backend
from todo_app.models import deneme
from django.urls import reverse_lazy
import os
from .forms import BookForm
from .models import Book

from datetime import date
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

# Create your views here.
def index(request):
    return HttpResponse("index sayfam")

def deneme(request):
    file_path = ('media/books/txt/deneme.txt')   #full path to text.
    data_file = open(file_path , 'r')
    data = data_file.read()
    data=list(data.split("\n"))
    context = {'deneme': data}
    return render(request,"todo_app/abaut.html",context,backend().badana())

def anaSayfa(request):
    return render(request,"todo_app/index.html")

def main(request):
    return render(request,"todo_app/base.html")

def ndviolustur(request):
    context = {}
    name=""
    if request.method =="POST":
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name=fs.save(uploaded_file.name,uploaded_file)
        url= fs.url(name)
        context["url"]=fs.url(name)
        print(name)
    return render(request,"todo_app/ndviolustur.html",context)

def ndvihesaplama(request):
    api = SentinelAPI('flavves', 'BATUhan123.', 'https://scihub.copernicus.eu/dhus')
    footprint = geojson_to_wkt(read_geojson('media/map.geojson'))
    products = api.query(footprint,
                        date=('20191219', date(2019, 12, 29)),
                        platformname='Sentinel-2')
    # pandas dataframe yap
    products_df = api.to_dataframe(products)

    # filtreleme
    products_df_sorted = products_df.sort_values(['cloudcoverpercentage', 'ingestiondate'], ascending=[True, True])
    products_df_sorted = products_df_sorted.head(1)



    df=products_df_sorted
    NotDefteriKaydi = df.values.tolist()
    str_denemesi=str(NotDefteriKaydi)

    Kaydetmeye_basla=list(str_denemesi.split(","))
    yerler=[0,7,8,9,12,14,18,19,20]
    isimler=["Dosya adı:","Uydu adı","Dosya boyutu","Çekim tarihi","Orbit numarası","Bulut","vejetasyon","su","not vejetasyon"]
    i=0

    with open("media/books/txt/deneme.txt", "w") as dosya:
        for sira in yerler:
            print(isimler[i]+":"+Kaydetmeye_basla[sira])
            yaz=(isimler[i]+":"+Kaydetmeye_basla[sira])
            i=i+1
            dosya.write(yaz)
            dosya.write("\n")
    dosya.close()

    file_path = ('media/books/txt/deneme.txt')   #full path to text.
    data_file = open(file_path , 'r')
    data = data_file.read()
    data=list(data.split("\n"))
    context = {'deneme': data}
    return render(request,"todo_app/ndvihesaplama.html",context,backend().badana())



def book_list(request):
    books = Book.objects.all()
    return render(request,"todo_app/book_list.html",{"books": books})

def upload_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form= BookForm()
    return render(request,"todo_app/upload_book.html", {"form":form})


def delete_book(request,pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'
