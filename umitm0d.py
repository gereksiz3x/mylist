import requests
import re
import sys
import json

# Terminal renkleri
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Kanallar listesi (başına ÜmitM0d eklenecek)
KANALLAR = [
    {"dosya": "yayinzirve.m3u8", "tvg_id": "BeinSports1.tr", "kanal_adi": "Bein Sports 1 HD (VIP)"},
    {"dosya": "yayin1.m3u8", "tvg_id": "BeinSports1.tr", "kanal_adi": "Bein Sports 1 HD"},
    {"dosya": "yayinb2.m3u8", "tvg_id": "BeinSports2.tr", "kanal_adi": "Bein Sports 2 HD"},
    {"dosya": "yayinb3.m3u8", "tvg_id": "BeinSports3.tr", "kanal_adi": "Bein Sports 3 HD"},
    {"dosya": "yayinb4.m3u8", "tvg_id": "BeinSports4.tr", "kanal_adi": "Bein Sports 4 HD"},
    {"dosya": "yayinb5.m3u8", "tvg_id": "BeinSports5.tr", "kanal_adi": "Bein Sports 5 HD"},
    {"dosya": "yayinbm1.m3u8", "tvg_id": "BeinMax1.tr", "kanal_adi": "Bein Max 1 HD"},
    {"dosya": "yayinbm2.m3u8", "tvg_id": "BeinMax2.tr", "kanal_adi": "Bein Max 2 HD"},
    {"dosya": "yayinss.m3u8", "tvg_id": "SSport1.tr", "kanal_adi": "S Sport 1 HD"},
    {"dosya": "yayinss2.m3u8", "tvg_id": "SSport2.tr", "kanal_adi": "S Sport 2 HD"},
    {"dosya": "yayinssp2.m3u8", "tvg_id": "SSportPlus.tr", "kanal_adi": "S Sport Plus HD"},
    {"dosya": "yayint1.m3u8", "tvg_id": "TivibuSpor1.tr", "kanal_adi": "Tivibu Spor 1 HD"},
    {"dosya": "yayint2.m3u8", "tvg_id": "TivibuSpor2.tr", "kanal_adi": "Tivibu Spor 2 HD"},
    {"dosya": "yayint3.m3u8", "tvg_id": "TivibuSpor3.tr", "kanal_adi": "Tivibu Spor 3 HD"},
    {"dosya": "yayinsmarts.m3u8", "tvg_id": "SmartSpor1.tr", "kanal_adi": "Smart Spor 1 HD"},
    {"dosya": "yayinsms2.m3u8", "tvg_id": "SmartSpor2.tr", "kanal_adi": "Smart Spor 2 HD"},
    {"dosya": "yayintrtspor.m3u8", "tvg_id": "TRTSpor.tr", "kanal_adi": "TRT Spor HD"},
    {"dosya": "yayintrtspor2.m3u8", "tvg_id": "TRTSporYildiz.tr", "kanal_adi": "TRT Spor Yıldız HD"},
    {"dosya": "yayinas.m3u8", "tvg_id": "ASpor.tr", "kanal_adi": "A Spor HD"},
    {"dosya": "yayinatv.m3u8", "tvg_id": "ATV.tr", "kanal_adi": "ATV HD"},
    {"dosya": "yayintv8.m3u8", "tvg_id": "TV8.tr", "kanal_adi": "TV8 HD"},
    {"dosya": "yayintv85.m3u8", "tvg_id": "TV85.tr", "kanal_adi": "TV8.5 HD"},
    {"dosya": "yayinnbatv.m3u8", "tvg_id": "NBATV.tr", "kanal_adi": "NBA TV HD"},
    {"dosya": "yayinex1.m3u8", "tvg_id": "ExxenSpor1.tr", "kanal_adi": "Exxen Spor 1 HD"},
    {"dosya": "yayinex2.m3u8", "tvg_id": "ExxenSpor2.tr", "kanal_adi": "Exxen Spor 2 HD"},
    {"dosya": "yayinex3.m3u8", "tvg_id": "ExxenSpor3.tr", "kanal_adi": "Exxen Spor 3 HD"},
    {"dosya": "yayinex4.m3u8", "tvg_id": "ExxenSpor4.tr", "kanal_adi": "Exxen Spor 4 HD"},
    {"dosya": "yayinex5.m3u8", "tvg_id": "ExxenSpor5.tr", "kanal_adi": "Exxen Spor 5 HD"},
    {"dosya": "yayinex6.m3u8", "tvg_id": "ExxenSpor6.tr", "kanal_adi": "Exxen Spor 6 HD"},
    {"dosya": "yayinex7.m3u8", "tvg_id": "ExxenSpor7.tr", "kanal_adi": "Exxen Spor 7 HD"},
    {"dosya": "yayinex8.m3u8", "tvg_id": "ExxenSpor8.tr", "kanal_adi": "Exxen Spor 8 HD"},
]

