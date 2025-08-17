import requests
import re
import sys

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
    for i in range(1364, 1454):
        url = f"https://trgoals{i}.xyz/"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                if "channel.html?id=" in r.text:
                    print(f"{GREEN}[OK] Yayın bulundu: {url}{RESET}")
                    return url
                else:
                    print(f"{YELLOW}[-] {url} yayında ama yayın linki yok.{RESET}")
        except requests.RequestException:
            print(f"{RED}[-] {url} erişilemedi.{RESET}")
    return None

def find_baseurl(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except requests.RequestException:
        return None
    match = re.search(r'baseurl\s*[:=]\s*["\']([^"\']+)["\']', r.text)
    if match:
        return match.group(1)
    return None

def generate_m3u(base_url, referer, user_agent):
    lines = ["#EXTM3U"]
    for idx, k in enumerate(KANALLAR, start=1):
        name = f"ÜmitM0d {k['kanal_adi']}"
        lines.append(f'#EXTINF:-1 tvg-id="{k["tvg_id"]}" tvg-name="{name}",{name}')
        lines.append(f'#EXTVLCOPT:http-user-agent={user_agent}')
        lines.append(f'#EXTVLCOPT:http-referrer={referer}')
        lines.append(base_url + k["dosya"])
        print(f"  ✔ {idx:02d}. {name}")
    return "\n".join(lines)

if __name__ == "__main__":
    site = siteyi_bul()
    if not site:
        print(f"{RED}[HATA] Yayın yapan site bulunamadı.{RESET}")
        sys.exit(1)

    channel_url = site.rstrip("/") + "/channel.html?id=yayinzirve"
    base_url = find_baseurl(channel_url)
    if not base_url:
        print(f"{RED}[HATA] Base URL bulunamadı.{RESET}")
        sys.exit(1)

    playlist = generate_m3u(base_url, site, "Mozilla/5.0")
    with open("umitm0d.m3u", "w", encoding="utf-8") as f:
        f.write(playlist)

    print(f"{GREEN}[OK] Playlist oluşturuldu: umitm0d.m3u{RESET}")