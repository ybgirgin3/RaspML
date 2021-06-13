from django.db import models
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import numpy as np
import pandas as pd
import rasterio
import os
from archive import Archive

from django.core.files import File

kappa=("kappa burada")

import matplotlib.pyplot as plt
import matplotlib.colors as colors
# Create your models here.

class backend(models.Model):
    adana=("burası about sayfası için python kodu çalıştıran kod backend içinde")
    def badana(self):
        global kappa
        kappa=1
        self.deneme="badana içine girdiğini gösteren kod"
        print(self.deneme)
        print(self.adana)
        api = SentinelAPI('flavves', 'ŞİFRE', 'https://scihub.copernicus.eu/dhus')
        footprint = geojson_to_wkt(read_geojson('media/map.geojson'))
        print(footprint)
        self.products = api.query(footprint,date=('20191219', date(2019, 12, 29)),platformname='Sentinel-2')
        products_df = api.to_dataframe(self.products)
        print("oluyor galiba")
        self.products_df_sorted = products_df.sort_values(['cloudcoverpercentage', 'ingestiondate'], ascending=[True, True])
        self.products_df_sorted = self.products_df_sorted.head(1)



        self.df=self.products_df_sorted
        self.NotDefteriKaydi = self.df.values.tolist()
        self.str_denemesi=str(self.NotDefteriKaydi)

        self.Kaydetmeye_basla=list(self.str_denemesi.split(","))
        self.yerler=[0,7,8,9,12,14,18,19,20]
        self.isimler=["Dosya adı:","Uydu adı","Dosya boyutu","Çekim tarihi","Orbit numarası","Bulut yüzdesi","vejetasyon yüzdesi","su yüzdesi","not vejetasyon yüzdesi"]
        self.i=0
        with open("media/books/txt/deneme.txt", "w") as self.dosya:
            for self.sira in self.yerler:   
                print(self.isimler[self.i]+":"+self.Kaydetmeye_basla[self.sira])
                self.yaz=(self.isimler[self.i]+":"+self.Kaydetmeye_basla[self.sira])
                self.i=self.i+1
                self.dosya.write(self.yaz)
                self.dosya.write("\n")
        self.dosya.close()
        



        print(self.products_df_sorted)
        print("indirme başladı")
        #burasını blockladım çünkü 1 gb arşiv indiriyor
        #api.download_all(self.products_df_sorted.index)
        print("indirme bitti")
        self.veri_cekme=self.products_df_sorted.index
        self.veri_cekme1=self.veri_cekme[0]

        """
        Bu işlem arşivden çıkarmak için gerekli arşivin adı indirdiğimiz verinin title adı oluyor

        """
        self.arsiv_adi=api.get_product_odata(self.veri_cekme1)
        self.arsiv_adi=self.arsiv_adi["title"]
        self.arsiv_adi=str(self.arsiv_adi)
        print(self.arsiv_adi)
                
        
        self.a = Archive(self.arsiv_adi+'.zip')
        self.a.extract()
        self.img_data_klasor_ismi=os.listdir((self.arsiv_adi+".SAFE"+'/GRANULE'))
        self.img_data_klasor_ismi=self.img_data_klasor_ismi[0]
        self.img_data_klasor_ismi=str(self.img_data_klasor_ismi)
        self.dosya_yer_=(self.arsiv_adi+".SAFE"+'/GRANULE/'+self.img_data_klasor_ismi+'/IMG_DATA')
        self.resim_isim=os.listdir(self.dosya_yer_)
        print(self.dosya_yer_)

        """
        şimdi ise resimleri rasterio ile bi kullanalım

        """

        if self.resim_isim == "R10m" or "R20m" or "R60m":
            self.dosya_yer_=(self.arsiv_adi+".SAFE"+'/GRANULE/'+self.img_data_klasor_ismi+'/IMG_DATA/R60m')
            self.resim_isim=os.listdir(self.dosya_yer_)
            self.resim_isim[2]
            self.resim_isim[3]
                
            self.jp2ler = [self.resim_isim[2],self.resim_isim[3]]
            self.bands = []
            
            #burası bizim jp2 dosyalarımızı okuyacak
            
            for self.jp2 in self.jp2ler:
                with rasterio.open(self.dosya_yer_+"/"+self.jp2) as self.f:
                    self.bands.append(self.f.read(1))
            
            #resimlerimizi ayrıştırdık özel bantlara
            
            self.band_red=self.bands[0]
            self.band_nir=self.bands[1]
            print("bant değerleri hesaplandı")
            print(self.bands[0],self.bands[1])
        else:
        
            self.resim_isim[2]
            self.resim_isim[3]
            
            
            self.jp2ler = [self.resim_isim[2],self.resim_isim[3]]
            self.bands = []
            
            #burası bizim jp2 dosyalarımızı okuyacak
            
            for self.jp2 in self.jp2ler:
                with rasterio.open(self.dosya_yer_+"/"+self.jp2) as f:
                    self.bands.append(self.f.read(1))
            
            #resimlerimizi ayrıştırdık özel bantlara
            self.band_red=self.bands[0]
            self.band_nir=self.bands[1]
            print("bant değerleri hesaplandı")
            print(self.bands[0],self.bands[1])
                        
        # Klasik NDVI denklemi ile hesaplama
        print("ndvı hesaplanıyor")
        np.seterr(divide='ignore', invalid='ignore')

        # Calculate NDVI. This is the equation at the top of this guide expressed in code
        self.ndvi = (self.band_nir.astype(float) - self.band_red.astype(float)) / (self.band_nir + self.band_red)
        #su için yapıyorum bu analizi
        ##
        ###
        self.ndvi=(self.band_red.astype(float) - self.band_nir.astype(float)) / (self.band_red + self.band_nir)
        ###
        ###
        np.nanmin(self.ndvi), np.nanmax(self.ndvi)
        print("ndvı değerler aralıkları")
        print(np.nanmin(self.ndvi), np.nanmax(self.ndvi))


        

        

        # görüntümüze bakalım renklerine ayrılmış bir görüntümüz var
        # çizim yapacağız bunun için gerekli kütüphaneler ekleniyor

        # NDVI bilindiği üzere 1 ve -1 arasındaki değerlerde sınıflandırılır.
        # Biz de bu değerleri renklerle göstermek istiyoruz.
        # Bunun için alınan sayısal değerleri farklı renk spektrumlarına atayarak elimizde NDVI için renklendirilmiş bir görüntümüz olacaktır
        # 
        # Bir orta nokta belirledik ve bu sola ve sağa olacak şekilde renklendiriyoru renk spekturumunu da aşağıda paylaşacağım

        class RenkNormalizasyonu(colors.Normalize):
        
            def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
                self.midpoint = midpoint
                colors.Normalize.__init__(self, vmin, vmax, clip)

            def __call__(self, value, clip=None):

                x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
                return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))

        self.min=np.nanmin(self.ndvi)
        self.max=np.nanmax(self.ndvi)
        self.mid=0.1
        print("bitti mi şimdi")
        print(self.min,self.max)

                
        self.fig = plt.figure(figsize=(20,10))
        self.ax = self.fig.add_subplot(111)

        self.cmap = plt.cm.RdYlGn 

        self.cax = self.ax.imshow(self.ndvi, cmap=self.cmap, clim=(self.min, self.max), norm=RenkNormalizasyonu(midpoint=self.mid,vmin=self.min, vmax=self.max))

        self.ax.axis('off')
        self.ax.set_title('NDVI görüntüsü', fontsize=18, fontweight='bold')

        self.cbar = self.fig.colorbar(self.cax, orientation='horizontal', shrink=0.65)
        #normalde byu alttaki gibi kaydetsin ama şimdilik benim yazdığım gibi yapsın olur mu cnm muck
        #self.fig_kaydet="resimler/"+self.resim_isim[2]+".tif"
        self.fig_kaydet="media/books/covers/denemeresmi.png"
        self.fig.savefig(self.fig_kaydet, dpi=200, bbox_inches='tight', pad_inches=0.7)
        self.fig_kaydet_tif="media/books/covers/denemeresmi.tif"
        self.fig.savefig(self.fig_kaydet_tif, dpi=200, bbox_inches='tight', pad_inches=0.7)



class deneme(models.Model):
    denemeyazisi=("bi ol")

class Book(models.Model):
    tarih = models.CharField(max_length=100)
    author = models.FileField(upload_to="books/geojsons/")
    pdf = models.FileField(upload_to="books/tifs/")
    cover = models.ImageField(upload_to="books/covers", null=True, blank=True)
    myfile = ('media/books/tifs/ndviresim_osS9Jvz.png')
    
    


    def __str__(self):
        return self.tarih
    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, ** kwargs)
