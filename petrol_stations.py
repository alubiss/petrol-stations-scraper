#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from collections import OrderedDict
driver = webdriver.Chrome()
driver.get("https://www.wspolrzedne-gps.pl/")


# In[ ]:


driver.get("https://www.google.com/search?sxsrf=ACYBGNQsCSXtIr9hLhvgXb51yrt8GU1drQ:1568129086326&q=circle&npsic=0&rflfq=1&rlha=0&rllag=52161572,21064468,2055&tbm=lcl&ved=2ahUKEwiRzpuJyMbkAhWMlosKHdJ3CygQtgN6BAgKEAQ&tbs=lrf:!2m4!1e17!4m2!17m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:4&rldoc=1#rlfi=hd:;si:;mv:!1m2!1d52.301482199999995!2d21.2360275!2m2!1d52.133469299999994!2d20.8924046;tbs:lrf:!2m1!1e3!2m4!1e17!4m2!17m1!1e2!3sIAE,lf:1,lf_ui:4")
dane2= pd.DataFrame({'adres stacji':[],'wielkosc ruchu':[],'godziny otwarcia':[], 'liczba gwiazdek': [], "sredni ruch poniedzialek": [], "sredni ruch wtorek": [], "sredni ruch sroda": [], "sredni ruch czwartek": [], "sredni ruch piatek": [], "sredni ruch sobota": [], "sredni ruch niedziela": [], "udział poniedzialek": [], "udział wtorek": [], "udział sroda": [], "udział czwartek": [], "udział piatek": [], "udział sobota": [], "udział niedziela": [], "średni spędzany czas (min)": [], "sredni ruch w godzinach 4-8":[], "sredni ruch w godzinach 8-12":[], "sredni ruch w godzinach 12-16":[],"sredni ruch w godzinach 16-20":[],"sredni ruch w godzinach 20-24":[],"sredni ruch w godzinach 24-4":[]})
dane=pd.DataFrame({'godziny':[],'wielkosc ruchu':[],'opis ruchu':[], "dzień tygodnia": [], "adres":[]}) 


# In[199]:


stacje =["circle warszawa", "BP warszawa", "orlen warszawa", "Shell warszawa", "lotos warszawa", "moya warszawa"]
adres=[]
otwarcie=[]
godziny=[]
ruch=[]
ruch_slupki=[]
stars=[]
dzien=[]
href=[]
link=driver.page_source
soup=BeautifulSoup(link,"html.parser")
adr= soup.find("span",{"class":"LrzXr"}).text.strip()
adres.append(adr)
otw= soup.find("span",{"class":"vyFVZe"}).text.strip()
otwarcie.append(otw)
strs= soup.find("span",{"class":"Aq14fc"}).text.strip()
stars.append(strs)
godz = soup.find_all("div",{"class":"lubh-bar"})
for item in godz:
        item3=item["aria-label"]
        item3=item3[item3.find(":")+4:]
        ruch.append(item3)
        item2=item["aria-label"]
        item2=item2[:item2.find(":")+3]
        godziny.append(item2)
        item=item["style"]
        item=item[item.find("h")+7:item.find("p")]
        item=item.strip()
        item=int(item)
        ruch_slupki.append(item)
dzien_tyg=['poniedzialek', 'wtorek', 'sroda', 'czwartek', 'piatek', 'sobota', 'niedziela']
for k in range(0,len(dzien_tyg)):
    dzien += 24 * [dzien_tyg[k]]
