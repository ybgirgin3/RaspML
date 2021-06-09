# NDVI-analizi-Django-project
Batuhan

# NDVI-analizi-Django-project
TARNET

Django için ayrı bir virutual machine oluşturmak daha yararlı oluyor çünkü karışma olasılığıyla karşılaşabiliriz bunu nasıl yapacağız

masaüstüne klasörümüzü açıyoruz burası bizim çalışma ortamımız olacak


pip install virtualenv 

komutu ile bir sanal ortam kuruyoruz


virtualenv Sanalortamadi 


ile kendimize sanal ortam olusturuyoruz
konsolumuz ile sanal ortam içindeki Scripts klasöründeki activate.bat dosyasını çalıştırıyoruz


Sanalortamadi/Scripts/activate


bu sayede elimizdeki sanal ortamda çalışacağız artık

artık kütüphaneleri kurabiliriz
projemiz için aşağıdaki kütüphanelerin kurulu olması gerekiyor

Kurulması gereken kütüphaneler


python -m pip install Django


pip install sentinelsat



pip install Archive



pip install rasterio ya da conda install -c conda-forge rasterio


pip install pandas


pip install numpy


pip install pip-date


pip install matplotlib


kütüphanelerimizi kurduk şimdi projemizi çalıştıracağız

verdiğim dosyaları bir klasör halinde aktarmadan önce 

ana klasörde bir yere girmeden şu kodu yazıyoruz



django-admin startproject mysite



ardından benim dosyalarımı mysite kısmına atıyoruz

ardınan manage.py olan kısma geliyoruz mysite içine




python manage.py runserver 




ile sanal sunucumuz başlıyor ve bu şekilde sisteme giriş yapabiliyoruz.


