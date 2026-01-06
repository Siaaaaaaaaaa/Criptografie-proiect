# Numere pseudo-aleaotrii & metode de producere 

## 1. Generarea de numere pseudoaleatorii 
Numerele pseudoaleatorii sunt valori generate de un algoritm într-un limbaj de programare, care par aleatorii, dar sunt de fapt determinate și predictibile. Ele nu sunt cu adevărat aleatorii, ci „fals aleatorii”. Generatoarele de numere pseudoaleatoare (PRNG – Pseudorandom Number Generators) sunt algoritmi care produc secvențe de numere ale căror proprietăți se apropie de cele ale numerelor aleatoare. Printre astfel de generatoare se numără și cei bazați pe recurențe liniare, precum și cei bazați pe contor. Acestea sunt esențiale în aplicații precum simulările (de exemplu, metoda Monte Carlo), jocurile electronice (pentru generare procedurală) și criptografia. Proprietățile statistice bune reprezintă o cerință fundamentală pentru un PRNG. 

### 1.1 Generatoare bazate pe recurențe liniare 
În a doua jumătate a secolului XX, generatoarele congruențiale liniare (LCG) au reprezentat standardul PRNG, deși calitatea lor era recunoscută ca fiind insuficientă. Un progres major l-a constituit introducerea tehnicilor bazate pe recurențe liniare peste F 2 (câmpul cu două elemente), înrudite cu registrele de deplasare cu reacție liniară (LFSR). 

### 1.2 Generatoare bazate pe contor 
Un Generator bazat pe Contor (CBRNG) este un tip PRNG care utilizează o cheie (key) fixă și un contor întreg ca unică stare internă. Aceste generatoare sunt esențiale în calculele paralele de mare amploare (GPU-uri sau clustere de procesoare CPU) datorită avantajelor lor structurale. 

## 2. Generator pentru aplicații criptografie
PRNG-urile obișnuite nu sunt potrivite pentru criptografie deoarece sunt ușor de prezis dacă starea lor internă este compromisă. Odată ce un atacator obține această stare, el poate calcula atât secvența generată anterior, cât și pe cea viitoare. Din acest motiv sunt necesare generatoare mult mai sigure — CSPRNG-urile — care, pe lângă calitățile statistice ale unui PRNG, includ și mecanisme criptografice ce le protejează împotriva analizelor inverse.

### 2.1. Proprietăți CSPRNG
Un CSPRNG este definit prin două categorii de proprietăți: **impredictibilitate (Next Bit step)** și **reizstenșa la compromiterea stării**. Impredictibilitatea se referă la proprietatea conform căreia, chiar dacă un atacator cunoaște o parte mare din ieșirile generatorului, acesta nu poate prezice următorul bit generat cu o probabilitate semnificativ mai mare decât 1/2. Dacă această condiție este îndeplinită, generatorul este considerat sigur din punct de vedere statistic, deoarece niciun algoritm polinomial nu poate distinge între ieșirile sale și o secvență aleatoare ideală cu un avantaj neneglijabil. În ceea ce privește rezistența la compromiterea stării, această proprietate constă în capacitatea unui CSPRNG de a izola impactul unei compromiteri a stării interne la un anumit moment în timp. Mai exact, această proprietate asigură că divulgarea stării nu permite atacatorului să reconstruiască ieșirile generate anterior (Forward Secrecy) și nici să prezică ieșirile viitoare, odată ce generatorul a fost reînsămânțat cu entropie nouă (Backward Secrecy). Astfel, compromiterea are efecte limitate temporal, iar securitatea pe termen lung a generatorului este menținută.

### 2.2. Sursa de Entropie și Rolul Seedului 
Securitatea unui CSPRNG depinde de seed, adică valoarea inițială cu care este pornit generatorul. Seed-ul trebuie să provină dintr-o sursă imprevizibilă de entropie (TRNG): zgomot hardware, evenimente de I/O, latențe, sau senzori specializați. Sistemele de operare colectează acea entropie într-un „pool” dedicat și o oferă la inițializarea și reînsămânțarea CSPRNG-urilor. Dacă seed-ul este slab sau predictibil, întreaga securitate a generatorului este compromisă, motiv pentru care CSPRNG-urile includ mecanisme de reseeding periodic, pentru a restabili Backward Secrecy și pentru a preveni atacurile pe termen lung. 

