# -*- coding: utf-8 -*-
import sys
import six
import os
import re
from kodi_six import xbmc
if six.PY3:
    from http.server import HTTPServer
    from http.server import SimpleHTTPRequestHandler
else:
    from BaseHTTPServer import HTTPServer    
    from SimpleHTTPServer import SimpleHTTPRequestHandler
import threading
import requests
import time

#http://127.0.0.1:65110/elgatito/addons/addons.xml

PORT = 65110 
global addons_xml
addons_xml = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addons>
<addon id="plugin.video.elementum" name="Elementum" version="0.1.86" provider-name="elgatito">
    <requires>
        <import addon="xbmc.addon" version="16.0.0" />
        <import addon="repository.elementum" optional="true" />
        <import addon="script.module.kodi-six" />
        <import addon="script.module.requests" />
    </requires>
    <extension point="xbmc.python.pluginsource" library="navigation.py">
        <provides>video</provides>
    </extension>
    <extension point="xbmc.service" library="service.py" start="startup" />
    <extension point="xbmc.python.module" library="resources/site-packages" />
    <extension point="xbmc.subtitle.module" library="navigation.py" />
    <extension point="xbmc.addon.metadata">
        <summary lang="ru">Elementum: Стриминг видео</summary>
        <summary lang="en">Elementum: Media streaming</summary>
        <summary lang="hr">Elementum: Medijsko strujanje</summary>
        <summary lang="es">Elementum: Transmisión de medios</summary>
        <summary lang="sv">Elementum: medieströmning</summary>
        <description lang="ru">Elementum это дополнение для поиска и воспроизведения торрентов. Дополнение не ходит на запрещенные сайты самостоятельно. Хотя, для поиска используются дополнения (называемые провайдерами), которые устанавливаются отдельно.[CR]Этот проект является ответвлением хорошо извесных, но не поддерживаемых Pulsar/Quasar от steeve и scakemyer.</description>
        <description lang="en">Elementum is a torrent finding and streaming engine. It doesn't go on torrent websites for legal reasons. However, it calls specially crafted add-ons (called providers) that are installed separately.[CR]This project is a fork of the well known, but no longer maintained Pulsar/Quasar projects from steeve and scakemyer.</description>
        <description lang="hr">Elementum je pogon pretraživanja i strujanja. Ne posjećuje torrent web stranice iz pravnih razloga. Ipak, koristi posebno napravljene dodatke (nazvane pružatelji usluge) koji su instalirani odvojeno.[CR]Ovaj projekt je ogranak dobro poznatih, ali više ne održavanih Pulsar/Quasar projekata od autora steevea i scakemyera.</description>
        <description lang="es">Elementum es un motor de búsqueda y transmisión torrent. No navega por sitios web torrent por razones legales. Sin embargo, llama a complementos especialmente diseñados para ello (denominados providers o proveedores) que se instalan por separado.[CR]Este proyecto es un fork de los bien conocidos, pero ya sin soporte proyectos Pulsar/Quasar de steeve y scakemyer.[CR]</description>
        <description lang="sv">Elementum är en torrentsöknings- och strömningsmotor. Det går inte till torrentwebbplatser av juridiska skäl. Den anropar dock speciellt utformade tillägg (kallade leverantörer) som installeras separat.[CR]Detta projekt är en förgrening av de välkända, men inte längre underhållna Pulsar/Quasar-projekten av steeve och scakemyer. </description>
        <disclaimer lang="ru">Автор дополнения не несёт ответственности за скачивание или поиск информации и содержимого в этом дополнении. Автор никак не связан с Kodi, командой Kodi, или XBMC Foundation.</disclaimer>
        <disclaimer lang="en">The author does not own or host any content found within this Addon. The author is not connected to or in any other way affiliated with Kodi, Team Kodi, or the XBMC Foundation.</disclaimer>
        <disclaimer lang="hr">Autor ovog dodatka ne posjeduje i ne distribuira bilo kakav sadržaj koji je pronađen. Autor nije povezan sa ili na bilo koji drugi način bilo sa Kodijem, Team Kodijem ili XBMC fundacijom.</disclaimer>
        <disclaimer lang="es">El autor no posee ni aloja ningún contenido que se encuentre a través de este complemento. El autor no está unido ni relacionado de ninguna manera con Kodi, Team Kodi, o XBMC Foundation.</disclaimer>
        <disclaimer lang="sv">Skaparen äger inte eller är värd av något innehåll som finns i detta tillägg. Författaren är inte ansluten till eller på något annat sätt en del av Kodi, Team Kodi eller XBMC Foundation.</disclaimer>
        <language>en el es de fi fr he hr it nl pt ro sk sv</language>
        <platform>all</platform>
        <website>http://elementum.surge.sh/</website>
        <source>https://github.com/elgatito/plugin.video.elementum</source>
        <forum></forum>
        <license>Non commercial. See https://github.com/elgatito/plugin.video.elementum/blob/master/LICENSE</license>
        <assets>
            <icon>icon.png</icon>
            <fanart>fanart.jpg</fanart>
            <screenshot>resources/screenshots/home.png</screenshot>
            <screenshot>resources/screenshots/movies.png</screenshot>
            <screenshot>resources/screenshots/webui.png</screenshot>
        </assets>
    </extension>
