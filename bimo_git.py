from types import ModuleType
import sys
import importlib.util
fake_imp = ModuleType('imp')
def find_module(name, path=None):
    spec = importlib.util.find_spec(name, path)
    return spec is not None
fake_imp.find_module = find_module


sys.modules['imp'] = fake_imp

import pygame
import asyncio
import threading
import scipy.signal
import socket
import time
import numpy as np
import traceback
import cv2
import time
import statistics
from collections import deque
from deepface import DeepFace
import sys
import os
from gtts import gTTS
import importlib.util
from types import ModuleType
import speech_recognition as sr
import queue
import random
import importlib
import pyaudio
from bleak import BleakScanner, BleakClient
from picamera2 import Picamera2
from gat_bimo import GatBimo
from deepface import DeepFace
from openai import OpenAI
from gpiozero import Button
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from libcamera import Transform
from cryptography.hazmat.backends import default_backend
from modul_stres_zilnic import a_fost_evaluat_azi, ruleaza_micro_chestionar_vocal
from datetime import datetime, timezone
from faster_whisper import WhisperModel
from openwakeword.model import Model
from gtts import gTTS
import subprocess
import requests
import json
from collections import deque
import statistics


camera = None
ecran = None
font_bimo = None
w, h = 0, 0
mijloc_x, mijloc_y = 0, 0
bimo = GatBimo()


def init_hardware():
    global camera, ecran, font_bimo, w, h, mijloc_x, mijloc_y
    
    try:
        pygame.display.init()
        pygame.font.init()
        pygame.mixer.quit()
        
        
        camera = Picamera2()
        config = camera.create_video_configuration(main={"size": (640, 480)})
        camera.configure(config)
        camera.start()
        screen_info = pygame.display.Info()
        w, h = screen_info.current_w, screen_info.current_h
        
        ecran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)
        
        mijloc_x, mijloc_y = w // 2, h // 2
        text_centrat_x=mijloc_x+100
        font_bimo = pygame.font.Font("font_bimo.ttf", 60)
        
        return True
    except Exception as e:
        print(f" Eroare la inițializare: {e}")
        return False

class ResourceManager:
    def __init__(self):
        
        self.client = OpenAI(api_key="cheie")        
        
        self.inima = queue.Queue()
        self.sfat = queue.Queue()
        self.blt = queue.Queue()
        self.text_spus = queue.Queue()
        self.dialog = queue.Queue()
        self.stare_audio = queue.Queue()
        
        
        self.puls_curent = 0
        self.volum_curent=0
        self.stare_interfata = 0
        self.generating = False
        self.listening = False
        self.mesaj = ""
        self.model =None
        
        self.buton = Button(26, bounce_time=0.1)
        
        
        self.assets = {}

    def load_all_assets(self):
        
     
        self.assets["fundal"] = pygame.image.load("/home/teodor/Documents/fundal.png")
        self.assets["imagine_noua"] = pygame.transform.scale(
            pygame.image.load("/home/teodor/Documents/frame_004.png"), (1000, 380)
        )
        
       
        self.assets["frames_mouth"] = [pygame.image.load(f"/home/teodor/Documents/frames_mouth/frame_{i:03d}.png") for i in range(1, 37)]
        self.assets["frames"] = [pygame.image.load(f"/home/teodor/Documents/frames_eye/frame_{i:03d}.png") for i in range(1, 16)]
        self.assets["frames2"] = [pygame.image.load(f"/home/teodor/Documents/frames_left/frame_{i:03d}.png") for i in [2, 3, 4]]
        self.assets["frame_respiratie"] = [pygame.image.load(f"/home/teodor/Documents/respiratie/{i:02d}.png") for i in range(1, 41)]
        
        
