# Numere pseudo-aleaotrii & metode de producere 

## 1. Generarea de numere pseudoaleatorii 
Numerele pseudoaleatorii sunt valori generate de un algoritm într-un limbaj de programare, care par aleatorii, dar sunt de fapt determinate și predictibile. Ele nu sunt cu adevărat aleatorii, ci „fals aleatorii”.  

Generatoarele de numere pseudoaleatoare (PRNG – Pseudorandom Number Generators) sunt algoritmi care produc secvențe de numere ale căror proprietăți se apropie de cele ale numerelor aleatoare. Acestea sunt esențiale în aplicații precum simulările (de exemplu, metoda Monte Carlo), jocurile electronice (pentru generare procedurală) și criptografia. Proprietățile statistice bune reprezintă o cerință fundamentală pentru un PRNG.  

### 1.1 Generatori bazați pe recurențe liniare 
În a doua jumătate a secolului XX, generatoarele congruențiale liniare (LCG) au reprezentat standardul PRNG, deși calitatea lor era recunoscută ca fiind insuficientă. Un progres major l-a constituit introducerea tehnicilor bazate pe recurențe liniare peste F 2 (câmpul cu două elemente), înrudite cu registrele de deplasare cu reacție liniară (LFSR). 

### 1.2 Generatoare bazate pe contor 
Un Generator bazat pe Contor (CBRNG) este un tip PRNG care utilizează o cheie (key) fixă și un contor întreg ca unică stare internă. Aceste generatoare sunt esențiale în calculele paralele de mare amploare (GPU-uri sau clustere de procesoare CPU) datorită avantajelor lor structurale. 

## 2. Generator pentru aplicații criptografie
PRNG-urile obișnuite nu sunt potrivite pentru criptografie deoarece sunt ușor de prezis dacă starea lor internă este compromisă. Odată ce un atacator obține această stare, el poate calcula atât secvența generată anterior, cât și pe cea viitoare. Din acest motiv sunt necesare generatoare mult mai sigure — CSPRNG-urile — care, pe lângă calitățile statistice ale unui PRNG, includ și mecanisme criptografice ce le protejează împotriva analizelor inverse.

### 2.1. Proprietăți CSPRNG
Un CSPRNG este definit prin două categorii de proprietăți: 

1. Impredictibilitate (Next Bit step)  
Chiar dacă un atacator cunoaște o parte mare din ieșirile generatorului, el nu trebuie să poată prezice bitul următor mai bine decât prin ghicit (50%). Dacă această condiție este îndeplinită, generatorul este considerat sigur din punct de vedere statistic.

2. Rezistența la compromiterea stării  
- Forward Secrecy: Dacă starea internă este dezvăluită la un moment dat, atacatorul nu trebuie să poată recupera ieșirile generate în trecut. Astfel, cheile sau secretele deja folosite rămân protejate.  
- Backward Secrecy: Dacă starea a fost compromisă, generatorul trebuie să poată integra rapid entropie nouă (reînsămânțare), astfel încât ieșirile viitoare să nu mai fie predictibile pentru atacator.

### 2.2. Sursa de Entropie și Rolul Seedului 
Securitatea unui CSPRNG depinde de seed, adică valoarea inițială cu care este pornit generatorul. Seed-ul trebuie să provină dintr-o sursă imprevizibilă de entropie (TRNG): zgomot hardware, evenimente de I/O, latențe, sau senzori specializați. Sistemele de operare colectează acea entropie într-un „pool” dedicat și o oferă la inițializarea și reînsămânțarea CSPRNG-urilor. Dacă seed-ul este slab sau predictibil, întreaga securitate a generatorului este compromisă, motiv pentru care CSPRNG-urile includ mecanisme de reseeding periodic, pentru a restabili Backward Secrecy și pentru a preveni atacurile pe termen lung. 

### 2.3. Modele criptografice
Generatoarele criptografice sigure sunt cunoscute sub numele de Deterministic Random Bit Generators (DRBG) și sunt standardizate pentru a garanta robustețea.

1. Abordarea Standardizată  
Majoritatea CSPRNG-uirlor moderne respectă specificațiile NIST SP 800-90A, care definește trei mecanisme de generare, toate bazate pe primitive bine studiate:  
- Hash DRBG: Utilizează o funcție hash criptografică (ex. SHA-256) pentru a genera biții și pentru a actualiza starea.  
- HMAC DRBG: Utilizează funcția HMAC (Hash-based Message Authentication Code), care oferă o securitate teoretică mai robustă decât Hash DRBG-ul simplu.  
- CTR DRBG: Utilizează un cifru pe bloc (ex. AES) în modul Counter (CTR) pentru a genera secvența de biți.

2. Sursa de Entropie (Seed-ul)  
Pentru a fi sigure, DRBG-urile necesită un seed provenit dintr-o sursă de entropie reală (True Random Number Generator). Entropia este colectată din fenomene fizice imprevizibile precum zgomotul electronic, mișcările utilizatorului sau timpii de latență ai sistemului.  
Sistemele de operare acumulează aceste informații într-un „pool” de entropie și le expun prin interfețe precum /dev/random, /dev/urandom (Linux) sau API-uri specifice precum Windows CryptoAPI. Această entropie este necesară atât la inițializare, cât și la re-seeding, pentru a asigura impredictibilitatea pe termen lung.

## 3. Implementare de PRNG

Acest capitol prezintă implementarea a 4 versiuni diferite de generare de numere pseudo-aleatoare folosind Python. Limbajul Python a fost ales datorită ușurinței sale de scriere și înțelegere. 

