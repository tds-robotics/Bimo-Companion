# Bimo-Companion
BIMO este un companion inteligent de birou conceput pentru prevenirea stresului și monitorizarea stării de bine a utilizatorului în timp real
. Acesta dispune de o prezență fizică proactivă și o interfață bazată pe AI pentru comunicare naturală, oferind suport personalizat și exerciții de relaxare ghidate
. Sistemul integrează analiză multi-senzorială — incluzând monitorizarea ritmului cardiac, analiza micro-expresiilor faciale și recunoașterea tonului vocii — pentru a identifica semnele timpurii de burnout înainte ca acestea să escaladeze
. Construit pe o platformă hardware accesibilă (Raspberry Pi) cu inteligență artificială integrată, BIMO facilitează o relație mai sănătoasă cu tehnologia, transformând-o într-un partener empatic dedicat echilibrului emoțional și productivități


## Utlizare


- Monitorizarea proactivă a stresului și prevenirea burnout-ului în timp real pentru angajați și studenți
- Asistență personalizată pentru sănătatea mintală prin exerciții de respirație și tehnici de relaxare ghidate
- Gestionarea presiunii academice și a emoțiilor din perioadele de examene pentru elevi
- Optimizarea echilibrului work-life și reducerea izolării pentru persoanele care lucrează în regim remote
- Soluții de wellbeing scalabile pentru departamentele de HR corporate și instituțiile educaționale
- Analiză multi-senzorială a stării emoționale (facială, vocală și cardiacă) pentru feedback empatic instantaneu
##  Tehnologii Utilizate
- **Hardware:**
  - Raspberry Pi 5 — Unitatea centrală de procesare pentru rularea modelelor AI și gestionarea logicii de sistem
  - Display (Ecran) — Interfață vizuală pentru afișarea expresiilor "prietenului digital" și a datelor de wellbeing
  - Carcasă imprimată 3D — Structură personalizată pentru protecția componentelor și estetica de companion tangibil
- **Senzori și Input:**
   - Cameră integrată — Utilizată pentru analiza micro-expresiilor faciale în timp real prin biblioteca DeepFace și analiza agitației utilizatorului
   - Microfon sensibil — Captarea vocii pentru recunoașterea tonului, intensității emoționale și procesarea comenzilor vocale
   - Brățară inteligentă  — Monitorizarea continuă a ritmului cardiac, conectată via protocolul Bleak
- **Software & AI:**
   - Python 3 — Limbajul principal utilizat pentru integrarea tuturor modulelor hardware și software
   - OpenAI API (GPT-4.0-mini) — Creierul conversațional pentru dialoguri naturale, suport personalizat și asistență empatică complexă
   - DeepFace & Picamera2 — Suite de procesare a imaginilor pentru detectarea stării emoționale din expresiile feței și detecția nivelurilor de agitație
   - Faster-Whisper & openWakeWord — Tehnologii pentru recunoașterea vocală rapidă și activarea asistentului prin comandă vocală chiar dacă nu există internet
- **Mecanisme de Interacțiune:**
   - Servomotoare și mecanism — Permit rotația capului și mișcări fizice pentru o interacțiune mai naturală și empatică
   - Sistem audio (Difuzor) — Redarea răspunsurilor vocale generate și a ghidajelor pentru exerciții de relaxare

##  Funcționalități Cheie

- Analiză Multi-Senzorială în Timp Real — Monitorizarea simultană a ritmului cardiac (prin brățară inteligentă), a micro-expresiilor faciale (via cameră integrată) și a tonului vocii pentru o imagine completă a stării utilizatorului
- Intervenție Proactivă și Empatică — Spre deosebire de aplicațiile pasive, BIMO observă utilizatorul în mod continuu și inițiază conversația autonom atunci când detectează primele semne de stres
- Comunicare Naturală bazată pe AI — Integrare cu OpenAI GPT pentru dialoguri fluide, susținută de tehnologii de procesare vocală locală precum Faster-Whisper și gTTS (pentru sinteză vocală)
- Asistență Personalizată pentru Relaxare — Oferă ghidaj instantaneu pentru tehnici de respirație, pauze de mișcare și recomandări specifice (ex: hidratare, corectarea posturii sau pauze de ecran)
- Detectare Timpurie a Burnout-ului — Algoritmi de recunoaștere a tiparelor de comportament și a nivelului de agitație pentru a preveni escaladarea stresului în probleme cronice
- Prezență Fizică Tangibilă — Un companion real pe birou, dotat cu un display pentru redarea emoțiilor digitale și o carcasă personalizată imprimată 3D, facilitând o conexiune mai apropiată de cea umană


