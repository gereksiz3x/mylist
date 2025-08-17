name: ÜmitM0d IPTV Otomatik

on:
  schedule:
    - cron: "0 */3 * * *" # Her 3 saatte bir
  workflow_dispatch: # Manuel çalıştırma

jobs:
  run-umitmod:
    runs-on: ubuntu-latest
    steps:
      - name: Repo'yu Klonla
        uses: actions/checkout@v4

      - name: Python Kur
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Bağımlılıkları Kur
        run: |
          pip install requests

      - name: ÜmitM0d Script Çalıştır
        run: |
          python umitm0d.py

      - name: Playlist'i Commit Et
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add umitm0d.m3u
          git commit -m "Otomatik güncelleme: $(date '+%Y-%m-%d %H:%M:%S')" || echo "Değişiklik yok"
          git push