class BimoUI:
    def __init__(self, res):
        
        self.res = res
        
        
        self.animation_speed = 0.75
        self.blinking = False
        self.frame_index = 0
        self.frame_index2 = 0
        
        
        self.directie_bula = 1
        self.raza_bula = 40
        self.index_respiratie = 0
        self.directie = 0

    def deseneaza_fata(self, ecran, centru_x, centru_y):
        
        frames = self.res.assets["frames"]
        frames2 = self.res.assets["frames2"]
        imagine_noua = self.res.assets["imagine_noua"]

        if not self.blinking and random.random() < 0.005:
            self.blinking = True
            self.frame_index = 0

        if self.blinking:
            current_eye = frames[int(self.frame_index)]
            self.frame_index += self.animation_speed
            if self.frame_index >= len(frames):
                self.blinking = False
        else:
            current_eye = frames2[int(self.frame_index2)]
            self.frame_index2 += (self.animation_speed - 0.50)
            if self.frame_index2 >= len(frames2):
                self.frame_index2 = 0

        ecran.blit(current_eye, (centru_x + 10, centru_y - 400))
        ecran.blit(current_eye, (centru_x - 550, centru_y - 400))
        ecran.blit(imagine_noua, (centru_x - 530, centru_y + 10))

    def exercitiu_respiratie(self, ecran, centru_x, centru_y, raza_maxima, culoare_bula):
        if self.directie_bula == 1:
            self.raza_bula += 1.5
            if self.raza_bula >= raza_maxima: self.directie_bula = -1
        if self.directie_bula == -1:
            self.raza_bula -= 1.5
            if self.raza_bula <= 40: self.directie_bula = 1
        
        pygame.draw.circle(ecran, culoare_bula, (int(centru_x), int(centru_y)), int(self.raza_bula), 5)

    def exercitiu_respiratie2(self, ecran, centru_x, centru_y):
        frame_respiratie = self.res.assets["frame_respiratie"]
        respiratie_curent = frame_respiratie[int(self.index_respiratie)]
        ecran.blit(respiratie_curent, (centru_x, centru_y))
        
        if self.directie == 0:
            self.index_respiratie += 1
            if self.index_respiratie >= len(frame_respiratie) - 1: self.directie = 1
        elif self.directie == 1:
            self.index_respiratie -= 1
            if self.index_respiratie <= 0: self.directie = 0
            
    def scrie_mesaj(self, ecran, text, font, x, y, culoare=(255, 255, 255)):
        
        text_surface = font.render(text, True, culoare)
        text_rect = text_surface.get_rect(center=(x, y))
        ecran.blit(text_surface, text_rect)

    def afiseaza_raspuns(self, ecran, text_afisat, secunde):
       
        timp_start = time.time()
        font_bimo = self.res.assets.get("font_bimo", pygame.font.Font(None, 42))
        
        while time.time() - timp_start < secunde:
            ecran.blit(self.res.assets["fundal"], (0,0)) 
            self.scrie_mesaj(ecran, text_afisat, font_bimo, mijloc_x+100, mijloc_y)
            
            pygame.display.update()
            pygame.event.pump() 
            pygame.time.delay(50)
            
    def loading_screen(self, ecran, text_pas, secunde_asteptare, mijloc_x, mijloc_y):
        
        timp_start = time.time()
        font_bimo = self.res.assets.get("font_bimo", pygame.font.Font(None, 42))
        
        while time.time() - timp_start < secunde_asteptare:
            
            ecran.blit(self.res.assets["fundal"], (0, 0)) 
            
            
            numar_puncte = (pygame.time.get_ticks() // 500) % 4
            text_incarcare = text_pas + "." * numar_puncte
            
            
            self.scrie_mesaj(ecran, text_incarcare, font_bimo, mijloc_x, mijloc_y)
            
            pygame.display.update()
            pygame.event.pump()
            pygame.time.delay(30)
    
class HeartRateManager(threading.Thread):
    def __init__(self, inima_queue):
        super().__init__()
        self.inima_queue = inima_queue
        self.MAC_BRATARA = "ED:D8:8D:FC:FA:87"
        self.AUTH_KEY = bytes.fromhex("873ed84f154b4a57cff9114aae28ccf9")
        self.AUTH_UUID = "00000009-0000-3512-2118-0009af100700"
        self.HR_DATA_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
        self.HR_CTRL_UUID = "00002a39-0000-1000-8000-00805f9b34fb"

    def run(self):
       
        asyncio.run(self.connection_loop())

    async def connection_loop(self):
        while True:
            try:
                print(f"🔗 Bimo: Tentativă conectare la {self.MAC_BRATARA}...")
                async with BleakClient(self.MAC_BRATARA, timeout=10.0) as client:
                    await self.authenticate_and_read(client)
            except Exception as e:
                print(f"❌ [BLUETOOTH] Eroare: {e}. Reîncerc în 5 secunde...")
                await asyncio.sleep(5)

    async def authenticate_and_read(self, client):
        random_number = None
        auth_success = asyncio.Event()

        def auth_handler(sender, data):
            nonlocal random_number
            
            if data[:3] == b'\x10\x02\x01':
                random_number = data[3:]
                
            elif data[:3] == b'\x10\x03\x01':
                
                auth_success.set()
            else:
                

        def citire_puls(sender, data):
            print("HR RAW:", data.hex())

            if len(data) > 1:
                puls = data[1]
                print("Puls:", puls)
                self.inima_queue.put(puls)

        
        await client.start_notify(self.AUTH_UUID, auth_handler)
        
       
        await client.write_gatt_char(self.AUTH_UUID, b'\x02\x00')
        
        
        await asyncio.sleep(2) 

        if random_number:
            
            cipher = Cipher(algorithms.AES(self.AUTH_KEY), modes.ECB(), backend=default_backend())
            encryptor = cipher.encryptor()
            encrypted = encryptor.update(bytes(random_number)) + encryptor.finalize()
            
            
            await client.write_gatt_char(self.AUTH_UUID, b'\x03\x00' + encrypted)
            
            
            try:
                await asyncio.wait_for(auth_success.wait(), timeout=10.0)
                
            except asyncio.TimeoutError:
                
                return

            
            await client.start_notify(self.HR_DATA_UUID, citire_puls)
            await client.write_gatt_char(self.HR_CTRL_UUID, b'\x15\x01\x01')
            await client.write_gatt_char(self.HR_CTRL_UUID, b'\x15\x02\x00')
            await client.write_gatt_char(self.HR_CTRL_UUID, b'\x15\x02\x01')
            await client.write_gatt_char(self.HR_CTRL_UUID, b'\x15\x01\x00')
            
            while client.is_connected:
                await asyncio.sleep(2)
        else:
            print("EROARE: Nu am primit niciun număr aleatoriu de la brățară.")
            


class StressAndEmotionAnalyzer:
    def __init__(self):
        
        self.istoric_emotii = deque(maxlen=5)
        self.timp_ultima_scanare = 0
        self.ultima_emotie_cunoscuta = "neutral"
        self.ultim_x = None
        self.ultim_y = None
        self.agitatie_cap = 0
        self.istoric_agitatie = deque(maxlen=15)
        
        
        
        cascade_path = cv2.data.haarcascades

        self.face_cascade = cv2.CascadeClassifier(
    cascade_path + "haarcascade_frontalface_default.xml"
)

        self.upperbody_cascade = cv2.CascadeClassifier(
    cascade_path + "haarcascade_upperbody.xml"
)

        self.smile_cascade = cv2.CascadeClassifier(
    cascade_path + "haarcascade_smile.xml"
)
        
        self.tension_score = 0
        self.nivel_stres_fizic = "relaxat"

    def este_om(self, imagine):
        try:
            if imagine.shape[2] == 4:
                imagine = imagine[:, :, :3]
            DeepFace.extract_faces(img_path=imagine, enforce_detection=True, detector_backend="ssd")
            return True
        except ValueError:
            return False   
        except Exception:
            return False

    def analiza_cadru(self, frame):
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.2, 3)
        
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            if self.ultim_x is not None:

                dist = abs(x - self.ultim_x) + abs(y - self.ultim_y)

                if dist > 35:
                    self.istoric_agitatie.append(1)
                else:
                    self.istoric_agitatie.append(0)

                self.agitatie_cap = sum(self.istoric_agitatie)
                print(f"Agitatie: {self.agitatie_cap}")

            self.ultim_x = x
            self.ultim_y = y
            
            
            roi_mouth = gray[y + int(h/2):y+h, x:x+w]

            smiles = self.smile_cascade.detectMultiScale(
    roi_mouth,
    scaleFactor=1.8,
    minNeighbors=20
)

            if len(smiles) == 0:
                self.tension_score += 1
           
            bodies = self.upperbody_cascade.detectMultiScale(gray, 1.1, 2)
            for (bx, by, bw, bh) in bodies:
                if (y + h) > by:
                    self.tension_score += 2
                    
        
        timp_curent = time.time()
        if timp_curent - self.timp_ultima_scanare >= 8:
            try:
                result = DeepFace.analyze(img_path=frame, actions=['emotion'], enforce_detection=False, detector_backend="ssd")
                procente = result[0]['emotion']
                
               
                if self.tension_score > 30:
                    self.nivel_stres_fizic = "ridicat (umeri/maxilar tensionat)"
                else:
                    self.nivel_stres_fizic = "relaxat"
                    
                
                self.tension_score = 0 
                
               
                if (procente['sad'] < 50 and procente['fear'] < 50 and procente['angry'] < 50) or procente['happy'] > 50:
                    emotie_curenta = "neutral"
                else:
                    emotie_curenta = result[0]['dominant_emotion']
                
                self.istoric_emotii.append(emotie_curenta)
                if len(self.istoric_emotii) > 0:
                    try:
                        self.ultima_emotie_cunoscuta = statistics.mode(self.istoric_emotii)
                    except:
                        self.ultima_emotie_cunoscuta = self.istoric_emotii[-1]
                    
            except Exception as e:
                pass
                
            self.timp_ultima_scanare = timp_curent
            
        return self.ultima_emotie_cunoscuta, self.nivel_stres_fizic