</addon>
<addon id="script.elementum.burst" name="Elementum [COLOR FFFF6B00]Burst[/COLOR]" version="0.0.72" provider-name="elgatito">
    <requires>
        <import addon="xbmc.addon" version="16.0.0" />
        <import addon="plugin.video.elementum" optional="true"/>
        <import addon="script.module.kodi-six" />
        <import addon="script.module.requests" />
        <import addon="script.module.future" version="0.16.0.4"/>
    </requires>
    <extension point="xbmc.python.script" library="burst.py">
        <provides>executable</provides>
    </extension>
    <extension point="xbmc.addon.metadata">
        <summary lang="en">Elementum torrents provider</summary>
        <summary lang="hr">Elementum torrent pružatelji usluga</summary>
        <summary lang="es">Proveedor de torrents Elementum</summary>
        <summary lang="ru">Поисковое дополнение Elementum</summary>
        <summary lang="sv">Elementum-torrentleverantör</summary>
        <description lang="en">Elementum Burst is a lean and mean multi-provider for Elementum.</description>
        <description lang="hr">Elementum Burst je višestruki pružatelj usluga za Elementum.</description>
        <description lang="es">Elementum Burst es un multi-proveedor simple y eficiente para Elementum.</description>
        <description lang="ru">Elementum Burst это поисковое дополнение, для поиска торрентов для Elementum.</description>
        <description lang="sv">Elementum Burst är en enkel och effektiv multi-leverantör för Elementum.</description>
        <disclaimer lang="en">The author does not host or distribute any of the content displayed by this addon. The author does not have any affiliation with the content providers.</disclaimer>
        <disclaimer lang="hr">Autor ovog dodatka ne posjeduje i ne distribuira bilo kakav sadržaj koji je pronađen. Autor nije povezan sa bilo kojim izvorom sadržaja.</disclaimer>
        <disclaimer lang="es">El autor no aloja ni distribuye ninguno de los contenidos mostrados por este complemento. El autor no tiene ninguna afiliación con los proveedores de contenido.</disclaimer>
        <disclaimer lang="ru">Автор не несёт ответственности за использование дополнения, не распространяет данные, выводимые дополнением.</disclaimer>
        <disclaimer lang="sv">Skaparen är inte värd eller distribuerar något av innehållet som visas av detta tillägg. Skaparen har ingen anslutning till innehållsleverantörerna.</disclaimer>
        <license>WTFPL, Version 2, December 2004. See included LICENSE.</license>
        <website>https://elementum.surge.sh</website>
        <source>https://github.com/elgatito/script.elementum.burst</source>
        <forum>TODO</forum>
        <assets>
            <icon>icon.png</icon>
            <fanart>fanart.jpg</fanart>
        </assets>
    </extension>