- **[random_numbers.py](Code-Source/random_numbers.py)**: Programul trimite o cerere către **random.org** pentru a primi un **număr aleator** între 0 și 100. Dacă răspunsul este valid, extrage numărul și îl afișează.  
- **[rnd_numbers.py_v2](Code-Source/rnd_numbers_v2.py)**: Programul trimite o cerere către **ANU Quantum Random Number Generator API**, care generează numere aleatoare folosind **fenomene cuantice reale**. API-ul returnează informația în format **JSON**, de aceea se folosește și librăria `json`.  
- **[rnd_numbers_v2_timeout.py](Code-Source/rnd_numbers_v2_timeout.py)**: Programul trimite o cerere către API-ul ANU pentru a obține un număr aleator cuantic și îl afișează dacă totul este în regulă. Dacă serverul indică că a fost depășită limita de un request pe minut, programul așteaptă automat 60 de secunde și reîncearcă. Folosește o funcție separată care gestionează cererea, răspunsul și eventualele erori, făcând codul mai organizat decât celelalte versiuni.  
- **[secrets.py]()**: Programul generează local un token de autentificare securizat folosind modulul `secrets` și îl folosește într-o cerere HTTP către un API extern. Token-ul este trimis în header-ul Authorization, iar programul verifică dacă cererea a avut succes și extrage datele JSON returnate de API. Gestionarea erorilor de rețea și HTTP este realizată elegant, afișând fie rezultatul API-ului, fie mesajul de eroare. Comparativ cu celelalte programe, acesta nu generează numere de la un server, ci creează token-ul local și îl folosește pentru autentificare.

---
### Funcții și librării comune
- **`requests`** – trimite cereri HTTP și primește răspunsuri, permite verificarea codului de status, preluarea textului sau JSON-ului și tratarea erorilor.  
- **`json()`** – folosit pentru a parsa răspunsurile JSON și a accesa datele într-un mod structurat.  
- **`int()`** – transformă textul în număr întreg acolo unde este necesar.  
- **`try/except`** – previne blocarea aplicației în caz de erori de rețea, API sau conversie.  
- **`time.sleep()`** – folosit pentru implementarea pauzelor automate și retry logic (în programele cu rate-limit).  
- **`secrets`** – permite generarea de token-uri criptografic sigure pentru autentificare și securitate.

---

### Avantaje comune
- Gestionarea erorilor face programele robuste și previne crash-uri.  
- Permite obținerea de date reale sau simulate de la API-uri fără a implementa algoritmi complexi.  
- Structurarea codului în funcții (retry, tratamentul răspunsurilor) crește lizibilitatea și modularitatea.  
- Folosirea librăriilor standard (`requests`, `json`, `secrets`) face codul portabil și ușor de întreținut.
---

### Dezavantaje & Limitări
- Dependența de conexiune la internet și de disponibilitatea API-urilor externe.  
- Limitările rate-limit (1 request/minut la ANU RNG) pot încetini testarea și execuția rapidă.  
- Random.org și ANU RNG pot introduce latențe din cauza traficului sau restricțiilor serverului.  
- `secrets.py` generează date local, dar nu produce numere aleatoare cuantice.  
- Conversia la `int()` sau JSON parsing poate genera erori dacă API-ul schimbă structura răspunsului.

---
### Observații utile
- Programele oferă exemple de **interacțiune API în Python**, combinând generarea sigură de date și randomizare.  
- Folosirea unei funcții dedicate pentru retry (`rnd_numbers_v2_timeout.py`) este un exemplu de **programare robustă și modulară**.  
- Comparația între pseudo-random (`random.org`) și quantum random (`ANU RNG`) evidențiază diferențele dintre generarea locală, pseudo-random și quantum random.

---

## 4. Testare și concluzii

### 4.1 Testarea programelor
- **random_numbers.py**: verificarea numerelor în intervalul 0–100 și corectitudinea răspunsului API.  
- **rnd_numbers.py_v2**: validarea numerelor cuantice și a formatului JSON.  
- **rnd_numbers_v2_timeout.py**: testarea retry logic și a limitării rate-limit, confirmând robustețea funcției `fetch_quantum_number`.  
- **secrets.py**: verificarea generării token-urilor, a header-ului Authorization și gestionarea erorilor HTTP și de rețea.

### 4.2 Observații din testare
- Toate programele gestionează erorile comune (rețea, server, rate-limit).  
- Funcțiile modulare cresc lizibilitatea și întreținerea codului.  
- Latențele și timpul de răspuns diferă între API-uri; generarea locală (`secrets.py`) este instantanee.  
- Testarea evidențiază diferențele dintre pseudo-random, quantum random și generarea locală.

### 4.3 Concluzii
- Programele demonstrează abordări diferite pentru generarea numerelor aleatoare: pseudo-random, quantum random și generare locală criptografică.  
- Pentru securitate, `secrets.py` este recomandat datorită siguranței token-urilor și independenței de servere externe.  
- Pentru simulări sau aplicații statistice, ANU RNG oferă adevărat randomness, cu limitările de performanță asociate.  
- Retry logic și tratarea rate-limit-ului sunt practici bune pentru robustețea aplicațiilor care interacționează cu API-uri.  
- Combinarea generării locale și externe poate optimiza performanța și calitatea numerelor aleatoare.

---
## 5. Bibliografie
- (https://en.wikipedia.org/wiki/Cryptographically_secure_pseudorandom_number_generator)
- (https://www.youtube.com/watch?v=mkYdI6pyluY )
- (https://cryptography.io/en/latest/random-numbers/)
- (https://cryptobook.nakov.com/secure-random-generators)