class AudioManager(threading.Thread):
    def __init__(self, dialog_queue):
        super().__init__()
        self.dialog_queue = dialog_queue
        self.running = True
        self.este_pe_pauza = False
        self.microfon_liber = threading.Event()
        self.microfon_liber.set()
        
        
        self.mic_rate = 48000  
        self.ai_rate = 16000   
        self.chunk = 3840      
        
        
        self.owwModel = Model(wakeword_model_paths=["models/hey_bimo.onnx"])
        self.p = pyaudio.PyAudio()

        self.index_microfon = None
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            if info.get('maxInputChannels') > 0:
                nume = info.get('name').lower()
                if "sandberg" in nume:
                    self.index_microfon = i
                    print(f" Microfon {info.get('name')} (Index: {i})")
                    break

        self._deschide_microfon()

    def _deschide_microfon(self):
        
        for incercare in range(5):
            try:
                self.stream = self.p.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=self.mic_rate,
                    input=True,
                    input_device_index=self.index_microfon,
                    frames_per_buffer=self.chunk
            )
                return True
            except Exception as e:
                print(f"[EROARE AUDIO: {e}")
                self.running = False

    def pauza(self):
        
        self.microfon_liber.clear() 
        if hasattr(self, 'stream'):
            try:
                self.stream.stop_stream()
                self.stream.close()
            except: pass

    def reia(self):
        
        self._deschide_microfon() 
        self.microfon_liber.set()
        
    def calculeaza_volum(self, audio_data):
        return np.abs(audio_data).mean()

    def run(self):
        while self.running:
            if not self.microfon_liber.is_set():
                time.sleep(0.5)
                continue
            
            try:
                
                raw_data = self.stream.read(self.chunk, exception_on_overflow=False)
                audio_data = np.frombuffer(raw_data, dtype=np.int16)
                
                
                volum = self.calculeaza_volum(audio_data)
                self.volum_curent=volum
                if volum > 500: 
                    
                    bare_vizuale = "█" * int(volum / 100) 
                   
                    print(f"🎤 [Nivel Sunet]: {int(volum):4d} | {bare_vizuale}")
                
                resampled_audio=audio_data[::3]
                
                prediction = self.owwModel.predict(resampled_audio)
                
                if prediction.get('hey_bimo', 0) > 0.5:
                    
                    self.owwModel.reset()
                    
                    self.dialog_queue.put("WAKE_WORD_DETECTAT")
                    
                    self.pauza() 
                    
            except Exception as e:
                
                print(f"Eroare în buclă: {e}")
                time.sleep(0.5)

    def stop(self):
        self.running = False
        self.pauza()
        self.p.terminate()