def siteyi_bul():
    print(f"\n{GREEN}[*] Site aranıyor...{RESET}")
    
    # Önce güncel siteyi dene (1540)
    guncel_site = "https://trgoals1540.xyz/"
    try:
        r = requests.get(guncel_site, timeout=5)
        if r.status_code == 200:
            print(f"{GREEN}[OK] Güncel site çalışıyor: {guncel_site}{RESET}")
            return guncel_site
    except:
        print(f"{YELLOW}[!] Güncel siteye erişilemedi, tüm siteler taranıyor...{RESET}")
    
    # 1540'dan başlayarak yukarı doğru tara (önce güncel site ve sonrası)
    for i in range(1540, 1600):
        url = f"https://trgoals{i}.xyz/"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                if "channel.html?id=" in r.text or "yayin" in r.text or "player" in r.text:
                    print(f"{GREEN}[OK] Yayın bulundu: {url}{RESET}")
                    return url
                else:
                    print(f"{YELLOW}[-] {url} yayında ama yayın linki yok.{RESET}")
        except requests.RequestException:
            print(f"{RED}[-] {url} erişilemedi.{RESET}")
    
    # Bulamazsa eski siteleri tara (aşağı doğru)
    for i in range(1539, 1459, -1):
        url = f"https://trgoals{i}.xyz/"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                if "channel.html?id=" in r.text or "yayin" in r.text or "player" in r.text:
                    print(f"{GREEN}[OK] Yayın bulundu: {url}{RESET}")
                    return url
                else:
                    print(f"{YELLOW}[-] {url} yayında ama yayın linki yok.{RESET}")
        except requests.RequestException:
            pass  # Sessiz geç
    
    return None

