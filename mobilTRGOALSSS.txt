import requests
import re
import sys

# ========= RENK TANIMLARI =========
RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"

# ========= KANAL LİSTESİ =========
kanallar = [
    {"dosya":"yayinzirve.m3u8","tvg_id":"BeinSports1.tr","kanal_adi":"Bein Sports 1 HD (VIP)"},
    {"dosya":"yayin1.m3u8","tvg_id":"BeinSports1.tr","kanal_adi":"Bein Sports 1 HD"},
    {"dosya":"yayinb2.m3u8","tvg_id":"BeinSports2.tr","kanal_adi":"Bein Sports 2 HD"},
    {"dosya":"yayinb3.m3u8","tvg_id":"BeinSports3.tr","kanal_adi":"Bein Sports 3 HD"},
    {"dosya":"yayinb4.m3u8","tvg_id":"BeinSports4.tr","kanal_adi":"Bein Sports 4 HD"},
    {"dosya":"yayinb5.m3u8","tvg_id":"BeinSports5.tr","kanal_adi":"Bein Sports 5 HD"},
    {"dosya":"yayinbm1.m3u8","tvg_id":"BeinMax1.tr","kanal_adi":"Bein Max 1 HD"},
    {"dosya":"yayinbm2.m3u8","tvg_id":"BeinMax2.tr","kanal_adi":"Bein Max 2 HD"},
    {"dosya":"yayinss.m3u8","tvg_id":"SSport1.tr","kanal_adi":"S Sport 1 HD"},
    {"dosya":"yayinss2.m3u8","tvg_id":"SSport2.tr","kanal_adi":"S Sport 2 HD"},
    {"dosya":"yayinssp2.m3u8","tvg_id":"SSportPlus.tr","kanal_adi":"S Sport Plus HD"},
    {"dosya":"yayint1.m3u8","tvg_id":"TivibuSpor1.tr","kanal_adi":"Tivibu Spor 1 HD"},
    {"dosya":"yayint2.m3u8","tvg_id":"TivibuSpor2.tr","kanal_adi":"Tivibu Spor 2 HD"},
    {"dosya":"yayint3.m3u8","tvg_id":"TivibuSpor3.tr","kanal_adi":"Tivibu Spor 3 HD"},
    {"dosya":"yayinsmarts.m3u8","tvg_id":"SmartSpor1.tr","kanal_adi":"Smart Spor 1 HD"},
    {"dosya":"yayinsms2.m3u8","tvg_id":"SmartSpor2.tr","kanal_adi":"Smart Spor 2 HD"},
    {"dosya":"yayintrtspor.m3u8","tvg_id":"TRTSpor.tr","kanal_adi":"TRT Spor HD"},
    {"dosya":"yayintrtspor2.m3u8","tvg_id":"TRTSporYildiz.tr","kanal_adi":"TRT Spor Yıldız HD"},
    {"dosya":"yayinas.m3u8","tvg_id":"ASpor.tr","kanal_adi":"A Spor HD"},
    {"dosya":"yayinatv.m3u8","tvg_id":"ATV.tr","kanal_adi":"ATV HD"},
    {"dosya":"yayintv8.m3u8","tvg_id":"TV8.tr","kanal_adi":"TV8 HD"},
    {"dosya":"yayintv85.m3u8","tvg_id":"TV85.tr","kanal_adi":"TV8.5 HD"},
    {"dosya":"yayinnbatv.m3u8","tvg_id":"NBATV.tr","kanal_adi":"NBA TV HD"},
    {"dosya":"yayinex1.m3u8","tvg_id":"ExxenSpor1.tr","kanal_adi":"Exxen Spor 1 HD"},
    {"dosya":"yayinex2.m3u8","tvg_id":"ExxenSpor2.tr","kanal_adi":"Exxen Spor 2 HD"},
    {"dosya":"yayinex3.m3u8","tvg_id":"ExxenSpor3.tr","kanal_adi":"Exxen Spor 3 HD"},
    {"dosya":"yayinex4.m3u8","tvg_id":"ExxenSpor4.tr","kanal_adi":"Exxen Spor 4 HD"},
    {"dosya":"yayinex5.m3u8","tvg_id":"ExxenSpor5.tr","kanal_adi":"Exxen Spor 5 HD"},
    {"dosya":"yayinex6.m3u8","tvg_id":"ExxenSpor6.tr","kanal_adi":"Exxen Spor 6 HD"},
    {"dosya":"yayinex7.m3u8","tvg_id":"ExxenSpor7.tr","kanal_adi":"Exxen Spor 7 HD"},
    {"dosya":"yayinex8.m3u8","tvg_id":"ExxenSpor8.tr","kanal_adi":"Exxen Spor 8 HD"},
]