class SystemUtils:
    def __init__(self, resource_manager):
        self.res = resource_manager
        
        
        self.TG_TOKEN = "token"
        self.TG_CHAT_ID = "id"
        
        
        self.este_stresat = False
        self.timp_ultimul_sfat = 0
        self.timp_curent_stress = 0

    def spune(self, text):
        
        def ruleaza_audio():
            try:
                
                text_curat = text.replace('"', '').replace("'", "")
                
                
                fisier_mp3 = "vorbire_bimo.mp3"
                voce = "ro-RO-AlinaNeural"
                
                
                subprocess.run([
            "edge-tts",
            "--voice", voce,
            "--text", text_curat,
            "--write-media", fisier_mp3
        ], check=True)

                if os.path.exists(fisier_mp3):
                    subprocess.run([
                "mpg123",
                "-q",
                "-o", "alsa",
                fisier_mp3
            ], check=True)
                    
                   
                    os.remove(fisier_mp3)

            except Exception as e:
                print(f"❌ [EROARE în thread audio]: {e}")

        
        
        
        
        threading.Thread(target=ruleaza_audio, daemon=True).start()

                
           


    def trimite_alerta_telegram(self, mesaj):
       
        url = f"https://api.telegram.org/bot{self.TG_TOKEN}/sendMessage"
        date_trimise = {"chat_id": self.TG_CHAT_ID, "text": mesaj}
        
        
        try:
            raspuns = requests.post(url, data=date_trimise, timeout=3)
            if raspuns.status_code == 200:
                print("Alertă trimisă cu succes!")
            else:
                print(f"Eroare trimitere: {raspuns.text}")
        except Exception as e:
            print(f"Lipsă conexiune internet: {e}")
    def data_curenta(self):
        acum=datetime.now()
        timp_formatat = acum.strftime("%d-%m-%Y, ora %H:%M")
        print(f"Data si ora curenta:{acum}")
        return timp_formatat
    def ruleaza_meditatie_youtube(self):
        
        print("🧘 [TERAPIE] Pregătesc clipul de meditație...")
        try:
            pygame.mixer.quit() 
        except: pass 
        
        comanda = ["mpv", "--fs", "--ontop", "meditatie.mp4"]
        try:
            subprocess.run(comanda)
            print("✅ [TERAPIE] Meditația s-a încheiat.")
        except Exception as e:
            print(f"❌ [EROARE PLAYER]: {e}")

        
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f" Eroare sunet: {e}")

    def shutdown_bimo(self, camera_obj):
        
        
       
        if camera_obj is not None:
            try:
                camera_obj.stop()
                camera_obj.close()
                
            except Exception as e:
                print(f"Eroare oprire cameră: {e}")
                
        
        try:
            pygame.quit()
            
        except: pass
        
        time.sleep(1)
        print(" La revedere!")
       
        subprocess.run(["sudo", "shutdown", "-h", "now"])

def gaseste_index_microfon(cuvant_cheie):
    
   
    for index, nume_curent in enumerate(sr.Microphone.list_microphone_names()):
        
        if cuvant_cheie.lower() in nume_curent.lower():
            print(f"[SISTEM] Microfon detectat: '{nume_curent}' la Indexul -> {index}")
            return index
            
   
    return None
def asculta_conversatia(recognizer):
    
    with sr.Microphone(device_index=gaseste_index_microfon("Sandberg")) as source:
        try:
            
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print(" Procesez ")
            text = recognizer.recognize_google(audio, language='ro-RO')
            
            text_procesat = text.lower()
            print(f"[UTILIZATOR]: {text_procesat}")
            return text_procesat
            
        except sr.WaitTimeoutError:
            print(" Nu am auzit nimic.")
            return None
        except sr.UnknownValueError:
            print("] Nu am înțeles. ")
            return None
        except sr.RequestError as e:
            print(f" [BIMO Eroare Net]: {e}")
            return None