czas= soup.find("div",{"class":"UYKlhc"}).find_next('b').text.strip()
czas=czas[0:2]
dzien=dzien[0:len(godziny)]
ramka=pd.DataFrame({'godziny':godziny,'wielkosc ruchu':ruch_slupki,'opis ruchu':ruch, "dzień tygodnia": dzien}) #"adres":adress, "stacja": stacjas}) 
# ile pustych
#print(ramka.isnull().sum())
ramka3 = ramka.groupby('dzień tygodnia')
tab= ramka3.apply(lambda x: x['wielkosc ruchu'].sum())
print(tab)
całkowity_ruch=ramka['wielkosc ruchu'].sum()
ramka2= pd.DataFrame({'adres stacji':adres,'godziny otwarcia':otwarcie, 'liczba gwiazdek': stars, "sredni ruch poniedzialek": tab[0], "sredni ruch wtorek": tab[1], "sredni ruch sroda": tab[2], "sredni ruch czwartek": tab[3], "sredni ruch piatek": tab[4], "sredni ruch sobota": tab[5], "sredni ruch niedziela": tab[6], "udział poniedzialek": tab[0]/całkowity_ruch, "udział wtorek": tab[1]/całkowity_ruch, "udział sroda": tab[2]/całkowity_ruch, "udział czwartek": tab[3]/całkowity_ruch, "udział piatek": tab[4]/całkowity_ruch, "udział sobota": tab[5]/całkowity_ruch, "udział niedziela": tab[6]/całkowity_ruch, "średni spędzany czas (min)": czas}) 
adress=adres*len(ramka)
ramka=pd.DataFrame({'godziny':godziny,'wielkosc ruchu':ruch_slupki,'opis ruchu':ruch, "dzień tygodnia": dzien, "adres":adress})
godzinowa_wielkosc_ruchu=ramka.groupby(['godziny']).sum()
godzinowa_wielkosc_ruchu["godzina"]=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
godzinowa_wielkosc_ruchu.plot(x="godzina", y="wielkosc ruchu")
ruch4_8 = godzinowa_wielkosc_ruchu["wielkosc ruchu"].where(godzinowa_wielkosc_ruchu['godzina'] == 4 | 5 | 6| 7).sum()
ruch8_12=godzinowa_wielkosc_ruchu["wielkosc ruchu"].where(godzinowa_wielkosc_ruchu['godzina'] == 8 | 9 | 10| 11).sum()
ruch12_16=godzinowa_wielkosc_ruchu["wielkosc ruchu"].where(godzinowa_wielkosc_ruchu['godzina'] == 12 | 13 | 14| 15).sum()
ruch16_20=godzinowa_wielkosc_ruchu["wielkosc ruchu"].where(godzinowa_wielkosc_ruchu['godzina'] == 16 | 17 | 18| 19).sum()
ruch20_24=godzinowa_wielkosc_ruchu["wielkosc ruchu"].where(godzinowa_wielkosc_ruchu['godzina'] == 20 | 21 | 22| 23).sum()
ruch24_4=godzinowa_wielkosc_ruchu["wielkosc ruchu"].where(godzinowa_wielkosc_ruchu['godzina'] == 0 | 1 | 2| 3).sum()
ramka2= pd.DataFrame({'adres stacji':adres,'wielkosc ruchu':całkowity_ruch,'godziny otwarcia':otwarcie, 'liczba gwiazdek': stars, "sredni ruch poniedzialek": tab[0], "sredni ruch wtorek": tab[1], "sredni ruch sroda": tab[2], "sredni ruch czwartek": tab[3], "sredni ruch piatek": tab[4], "sredni ruch sobota": tab[5], "sredni ruch niedziela": tab[6], "udział poniedzialek": tab[0]/całkowity_ruch, "udział wtorek": tab[1]/całkowity_ruch, "udział sroda": tab[2]/całkowity_ruch, "udział czwartek": tab[3]/całkowity_ruch, "udział piatek": tab[4]/całkowity_ruch, "udział sobota": tab[5]/całkowity_ruch, "udział niedziela": tab[6]/całkowity_ruch, "średni spędzany czas (min)": czas, "sredni ruch w godzinach 4-8":ruch4_8, "sredni ruch w godzinach 8-12":ruch8_12, "sredni ruch w godzinach 12-16":ruch12_16,"sredni ruch w godzinach 16-20":ruch16_20,"sredni ruch w godzinach 20-24":ruch20_24,"sredni ruch w godzinach 24-4":ruch24_4})
dane=pd.concat([ramka,dane])
dane2=pd.concat([ramka2, dane2])


# In[200]:


#dane=pd.concat([ramka,dane])
#dane2=pd.concat([ramka2, dane2])
dane2


# In[201]:


dane.to_excel("moya.xls")
dane2.to_excel("moya2.xls")


# In[4]:


dane = pd.read_excel(io="dane.xlsx")


# In[ ]:


# uzyskanie współrzędnych


# In[146]:


x=[]
y=[]


# In[147]:


for stacja in dane["adres stacji"]:
    link=driver.page_source
    soup=BeautifulSoup(link,"html.parser")
    try:
        adres= driver.find_element_by_xpath('//*[@id="address"]')
        adres.click()
        adres.clear()
        adres.send_keys(stacja)
        go= driver.find_element_by_xpath('//*[@id="wrap"]/div[2]/div[3]/div[1]/form[1]/div[2]/div/button')
        go.click()
        time.sleep(3)
        link=driver.page_source
        soup=BeautifulSoup(link,"html.parser")
        szer= soup.find("div",{"id":"info_window"}).text.strip()
        szer=szer[szer.find("Szerokość geograficzna: ")+24:szer.find("|")-1]
        szer=float(szer)
        dl= soup.find("div",{"id":"info_window"}).text.strip()
        dl=dl[dl.find("Długość geograficzna: ")+22:dl.find("Długość geograficzna: ")+31]
        dl=float(dl)
        x.append(dl)
        y.append(szer)
    except:
        szer=None
        dl=None
        y.append(szer)
        x.append(dl)


# In[151]:


ramka= pd.DataFrame({'x':x,'y':y})


# In[153]:


dane = dane.append(ramka, ignore_index=True)


# In[154]:


dane


# In[ ]:


dane.to_excel("dane.xls")

