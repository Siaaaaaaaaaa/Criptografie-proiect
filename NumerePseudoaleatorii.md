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
a. Forward Secrecy: Dacă starea internă este dezvăluită la un moment dat, atacatorul nu trebuie să poată recupera ieșirile generate în trecut. Astfel, cheile sau secretele deja folosite rămân protejate.
b. Backward Secrecy: Dacă starea a fost compromisă, generatorul trebuie să poată integra rapid entropie nouă (reînsămânțare), astfel încât ieșirile viitoare să nu mai fie predictibile pentru atacator.

### 2.2. Sursa de Entropie și Rolul Seedului 
Securitatea unui CSPRNG depinde de seed, adică valoarea inițială cu care este pornit generatorul. Seed-ul trebuie să provină dintr-o sursă imprevizibilă de entropie (TRNG): zgomot hardware, evenimente de I/O, latențe, sau senzori specializați. Sistemele de operare colectează acea entropie într-un „pool” dedicat și o oferă la inițializarea și reînsămânțarea CSPRNG-urilor.
Dacă seed-ul este slab sau predictibil, întreaga securitate a generatorului este compromisă, motiv pentru care CSPRNG-urile includ mecanisme de reseeding periodic, pentru a restabili Backward Secrecy și pentru a preveni atacurile pe termen lung. 

###2.3. Modele criptografice
Generatoarele criptografice sigure sunt cunoscute sub numele de Deterministic Random Bit Generators (DRBG) și sunt standardizate pentru a garanta robustețea.