class DialogManager:
    def __init__(self, resource_manager, openai_client):
        self.res = resource_manager
        self.client = openai_client
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        
        
    def este_conectat(self,host="8.8.8.8", port=443, timeout=3):
        
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except Exception as e:
            print(f" Eroare rețea: {e}")
            return False
    
    def gaseste_index_microfon(cuvant_cheie):
        
   
        for index, nume_curent in enumerate(sr.Microphone.list_microphone_names()):
        
            if cuvant_cheie.lower() in nume_curent.lower():
                print(f" Microfon detectat: '{nume_curent}' la Indexul -> {index}")
                return index
            
        print(f" Nu am găsit niciun microfon care să conțină '{cuvant_cheie}'!")
        return None 
    def initiaza_conversatia(self, puls, emotie, stres_fizic, audio_manager,acum):
        
        audio_manager.microfon_liber.clear() 
        
        
        time.sleep(1) 
        
       
        threading.Thread(target=self._fir_conversatie, args=(puls, emotie, stres_fizic, audio_manager,acum), daemon=True).start()

    def _fir_conversatie(self, puls, emotie, stres_fizic, audio_manager, acum):
        self.res.stare_interfata = 3 
        
        
        mesaje_conversatie = [
            {"role": "system", "content": f"You are Bimo, a friendly companion robot. User BPM: {puls}, Emotion: {emotie}, Physical stress score: {stres_fizic}. The curent time is :{acum} Reply in Romanian.Try to be funny(like the cool guy) when needed. Avoid robotic answers and no emojis.If the question is about user's health, don t pe funny,be precise. Short (max 15 words)."}
        ]
        
        try:
            with sr.Microphone(device_index=gaseste_index_microfon("Sandberg"), sample_rate=48000, chunk_size=4096) as source:
                
                self.recognizer.dynamic_energy_threshold = False
            
            
                self.recognizer.energy_threshold = 250
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
                with open("test_microfon.wav", "wb") as f:
                    f.write(audio.get_wav_data())
            
            if self.este_conectat():
                
                    
                print(" Am înregistrat comanda! Procesez...")
                text_intrebare = self.recognizer.recognize_google(audio, language="ro-RO").lower()
                print(f" [UTILIZATOR]: {text_intrebare}")
                
                if "oprire sistem" in text_intrebare or "ne vedem" in text_intrebare or "ne auzim" in text_intrebare:
                    self.res.dialog.put("OPRIRE_SISTEM")
                    return

                elif "ce vezi" in text_intrebare or "deschide camera" in text_intrebare:
                    self.res.dialog.put("CE_VEZI")
                    return
                
                elif "bye" in text_intrebare or "stop" in text_intrebare or "la revedere" in text_intrebare:
                    self.res.dialog.put("Ne auzim mai târziu! Rămâi zen.")
                    return
                
                elif "sunt stresat" in text_intrebare:
                    self.res.dialog.put("RELAXARE")
                    return
                else:
                    mesaje_conversatie.append({"role": "user", "content": text_intrebare})
                    response = self.client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=mesaje_conversatie
                    )
                    raspuns_bimo = response.choices[0].message.content
                    print(f"🤖 [BIMO GÂNDEȘTE]: {raspuns_bimo}")
                    
                    
                    self.res.dialog.put(raspuns_bimo)
            else:
                print(f"OFFLINE ")
                self.res.dialog.put("Conexiunea a picat. Procesez comanda local, te rog așteaptă...")
                
                if self.res.model is None:
                    try:
                        from faster_whisper import WhisperModel
                        
                        self.res.model = WhisperModel(
    "/home/teodor/faster-whisper-small",
    device="cpu",
    compute_type="int8"
)
                    except Exception as e_load:
                        print(f" Nu am putut încărca  {e_load}")
                        self.res.dialog.put("Eroare la procesarea comnenzii")
                        return
                    
                try:
                    
                    
                    
                    
                    segments, _ = self.res.model.transcribe("test_microfon.wav", language="ro")
                    text_intrebare = "".join([segment.text for segment in segments])
                    print(f"{text_intrebare}")
                    
                   
                    if "oprire sistem" in text_intrebare.lower() or "stop" in text_intrebare.lower() or "sistem" in text_intrebare.lower():
                        self.res.dialog.put("OPRIRE_SISTEM")
                    elif "ce vezi" in text_intrebare.lower():
                        self.res.dialog.put("CE_VEZI")
                    else:
                        self.res.dialog.put("Am înțeles ce ai spus, dar fără internet pot executa doar comenzi de bază.")
                        
                except Exception as ex_offline:
                    print(f"❌ [DIALOG Eroare Whisper]: {ex_offline}")
                    self.res.dialog.put("Eroare critică la procesarea locală.")
                
        except sr.WaitTimeoutError:
            print(" Nu ai spus nimic. Renunț.")
        except sr.UnknownValueError:
            print("Nu s-a înțeles clar ce ai spus.")
            self.res.dialog.put("Nu am înțeles clar. Mai spune o dată.")
       
        except Exception as e:
            print(f"❌ [DIALOG Eroare]: {e}")
            
        finally:
            self.res.stare_interfata = 0
            
            audio_manager.microfon_liber.set()
            audio_manager.reia()
