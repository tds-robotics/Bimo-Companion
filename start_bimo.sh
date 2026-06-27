#!/bin/bash

# 1. Resetăm serverul de sunet și driverele ALSA
# '|| true' asigură că scriptul merge mai departe chiar dacă apar mici erori
pulseaudio -k || true
sudo alsa force-reload || true

# 2. Așteptăm să se stabilizeze driverele după reset
sleep 5

# 3. Direcționăm imaginea către ecran
export DISPLAY=:0

# 4. Lansăm robotul
/usr/bin/python3 /home/teodor/bimo_main.py