</addon>
<addon id="context.elementum" name="Elementum Context Helper" version="0.0.10" provider-name="elgatito">
    <requires>
        <import addon="xbmc.addon" version="16.0.0" />
        <import addon="script.module.requests"/>
        <import addon="plugin.video.elementum" optional="true"/>
        <import addon="script.module.future" version="0.16.0.4"/>
    </requires>
    <extension point="kodi.context.item">
        <menu id="kodi.core.main">
            <menu>
                <label>32011</label>
                <item library="context_play.py">
                    <label>32000</label>
                    <visible>StringCompare(ListItem.dbtype,movie) | StringCompare(ListItem.dbtype,episode) | StringCompare(ListItem.dbtype,season) | String.IsEqual(ListItem.dbtype,movie) | String.IsEqual(ListItem.dbtype,episode) | String.IsEqual(ListItem.dbtype,season)</visible>
                </item>
                <item library="context_download.py">
                    <label>32012</label>
                    <visible>StringCompare(ListItem.dbtype,movie) | StringCompare(ListItem.dbtype,episode) | StringCompare(ListItem.dbtype,season) | String.IsEqual(ListItem.dbtype,movie) | String.IsEqual(ListItem.dbtype,episode) | String.IsEqual(ListItem.dbtype,season)</visible>
                </item>
                <item library="context_assign.py">
                    <label>32002</label>
                    <visible>StringCompare(ListItem.dbtype,movie) | StringCompare(ListItem.dbtype,episode) | StringCompare(ListItem.dbtype,season) | String.IsEqual(ListItem.dbtype,movie) | String.IsEqual(ListItem.dbtype,episode) | String.IsEqual(ListItem.dbtype,season)</visible>
                </item>
                <item library="context_library.py" args="remove">
                    <label>32017</label>
                    <visible>Integer.IsGreater(ListItem.DBID,0)+[StringCompare(ListItem.dbtype,movie) | StringCompare(ListItem.dbtype,tvshow) | String.IsEqual(ListItem.dbtype,movie) | String.IsEqual(ListItem.dbtype,tvshow)]</visible>
                </item>
                <item library="context_trakt.py" args="watched">
                    <label>32018</label>
                    <visible>[Integer.IsGreater(ListItem.DBID,0) | Integer.IsGreater(ListItem.UniqueID(tmdb),0)]+Integer.IsEqual(ListItem.PlayCount,0)+[StringCompare(ListItem.dbtype,movie) | StringCompare(ListItem.dbtype,episode) | StringCompare(ListItem.dbtype,season) | StringCompare(ListItem.dbtype,tvshow) | String.IsEqual(ListItem.dbtype,movie) | String.IsEqual(ListItem.dbtype,episode) | String.IsEqual(ListItem.dbtype,season) | String.IsEqual(ListItem.dbtype,tvshow)]</visible>
                </item>
                <item library="context_trakt.py" args="unwatched">
                    <label>32019</label>
                    <visible>[Integer.IsGreater(ListItem.DBID,0) | Integer.IsGreater(ListItem.UniqueID(tmdb),0)]+Integer.IsGreater(ListItem.PlayCount,0)+[StringCompare(ListItem.dbtype,movie) | StringCompare(ListItem.dbtype,episode) | StringCompare(ListItem.dbtype,season) | StringCompare(ListItem.dbtype,tvshow) | String.IsEqual(ListItem.dbtype,movie) | String.IsEqual(ListItem.dbtype,episode) | String.IsEqual(ListItem.dbtype,season) | String.IsEqual(ListItem.dbtype,tvshow)]</visible>
                </item>
                <item library="context_info.py">
                    <label>32001</label>
                    <visible>System.GetBool(debug.extralogging)+[StringCompare(ListItem.dbtype,movie) | StringCompare(ListItem.dbtype,episode) | StringCompare(ListItem.dbtype,season) | StringCompare(ListItem.dbtype,tvshow) | String.IsEqual(ListItem.dbtype,movie) | String.IsEqual(ListItem.dbtype,episode) | String.IsEqual(ListItem.dbtype,season) | String.IsEqual(ListItem.dbtype,tvshow)]</visible>
                </item>
            </menu>
        </menu>
    </extension>
    <extension point="kodi.addon.metadata">
        <summary lang="ru">Elementum Контекстное меню</summary>
        <summary lang="en">Elementum Context Menu</summary>
        <description lang="ru">Контекстное меню для Elementum.</description>
        <description lang="en">Context Menu for Elementum.</description>
        <disclaimer lang="ru">Автор не несёт ответственности за использование дополнения, не распространяет данные, выводимые дополнением.</disclaimer>
        <disclaimer lang="en">The author is not responsible for addon usage and does not host or distribute any of the content displayed by this addon.</disclaimer>
        <license>WTFPL, Version 2, December 2004. See included LICENSE.</license>
        <website>https://elementum.surge.sh</website>
        <source>https://github.com/elgatito/context.elementum</source>
        <forum></forum>
    </extension>