class BiometricMonitor(threading.Thread):
    def __init__(self, resource_manager, analyzer, openai_client, camera_obj): 
        super().__init__()
        self.res = resource_manager
        self.analyzer = analyzer 
        self.client = openai_client
        self.camera = camera_obj
        self.running = True
        
        
        self.istoric_puls = deque(maxlen=15)
        self.baseline = 70
        self.baseline = self.load_baseline()
        self.ultimul_update_baseline = time.time()
        self.API_URL = "https://bimo-companion.base44.app/api/entities/StressLog"
        self.HEADERS = {
            "api_key": "ee52330ea647429d9078f0ba730aa158",
            "Content-Type": "application/json"
        }
        
        self.alerta = False
        self.este_stresat = False
        self.timp_ultimul_sfat = 0
        self.timp_curent_stress = 0
        self.k_sad = 0 
        self.device_id = "BIMO_A1D3"

    def save_baseline(self, baseline_value):
        try:
            with open("baseline.json", "w") as f:
                json.dump({"baseline": baseline_value}, f)
        except Exception as e:
            print(f"⚠️ Nu am putut salva baseline: {e}")
            
    def load_baseline(self):
        try:
            with open("baseline.json", "r") as f:
                data = json.load(f)
                return data["baseline"]
        except:
            return 70 

    def trimite_date_aplicatie(self, bpm, stress_level, stress_alert):
        payload = {
            "bpm": bpm,
            "stress_level": stress_level,
            "stress_alert": stress_alert,
            "device_id": self.device_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        try:
            
            response = requests.post(self.API_URL, json=payload, headers=self.HEADERS, timeout=3)
            print(f"Status: {response.status_code}")
        except Exception as e:
            print(f"Eroare API: {e}")

    def run(self):
        
        while self.running:
            try:
               
                cadru_curent = self.camera.capture_array()
                if self.res.puls_curent > 0:
                    self.istoric_puls.append(self.res.puls_curent)

                if cadru_curent is not None:
                    persoana_detectata = self.analyzer.este_om(cadru_curent)
                    print(persoana_detectata)
                    
                    
                    if persoana_detectata:
                        emotie, stres_fizic = self.analyzer.analiza_cadru(cadru_curent)
                        stres_instant = self.detecteaza_stres_instant(emotie)
                        scor_stres = self.calculeaza_scor_stres_instant(emotie)
                        print(
    f"Puls={self.res.puls_curent} | "
    f"Emotie={emotie} | "
    f"Agitatie={self.analyzer.agitatie_cap}"
)

                        print(f"⚡ Scor stres instant: {scor_stres}")
                        timp_actual = time.time() 

                        
                        if scor_stres >= 5 and (timp_actual - self.timp_ultimul_sfat >= 60):
                            if scor_stres >= 8:
                                self.res.sfat.put("Observ semne puternice de stres. Vrei să facem un exercițiu de respirație?")
                            else:
                                self.res.sfat.put("Pari puțin tensionat. Ia o scurtă pauză.")
                            
                            self.timp_ultimul_sfat = timp_actual 

                        if stres_instant:
                            print(" STRES INSTANT DETECTAT")
                        timp_actual = time.time()
                        
                        
                        if emotie == "sad": self.k_sad += 1
                        else: self.k_sad = 0
                        
                        
                        if timp_actual - self.ultimul_update_baseline >= 60:
                            self.baseline = 0.9 * self.baseline + 0.1 * self.res.puls_curent
                            print(f"📈 [BIOMETRIC] Nou Baseline: {self.baseline:.1f}")
                            self.save_baseline(self.baseline)
                            self.trimite_date_aplicatie(self.res.puls_curent, emotie, self.alerta)
                            self.ultimul_update_baseline = timp_actual
                            
                        print(f" Stres: {emotie} | Stres Fizic: {stres_fizic} | Puls: {self.res.puls_curent}")
                        
                       
                        nivel_critic = (
    stres_instant or
    self.res.puls_curent > self.baseline + 20 or
    (emotie in ["fear", "angry"] and self.res.puls_curent > self.baseline + 15) or
    (emotie == "sad" and self.res.puls_curent > self.baseline + 10) or
    (self.k_sad >= 30)
)
                        
                        timp_curent_ms = pygame.time.get_ticks()
                        
                        if nivel_critic:
                            if not self.este_stresat:
                                self.alerta = True
                                print("Nivel crescut de stres. ")
                                self.este_stresat = True
                                self.timp_curent_stress = timp_curent_ms
                            else:
                                timp_trecut = timp_curent_ms - self.timp_curent_stress
                                
                                if timp_trecut >= 5000:
                                    
                                    if (timp_curent_ms - self.timp_ultimul_sfat >= 120000) and not self.res.generating:
                                        print(" Stres confirmat! ")
                                        prompt = f"User is stressed ({emotie}), HR: {self.res.puls_curent}. Give a short calming response in Romanian (max 15 words)."
                                        
                                        response = self.client.chat.completions.create(
                                            model="gpt-4o-mini",
                                            messages=[{"role": "user", "content": prompt}]
                                        )
                                        raspuns_text = response.choices[0].message.content
                                        
                                       
                                        self.res.sfat.put(raspuns_text)
                                        self.timp_ultimul_sfat = timp_curent_ms
                                        
                        else:
                            if self.este_stresat:
                                print("Resetez.")
                                self.alerta = False
                                self.este_stresat = False
                                self.k_sad = 0
                    else:
                        self.alerta = False
            
                        
            except Exception as e:
                print(f" [BIOMETRIC Eroare]: {e}")
                
           
            time.sleep(2)
    def detecteaza_puls_brusc(self):
        if len(self.istoric_puls) < 10:
            return False

        return self.istoric_puls[-1] - self.istoric_puls[0] >= 10
    def calculeaza_scor_stres_instant(self, emotie):
       
        scor = 0
        
        if self.detecteaza_puls_brusc():
            scor += 4
            
        if self.analyzer.agitatie_cap > 5:
            scor += 2
        if self.res.volum_curent >5000:
            scor+=1
        if emotie == "fear":
            scor += 3
        elif emotie == "angry":
            scor += 3
        elif emotie == "sad":
            scor += 1
            
        if self.res.puls_curent > self.baseline + 15:
            scor += 2
            
        return scor

    def detecteaza_stres_instant(self, emotie):
       
        scor = self.calculeaza_scor_stres_instant(emotie)
        return scor >= 5
    def stop(self):
        self.running = False


def deschide_camera(camera_obj):
    
    try:
        
        camera_obj.start_preview(gl_preview=True, window=(100, 100, 640, 480))
        
        timp_start = pygame.time.get_ticks()
        while pygame.time.get_ticks() - timp_start < 5000:
            for event in pygame.event.get():
                pass 
            pygame.time.delay(10)
            
        camera_obj.stop_preview()
        
    except Exception as e:
        print("\n" + "="*50)
        print(" [EROARE CAMERĂ]:")
        traceback.print_exc()
        print("="*50 + "\n")

 

lista_sfaturi = [
     "Ia o pauză de 5-10 minute.",
     "Fă o scurtă plimbare.",
     "Ascultă muzică relaxantă.",
     "Relaxează-ți umerii și postura.",
     "Bea apă.",
     "Fă câteva întinderi ușoare.",
     "Ia o pauză scurtă de la ecran.",
     "Privește un obiect la distanță timp de 20 de secunde.",
    "Inspiră adânc și expiră lent de trei ori.",
    "Aerisește camera în care lucrezi.",
    "Spală-te pe față cu apă rece pentru revigorare.",
    "Clipește conștient de câteva ori pentru a-ți hidrata ochii.",
    "Verifică dacă strângi din dinți și relaxează-ți maxilarul.",
    "Rotește-ți încheieturile mâinilor și gleznele.",
    "Pune telefonul pe 'Do Not Disturb' pentru a te concentra mai bine.",
    "Ridică-te de pe scaun și întinde-ți spatele.",
    "Curăță-ți ecranul monitorului și ochelarii."
]

def main():
   
    if not init_hardware():
        print("Sistemul hardware nu a putut fi inițializat.")
        sys.exit()

    
    res = ResourceManager()
    res.load_all_assets()
    
    
    ui = BimoUI(res)
    utils = SystemUtils(res)
    analyzer = StressAndEmotionAnalyzer()
    dialog_manager = DialogManager(res, res.client)

    
    time.sleep(0.5)
   

    

    
    ui.loading_screen(ecran, "Inițializez conexiunea cu brățara", 3, mijloc_x, mijloc_y)
    hr_manager = HeartRateManager(res.inima)
    hr_manager.daemon = True 
    hr_manager.start()
    time.sleep(5)

    ui.loading_screen(ecran, "Inițializez audio", 3, mijloc_x, mijloc_y)
    audio_manager = AudioManager(res.dialog)
    audio_manager.daemon = True
    audio_manager.start()
    time.sleep(1)

    ui.loading_screen(ecran, "Inițializez asistentul AI", 3, mijloc_x, mijloc_y)
    
    biometric_monitor = BiometricMonitor(res, analyzer, res.client, camera) 
    biometric_monitor.daemon = True
    biometric_monitor.start()
    time.sleep(1)

    ui.loading_screen(ecran, "Sistem configurat!", 2, mijloc_x, mijloc_y)
    utils.spune("Inițializare completă.")
    threading.Thread(target=bimo.homing).start()
    time.sleep(1)

    
    running = True
    ceas = pygame.time.Clock()
    
    sfat_curent_ales = ""
    timp_start_sfat = 0
    exercising = False
    font_puls = pygame.font.SysFont("Arial", 30, bold=True)
    culoare_bula = (100, 200, 255)
    
    print("🤖 Bimo este activ și ascultă!")

    while running:
       
        ecran.blit(res.assets["fundal"], (0, 0))
        timp_curent_ms = pygame.time.get_ticks()

       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        
        text_puls = f"Puls: {res.puls_curent} BPM"
        suprafata_puls = font_puls.render(text_puls, True, (255, 255, 255))
        latime_text = suprafata_puls.get_width()
        ecran.blit(suprafata_puls, (ecran.get_width() - latime_text - 20, 20))

        
        if res.buton.is_pressed:
            timp_apasare = time.time()
            if hasattr(res, 'timp_ultima_apasare') and (timp_apasare - res.timp_ultima_apasare < 0.6):
                ui.loading_screen(ecran, "Oprire sistem", 3, mijloc_x, mijloc_y)
                utils.spune("Sistemele se închid în siguranță. Nu uita să te relaxezi. La revedere!")
                utils.shutdown_bimo(camera)
            else:
                res.timp_ultima_apasare = time.time()

        if not res.dialog.empty():
            mesaj = res.dialog.get_nowait()
            
            if mesaj == "WAKE_WORD_DETECTAT":
               
                threading.Thread(target=bimo.salut).start()
                timpul_de_acum = utils.data_curenta()
                dialog_manager.initiaza_conversatia(res.puls_curent, analyzer.ultima_emotie_cunoscuta, analyzer.nivel_stres_fizic, audio_manager,timpul_de_acum)
                
                
                
            elif mesaj=="OPRIRE_SISTEM":
                
                ui.loading_screen(ecran, "Oprire sistem", 3, mijloc_x, mijloc_y)
                utils.spune("Sistemele se închid în siguranță. La revedere!")
                time.sleep(3)
                utils.shutdown_bimo(camera)
                
            elif mesaj=="CE_VEZI":
                ui.loading_screen(ecran, "Inițializare feed video", 2, mijloc_x, mijloc_y)
                deschide_camera(camera) 
            
            elif mesaj=="RELAXARE":
                utils.spune("Inițiez sesiunea de relaxare.Procesul va dura aproximativ un minut.")
                last_exercise = timp_curent_ms
                res.stare_interfata=2
            elif any(cuvant in mesaj.lower() for cuvant in ["prezentare", "prezinta-te", "prezintă te"]):
                ui.loading_screen(ecran, "Initializez prezentarea", 2, mijloc_x, mijloc_y)
                utils.spune("Salutare! Numele meu este Bimo. Sunt companionul de încredere în momentele de stres, creat de TDS Robotics. Datele tale sunt în siguranță cu mine pe plan local.")
                res.stare_interfata = 0
                
            else:
                
                utils.spune(mesaj)
                ui.afiseaza_raspuns(ecran, mesaj, 4)
        if not res.inima.empty():
            res.puls_curent = res.inima.get()
            print(f" Puls actualizat: {res.puls_curent}")
        if not res.sfat.empty():
            sfat_ai = res.sfat.get_nowait()
            utils.trimite_alerta_telegram(f"Alertă Bimo: Stres ridicat detectat ({res.puls_curent} BPM). Am intervenit.")
            threading.Thread(target=bimo.dezaprobare).start()
            
            res.stare_interfata = random.choice([1, 4]) 

        
        if res.stare_interfata == 0:
            
            ui.deseneaza_fata(ecran, mijloc_x, mijloc_y)

        elif res.stare_interfata == 1:
            
            ui.scrie_mesaj(ecran, "Vrei să facem un exercițiu de respirație?", font_bimo, mijloc_x+100, mijloc_y)
            utils.spune("Vrei să facem un exercițiu de relaxare?")
            
            
            text_spus=asculta_conversatia(dialog_manager.recognizer)
            if text_spus=="da" or text_spus=="confirm":
                last_exercise = timp_curent_ms
                res.stare_interfata = 2
                
            elif text_spus=="nu" or text_spus=="anulare":
                res.stare_interfata=0

        elif res.stare_interfata == 2:
            
            ui.exercitiu_respiratie(ecran, mijloc_x, mijloc_y, 150, culoare_bula)
            exercising = True
            
            
            if timp_curent_ms - last_exercise > 60000:
                exercising = False
                utils.spune("Sper că te simți mai bine. Dacă mai ai nevoie de ceva, sunt aici.")
                res.stare_interfata = 0

        elif res.stare_interfata == 3:
            
            numar_puncte = (timp_curent_ms // 500) % 4
            text_gandit = "Ascult" + "." * numar_puncte
            ui.scrie_mesaj(ecran, text_gandit, font_bimo, mijloc_x, mijloc_y)

        elif res.stare_interfata == 4:
            
            if sfat_curent_ales == "":
                sfat_curent_ales = random.choice(lista_sfaturi)
                timp_start_sfat = time.time()
                utils.spune(sfat_curent_ales)
            
            ui.scrie_mesaj(ecran, sfat_curent_ales, font_bimo, mijloc_x, mijloc_y)
            
            if time.time() - timp_start_sfat >= 10.0:
                res.stare_interfata = 0      
                sfat_curent_ales = ""

        elif res.stare_interfata == 5:
            
            ui.scrie_mesaj(ecran, "Vrei să facem o meditație profundă (10 minute)?", font_bimo, mijloc_x, mijloc_y)
            utils.spune("Vrei să pornesc o meditație video?")
            time.sleep(2)
            res.stare_interfata = 6 

        elif res.stare_interfata == 6:
            
            utils.spune("Inițiez sesiunea de calmare. Relaxează-te.")
            utils.ruleaza_meditatie_youtube() # Funcția oprește pygame audio și deschide mpv
            res.stare_interfata = 0

       
        pygame.display.flip()
        ceas.tick(30) 

    
    print("🛑 [SISTEM] Programul a fost oprit. Curățare memorie...")
    
    
    audio_manager.stop()
    biometric_monitor.stop()
    time.sleep(0.5) 
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


