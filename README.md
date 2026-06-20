# Bimo-Companion
Robot companion de birou bazat pe AI, dezvoltat de echipa TDS Robotics. Bimo utilizează Computer Vision  și senzori biometrici (BLE) pentru a monitoriza stresul și a oferi suport emoțional utilizatorului. Proiect sustenabil, construit pe Raspberry Pi 5 pentru procesare Edge.
# Bimo: AI Desktop Companion 🤖

Bimo este un asistent digital personalizat, conceput pentru a oferi suport emoțional și a reduce stresul la locul de muncă sau de studiu. Proiectul a fost dezvoltat de echipa **TDS Robotics** și a obținut **Top 10 Național** la categoria „AI for Good”.

## 🚀 Despre Proiect
Bimo nu este doar un robot, ci un companion empatic. Construit pentru a combate epuizarea , Bimo utilizează fuziunea de senzori și viziunea computerizată pentru a detecta nivelul de stres al utilizatorului și pentru a interveni proactiv cu sfaturi și exerciții de relaxare.

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

## 🧠 Funcționalități Cheie
- **Sensor Fusion:** Corelarea datelor de puls cu expresiile faciale pentru eliminarea alarmelor false.
- **Degradare Elegantă:** Funcționare parțială offline (Edge Computing) chiar și fără conexiune la internet.
- **Design Sustenabil:** Optimizat termic și printat din materiale reciclate.

## 📸 Galerie / Media
*(Aici adaugă link-uri către poze cu Bimo sau un GIF cu interfața lui)*
- [Vezi Bimo în acțiune - Video] (link_aici)

## 📦 Structura Proiectului
```text
Bimo/
├── src/           # Codul sursă Python
├── models/        # Modele pre-antrenate (DeepFace, etc.)
├── 3d_files/      # Fișierele STL pentru șasiu
├── docs/          # Documentație tehnică și scheme
└── requirements.txt # Dependențe