def find_baseurl_advanced(url):
    """Gelişmiş base URL bulma fonksiyonu"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        r = requests.get(url, timeout=10, headers=headers)
        r.raise_for_status()
        
        html = r.text
        
        # Farklı pattern'ler dene
        patterns = [
            r'baseurl\s*[:=]\s*["\']([^"\']+)["\']',
            r'var\s+base\s*=\s*["\']([^"\']+)["\']',
            r'const\s+baseUrl\s*=\s*["\']([^"\']+)["\']',
            r'src=["\']([^"\']+load\.php[^"\']*)["\']',
            r'file:?\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
            r'"(https?://[^"]+cdn[^"]+)"',
            r'"(https?://[^"]+\.m3u8[^"]*)"',  # Direkt m3u8 linki
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                base = match.group(1)
                # Eğer direkt m3u8 linkiyse, base URL'yi çıkar
                if '.m3u8' in base:
                    base = '/'.join(base.split('/')[:-1]) + '/'
                # Eğer tam URL değilse, site URL'si ile birleştir
                elif not base.startswith('http'):
                    if base.startswith('//'):
                        base = 'https:' + base
                    elif base.startswith('/'):
                        base = url.rstrip('/') + base
                    else:
                        base = url.rstrip('/') + '/' + base
                print(f"{GREEN}[OK] Base URL bulundu: {base}{RESET}")
                return base
        
        # Sayfada gizli JSON var mı kontrol et
        json_pattern = r'<script[^>]*>(.*?)(?:var|const|let)\s+(\w+)\s*=\s*({.+?})</script>'
        json_matches = re.findall(json_pattern, html, re.DOTALL)
        for match in json_matches:
            try:
                data = json.loads(match[1])
                if isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, str) and ('.m3u8' in value or 'cdn' in value):
                            if '.m3u8' in value:
                                base = '/'.join(value.split('/')[:-1]) + '/'
                            else:
                                base = value
                            print(f"{GREEN}[OK] JSON'dan base URL bulundu: {base}{RESET}")
                            return base
            except:
                pass
                
    except requests.RequestException as e:
        print(f"{RED}[HATA] Sayfa yüklenemedi: {e}{RESET}")
    
    return None

def generate_m3u(base_url, referer, user_agent):
    lines = ["#EXTM3U"]
    calisan_kanal_sayisi = 0
    
    for idx, k in enumerate(KANALLAR, start=1):
        name = f"ÜmitM0d {k['kanal_adi']}"
        # Base URL'nin sonunda / var mı kontrol et
        base = base_url
        if not base.endswith('/'):
            base += '/'
        channel_url = base + k["dosya"]
        
        # Kanalları test et (opsiyonel)
        try:
            test = requests.get(channel_url, timeout=2, headers={'User-Agent': user_agent})
            if test.status_code == 200:
                durum = f"{GREEN}✓{RESET}"
                calisan_kanal_sayisi += 1
            else:
                durum = f"{YELLOW}?{RESET}"
        except:
            durum = f"{RED}✗{RESET}"
        
        lines.append(f'#EXTINF:-1 tvg-id="{k["tvg_id"]}" tvg-name="{name}",{name}')
        lines.append(f'#EXTVLCOPT:http-user-agent={user_agent}')
        lines.append(f'#EXTVLCOPT:http-referrer={referer}')
        lines.append(channel_url)
        print(f"  {durum} {idx:02d}. {name}")
    
    return "\n".join(lines), calisan_kanal_sayisi

if __name__ == "__main__":
    site = siteyi_bul()
    if not site:
        print(f"{RED}[HATA] Yayın yapan site bulunamadı.{RESET}")
        sys.exit(1)

    print(f"{YELLOW}[*] Site bulundu: {site}{RESET}")
    
    channel_url = site.rstrip("/") + "/channel.html?id=yayinzirve"
    print(f"{YELLOW}[*] Channel URL kontrol ediliyor: {channel_url}{RESET}")
    
    base_url = find_baseurl_advanced(channel_url)
    
    # Alternatif olarak direkt ana sayfayı dene
    if not base_url:
        print(f"{YELLOW}[*] Channel sayfasında bulunamadı, ana sayfa deneniyor...{RESET}")
        base_url = find_baseurl_advanced(site)
    
    if not base_url:
        print(f"{RED}[HATA] Base URL bulunamadı.{RESET}")
        print(f"{YELLOW}[!] Lütfen aşağıdaki siteyi manuel kontrol edin:{RESET}")
        print(f"  Site: {site}")
        print(f"  Channel URL: {channel_url}")
        sys.exit(1)

    playlist, calisan_sayi = generate_m3u(base_url, site, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    with open("umitm0d.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)

    print(f"\n{GREEN}[OK] Playlist oluşturuldu: umitm0d.m3u{RESET}")
    print(f"{GREEN}[OK] Toplam {len(KANALLAR)} kanal eklendi, {calisan_sayi} kanal erişilebilir{RESET}")
    print(f"{YELLOW}[!] Kullanılan site: {site}{RESET}")