### 2.3. Modele criptografice
Generatoarele criptografice sigure sunt cunoscute sub denumirea de **Deterministic Random Bit Generators (DRBG)** și sunt standardizate pentru a garanta robustețea și securitatea utilizării lor în aplicații criptografice. Majoritatea CSPRNG-urilor moderne respectă specificațiile NIST SP 800-90A, care definesc mecanisme de generare bazate exclusiv pe primitive criptografice bine studiate și considerate sigure.

Printre aceste mecanisme se numără generatoarele bazate pe funcții hash criptografice, _precum SHA-256_, care sunt utilizate atât pentru producerea secvențelor de biți, cât și pentru actualizarea stării interne a generatorului. O variantă mai robustă din punct de vedere teoretic este reprezentată de DRBG-urile bazate pe HMAC, care folosesc funcția _Hash-based Message Authentication Code_ pentru a oferi garanții de securitate suplimentare. De asemenea, sunt utilizate și generatoare bazate pe cifre pe bloc, precum AES, care operează în modul Counter (CTR) pentru a produce secvențe pseudo-aleatoare de biți.

Pentru a asigura securitatea, orice DRBG necesită un seed inițial provenit dintr-o sursă de entropie reală, furnizată de un True Random Number Generator. Această entropie este obținută din fenomene fizice imprevizibile. Sistemele de operare colectează și acumulează aceste informații într-un „pool” de entropie, pe care îl pun la dispoziția aplicațiilor prin interfețe specifice, precum /dev/random și /dev/urandom în Linux sau prin API-uri dedicate, cum este Windows CryptoAPI. Entropia astfel obținută este esențială atât în faza de inițializare a generatorului, cât și în procesele de reînsămânțare, pentru a menține impredictibilitatea și securitatea pe termen lung.

---
## 3. Implementare de PRNG

Acest capitol prezintă implementarea a 4 versiuni diferite de generare de numere pseudo-aleatoare folosind Python. Limbajul Python a fost ales datorită ușurinței sale de scriere și înțelegere. 

- **[random_numbers.py](Code-Source/random_numbers.py)**: Programul trimite o cerere către **random.org** pentru a primi un **număr aleator** între 0 și 100. Dacă răspunsul este valid, extrage numărul și îl afișează.  
- **[rnd_numbers.py_v2](Code-Source/rnd_numbers_v2.py)**: Programul trimite o cerere către **ANU Quantum Random Number Generator API**, care generează numere aleatoare folosind **fenomene cuantice reale**. API-ul returnează informația în format **JSON**, de aceea se folosește și librăria `json`.  
- **[rnd_numbers_v2_timeout.py](Code-Source/rnd_numbers_v2_timeout.py)**: Programul trimite o cerere către API-ul ANU pentru a obține un număr aleator cuantic și îl afișează dacă totul este în regulă. Dacă serverul indică că a fost depășită limita de un request pe minut, programul așteaptă automat 60 de secunde și reîncearcă. Folosește o funcție separată care gestionează cererea, răspunsul și eventualele erori, făcând codul mai organizat decât celelalte versiuni.  
- **[secrets.py]()**: Programul generează local un token de autentificare securizat folosind modulul `secrets` și îl folosește într-o cerere HTTP către un API extern. Token-ul este trimis în header-ul Authorization, iar programul verifică dacă cererea a avut succes și extrage datele JSON returnate de API. Gestionarea erorilor de rețea și HTTP este realizată elegant, afișând fie rezultatul API-ului, fie mesajul de eroare. Comparativ cu celelalte programe, acesta nu generează numere de la un server, ci creează token-ul local și îl folosește pentru autentificare.

