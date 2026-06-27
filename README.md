# Bimo-Companion
BIMO este un companion inteligent de birou conceput pentru prevenirea stresului și monitorizarea stării de bine a utilizatorului în timp real
,
,
. Acesta dispune de o prezență fizică proactivă și o interfață bazată pe AI pentru comunicare naturală, oferind suport personalizat și exerciții de relaxare ghidate
,
,
. Sistemul integrează analiză multi-senzorială — incluzând monitorizarea ritmului cardiac, analiza micro-expresiilor faciale și recunoașterea tonului vocii — pentru a identifica semnele timpurii de burnout înainte ca acestea să escaladeze
,
,
. Construit pe o platformă hardware accesibilă (Raspberry Pi) cu inteligență artificială integrată, BIMO facilitează o relație mai sănătoasă cu tehnologia, transformând-o într-un partener empatic dedicat echilibrului emoțional și productivități

## 🛠 Tehnologii Utilizate
- **Hardware:**
  - Raspberry Pi 5 (4GB RAM)
  - Cameră video (Module AI)
  - Senzori Biometrici (Bluetooth Low Energy)
  - Șasiu printat 3D (r-PETG)
- **Software:**
  - **Limbaj:** Python 
  - **Computer Vision:** OpenCV, DeepFace (pentru detecția stărilor faciale)
  - **Comunicații:** Protocol BLE (securizat cu AES-128)
  - **Edge Computing:** Procesare locală pentru confidențialitatea datelor

##  Funcționalități Cheie
- **Sensor Fusion:** Corelarea datelor de puls cu expresiile faciale pentru eliminarea alarmelor false.
- **Degradare Elegantă:** Funcționare parțială offline (Edge Computing) chiar și fără conexiune la internet.
- **Design Sustenabil:** Optimizat termic și printat din materiale reciclate.

## 📦 Structura Proiectului
```text
Bimo/
├── src/           # Codul sursă Python
├── models/        # Modele pre-antrenate (DeepFace, etc.)
├── 3d_files/      # Fișierele STL pentru șasiu
├── docs/          # Documentație tehnică și scheme
└── requirements.txt # Dependențe