# ========= YARDIMCI FONKSİYONLAR =========
def is_site_up(url):
    try:
        r = requests.head(url, timeout=5)
        return r.status_code < 400
    except:
        return False

def get_site_url():
    print(f"{YELLOW}[*]{RESET} Site adresi aranıyor (trgoals1364.xyz → 1453)...")
    for i in range(1364, 1454):
        domain = f"https://trgoals{i}.xyz/"
        print(f"  Deneniyor: {domain}", end="")
        if is_site_up(domain):
            print(f"  {GREEN}[OK]{RESET}")
            return domain
        else:
            print(f"  {RED}[Down]{RESET}")
    print(f"{RED}[HATA]{RESET} Hiçbir trgoalsN.xyz sitesi aktif değil.")
    sys.exit(1)

def get_final_url(url):
    try:
        r = requests.get(url, allow_redirects=True, timeout=10)
        return r.url
    except:
        return None

def find_baseurl(url):
    try:
        r = requests.get(url, timeout=10)
        for pattern in [r'baseurl\s*[:=]\s*["\']([^"\']+)["\']', r'"baseurl"\s*:\s*"([^"]+)"']:
            m = re.search(pattern, r.text)
            if m:
                return m.group(1)
    except:
        return None
    return None

def generate_m3u(base_url, referer, user_agent):
    lines = ["#EXTM3U"]
    print(f"{YELLOW}[*]{RESET} Kanallar ekleniyor...")
    for idx, k in enumerate(kanallar, start=1):
        kanal_mod = f"ÜmitM0d {k['kanal_adi']}"
        print(f"  {GREEN}✔{RESET} {str(idx).zfill(2)}. {kanal_mod}")
        lines.append(f'#EXTINF:-1 tvg-id="{k["tvg_id"]}" tvg-name="{kanal_mod}",{kanal_mod}')
        lines.append(f'#EXTVLCOPT:http-user-agent={user_agent}')
        lines.append(f'#EXTVLCOPT:http-referrer={referer}')
        lines.append(base_url + k["dosya"])
    print(f"{GREEN}[OK]{RESET} Toplam {len(kanallar)} kanal eklendi.")
    return "\n".join(lines)

# ========= ASIL ÇALIŞMA =========
if __name__ == "__main__":
    DOSYA_ADI = "Umitmod.m3u"
    user_agent = "Mozilla/5.0"

    print(f"{CYAN}{BOLD}╔══════════════════════════════════════╗")
    print(f"║           ÜmitM0d IPTV Script        ║")
    print(f"╚══════════════════════════════════════╝{RESET}\n")

    site_url = get_site_url()
    print(f"{GREEN}[OK]{RESET} Kullanılacak site: {site_url}")

    print(f"{YELLOW}[*]{RESET} Kanal sayfasına erişiliyor...")
    chan_url = get_final_url(site_url + "channel.html?id=yayinzirve")
    if not chan_url:
        print(f"{RED}[HATA]{RESET} Kanal sayfası alınamadı.")
        sys.exit(1)
    print(f"{GREEN}[OK]{RESET} Kanal URL: {chan_url}")

    base_url = find_baseurl(chan_url)
    if not base_url:
        print(f"{RED}[HATA]{RESET} Base URL bulunamadı.")
        sys.exit(1)
    print(f"{GREEN}[OK]{RESET} Base URL: {base_url}\n")

    playlist = generate_m3u(base_url, site_url, user_agent)
    with open(DOSYA_ADI, "w", encoding="utf-8") as f:
        f.write(playlist)

    print(f"\n{CYAN}{BOLD}╔══════════════════════════════════════╗")
    print(f"║  Playlist oluşturuldu: {DOSYA_ADI.ljust(16)}║")
    print(f"║  Toplam Kanal: {str(len(kanallar)).rjust(3)}                ║")
    print(f"╚══════════════════════════════════════╝{RESET}")