Drept funcții și librării comune, regăsim în toate cele patru surde cod următoarele: **`requests`**, funcție ce trimite cereri HTTP și primește răspunsuri, permite verificarea codului de status, preluarea textului sau JSON-ului și tratarea erorilor.  **`json()`** este folosit pentru a parsa răspunsurile JSON și a accesa datele într-un mod structurat. **`int()`** transformă textul în număr întreg acolo unde este necesar, **`try/except`** previne blocarea aplicației în caz de erori de rețea, API sau conversie. În final, mai regăsim și **`time.sleep()`** care este folosit pentru implementarea pauzelor automate și retry logic (în programele cu rate-limit).  și librăria **`secrets`**, ce permite generarea de token-uri criptografic sigure pentru autentificare și securitate.

### 3.1 Avantaje comune
Remarcaăm ca prim avantaj, faptul că toate programele folosesc librăriile standard ce fac codul portfabil și ușor de întreținut. De asemenea, toate cele patru programe sunt structurare în funcții - aspect ce crește lizibilitatea și modularitatea codului. Un alt avantaj regăsit printre cele 4 surse îl constituie faptul că programele permit obținerea de date reale sau simulate de la API-uri, fără a implementa aglorimit complexi. 

### 3.2. Dezavantaje & Limitări
În schimb, când vine vorba de dezavntaje & limitări, remarcăm dependența de conexiune la internet și de disponibilitatea API-urilor externe, precum și limitările cu privire la rate-limit (1 request/minut la ANU RNG) ce pot încetini testarea și execuția rapidă. De asemenea, un alt dezavantaj îl reprezintă faptul că Random.org și ANU RNG pot introduce latențe din cauza traficului sau restricțiilor serverului. `secrets.py` generează date local, dar nu produce numere aleatoare cuantice, iar conversia la `int()` sau JSON parsing poate genera erori dacă API-ul schimbă structura răspunsului.

### 3.3 Concluzii
Programele analizate ilustrează abordări diferite pentru generarea numerelor aleatoare, incluzând metode pseudo-aleatoare, generare cuantică și generare locală criptografică. Acestea evidențiază, totodată, modul în care Python poate fi utilizat pentru interacțiunea cu API-uri externe, combinând generarea sigură de date cu mecanisme de randomizare. Din perspectiva securității, utilizarea modulului `secrets` este recomandată datorită generării locale de token-uri criptografic sigure și independenței față de servere externe. Pentru simulări și aplicații statistice, generatoarele cuantice precum ANU RNG oferă un nivel ridicat de aleatoriu real, însă cu limitări de performanță impuse de accesul prin API. Implementarea mecanismelor de retry și gestionarea rate-limit-ului contribuie semnificativ la robustețea aplicațiilor care comunică cu servicii externe, iar combinarea generării locale cu surse externe de aleatoriu poate oferi un echilibru optim între performanță și calitatea numerelor generate.

---
### 4. Concluzii
În concluzie, proiectul realizat evidențiază diferențele dintre generatoarele pseudo-aleatoare clasice și generatoarele criptografice sigure, subliniind importanța alegerii corecte a metodei de generare în funcție de domeniul de aplicare. Implementările prezentate demonstrează atât utilizarea surselor externe de aleatoriu real, precum Random.org și ANU Quantum RNG, cât și generarea locală securizată prin intermediul CSPRNG-urilor oferite de sistemul de operare. Testele arată că, deși sursele externe pot oferi un nivel ridicat de entropie, acestea implică limitări de performanță și dependență de infrastructură, în timp ce generarea locală criptografică oferă un compromis optim între securitate, eficiență și disponibilitate. Astfel, utilizarea CSPRNG-urilor locale este recomandată pentru aplicații de securitate, în timp ce generatoarele cuantice sunt mai potrivite pentru simulări și experimente statistice.

---
## 5. Bibliografie
- (https://en.wikipedia.org/wiki/Cryptographically_secure_pseudorandom_number_generator)
- (https://www.youtube.com/watch?v=mkYdI6pyluY )
- (https://cryptography.io/en/latest/random-numbers/)
- (https://cryptobook.nakov.com/secure-random-generators)