</addon>
</addons>
'''

elementum_icon = 'https://github.com/elgatito/plugin.video.elementum/raw/master/icon.png'
elementum_fanart = 'https://github.com/elgatito/plugin.video.elementum/raw/master/fanart.png'
elementum_url = 'https://github.com/elgatito/plugin.video.elementum/releases/download/v0.1.86/plugin.video.elementum-0.1.86.zip'
path_elementum = '/elgatito/addons/zips/' + re.findall('elgatito/(.*?)/',elementum_url)[0] + '/' + elementum_url.split('/')[-1]

burst_url = 'https://github.com/elgatito/script.elementum.burst/releases/download/v0.0.72/script.elementum.burst-0.0.72.zip'
path_burst = '/elgatito/addons/zips/' + re.findall('elgatito/(.*?)/',burst_url)[0] + '/' + burst_url.split('/')[-1]

context_url = 'https://github.com/elgatito/context.elementum/releases/download/v0.0.10/context.elementum-0.0.10.zip'
path_context = '/elgatito/addons/zips/' + re.findall('elgatito/(.*?)/',context_url)[0] + '/' + context_url.split('/')[-1]

def md5_generator(addons_xml):
    try:
        import md5
        m = md5.new(addons_xml).hexdigest()
    except ImportError:
        import hashlib
        m = hashlib.md5(addons_xml.encode("UTF-8", "IGNORE")).hexdigest()
    return m   


class handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/elgatito/addons/addons.xml.md5":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            if six.PY3:
                self.wfile.write(bytes(md5_generator(addons_xml.strip()), "utf8"))
            else:
                self.wfile.write(md5_generator(addons_xml.strip()))
        elif self.path == "/elgatito/addons/addons.xml":
            self.send_response(200)
            self.send_header("Content-type", "application/xml")
            self.end_headers()    
            if six.PY3:                
                self.wfile.write(bytes(addons_xml.strip(), "utf8"))
            else:
                self.wfile.write(addons_xml.strip())
        elif self.path == path_elementum: #/elgatito/addons/zips/
            try:
                response = requests.get(elementum_url, stream=True, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
                file_size = int(response.headers["Content-Length"])
                self.send_response(200)
                self.send_header("Content-type", "application/zip")
                self.send_header("Content-Length", file_size)
                self.end_headers()
                for chunk in response.iter_content(chunk_size=8024):
                    self.wfile.write(chunk)
            except:
                self.send_error(404)
        elif 'icon.png' in self.path and 'plugin.video.elementum' in self.path:
            try:
                response = requests.get(elementum_icon, stream=True, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
                file_size = int(response.headers["Content-Length"])
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.send_header("Content-Length", file_size)
                self.end_headers()
                for chunk in response.iter_content(chunk_size=1024):
                    self.wfile.write(chunk)
            except:
                self.send_error(404)
        elif 'fanart.png' in self.path and 'plugin.video.elementum' in self.path:
            try:
                response = requests.get(elementum_fanart, stream=True, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
                file_size = int(response.headers["Content-Length"])
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.send_header("Content-Length", file_size)
                self.end_headers()
                for chunk in response.iter_content(chunk_size=1024):
                    self.wfile.write(chunk)
            except:
                self.send_error(404)                               
        elif self.path == path_burst: #/elgatito/addons/zips/
            try:
                response = requests.get(burst_url, stream=True, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
                file_size = int(response.headers["Content-Length"])
                self.send_response(200)
                self.send_header("Content-type", "application/zip")
                self.send_header("Content-Length", file_size)
                self.end_headers()
                for chunk in response.iter_content(chunk_size=1024):
                    self.wfile.write(chunk)
            except:
                self.send_error(404)                                
        elif self.path == path_context: #/elgatito/addons/zips/
            try:
                response = requests.get(context_url, stream=True, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
                file_size = int(response.headers["Content-Length"])
                self.send_response(200)
                self.send_header("Content-type", "application/zip")
                self.send_header("Content-Length", file_size)
                self.end_headers()
                for chunk in response.iter_content(chunk_size=1024):
                    self.wfile.write(chunk)
            except:
                self.send_error(404)                                
        elif self.path == '/':
            message = 'Repository Elementum'
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            if six.PY3:                
                self.wfile.write(bytes(message, "utf8"))
            else:
                self.wfile.write(message)
        else:
            self.send_error(404)


httpd = HTTPServer(('', PORT), handler)
def serve_forever(httpd):
    httpd.serve_forever()
    #httpd.handle_request()
    # with httpd:  # to make sure httpd.server_close is called
    #     httpd.serve_forever()#

class reposerver:
    def __init__(self):
        self.server = threading.Thread(target=serve_forever, args=(httpd, ))
    def start(self):
        self.server.start()
    def stop(self):
        httpd.shutdown()

reposerver().start()
time.sleep(5)
monitor = xbmc.Monitor()
while True:
    if monitor.abortRequested():
        reposerver().stop()
        break
sys.exit(0)
