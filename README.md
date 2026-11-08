# Counter of Visits

![CI](https://github.com/Euromperman/counter-of-visits/actions/workflows/ci.yml/badge.svg)
![CI](https://github.com/Euromperman/counter-of-visits/actions/workflows/ci.yml/badge.svg)

Jednostavna Python Flask aplikacija koja koristi Redis bazu podataka za brojanje poseta. Projekat demonstrira kontejnerizaciju pomoću Docker-a, upravljanje servisima pomoću Docker Compose-a, trajno čuvanje podataka, automatsko testiranje i kontinuiranu integraciju (CI) pomoću GitHub Actions-a.

## 1. Arhitektura


```text
       Korisnik
          |
          | HTTP zahtev
          v
   Flask aplikacija
       Port 5000
          |
          | Redis INCR / PING
          v
      Redis server
          |
          v
     Docker volume
      (redis-data)
```



## 2. Preduslovi

Za pokretanje projekta potrebni su:

Git

Docker sa Docker Compose podrškom

Python 3.13 (za lokalno pokretanje testova)

Bash i curl (za healthcheck skriptu)

## 3. Pokretanje aplikacije

### Kloniranje repozitorijuma

```bash
git clone https://github.com/Euromperman/counter-of-visits.git
cd counter-of-visits
```

### Podešavanje promenljivih okruženja

Kopirati primer konfiguracije:

```bash
cp .env.example .env
```

U trenutnoj Docker Compose konfiguraciji `APP_PORT` određuje port na host računaru, dok su parametri povezivanja sa Redisom direktno definisani u `compose.yaml`.

Datoteka `.env` nije uključena u Git repozitorijum.

### Pokretanje servisa

```bash
docker compose up -d --build
```

Ova komanda:

- Gradi Docker image aplikacije.

Provera pokrenutih kontejnera:

```bash
docker compose ps
```

### Zaustavljanje servisa

```bash
docker compose down
```

Ova komanda zaustavlja i uklanja kontejnere, ali ne briše Redis volume, tako da brojač ostaje sačuvan.




Pod pretpostavkom da su Git i Docker Desktop već instalirani i da je Docker Desktop pokrenut:

Korak 1 — Kloniranje repozitorijuma
git clone https://github.com/Euromperman/counter-of-visits.git
cd counter-of-visits


Korak 2 — Kreiranje .env fajla
cp .env.example .env


Korak 3 — Pokretanje aplikacije i Redis servera
docker compose up -d --build


Korak 4 — Provera kontejnera
docker compose ps


Korak 5 — Testiranje endpointa
curl http://localhost:5000/
curl http://localhost:5000/visits
curl -i http://localhost:5000/health


Korak 6 — Pokretanje Bash healthcheck skripte
./scripts/healthcheck.sh http://localhost:5000


Korak 7 — Zaustavljanje aplikacije
docker compose down



## 4. HTTP Endpoint-i

Aplikacija podržava tri HTTP GET endpoint-a:

/        Vraća JSON sa porukom Hello DevOps i hostname-om servera

/visits  Atomski povećava brojač poseta u Redis bazi

/health  Proverava Redis konekciju i vraća HTTP 200, ako je dobra, ili 503 ako je loša
Primeri poziva:

curl http://localhost:5000/
curl http://localhost:5000/visits
curl -i http://localhost:5000/health


## 5. Docker i trajno čuvanje podataka

Flask aplikacija koristi zvanični Python 3.13 slim Docker image i izvršava se kao korisnik bez root privilegija.

Redis persistence je realizovan kombinacijom:

- **Redis AOF (Append Only File)** — zapisuje operacije koje menjaju podatke na disk.
- **Docker named volume (`redis-data`)** — čuva Redis podatke nezavisno od životnog ciklusa kontejnera.

Zahvaljujući tome, brojač poseta ostaje sačuvan nakon zaustavljanja i ponovnog kreiranja kontejnera.

Za servise je definisana restart politika, dok Redis servis ima healthcheck koji proverava njegovu dostupnost.

## 6. Bash healthcheck skripta

Datoteka `scripts/healthcheck.sh` služi za automatsku proveru zdravlja aplikacije.

Pokretanje iz glavnog direktorijuma projekta:

```bash
./scripts/healthcheck.sh http://localhost:5000
```

Skripta:

- Prima osnovni URL aplikacije kao argument.
- Poziva `/health` endpoint najviše pet puta.
- Pravi pauzu od tri sekunde između neuspešnih pokušaja.
- Ispisuje vreme, redni broj pokušaja i HTTP status.
- Vraća izlazni kod `0` kada dobije HTTP 200.
- Vraća izlazni kod `1` ako nijedan pokušaj nije uspešan ili argument nije prosleđen.

## 7. Lokalno testiranje

Za lokalno testiranje potrebno je instalirati Python biblioteke:

```bash
python -m pip install -r requirements.txt
python -m pip install pytest ruff
```

Pokretanje testova:

```bash
python -m pytest tests/test.py -v
```

Implementirana su dva automatska testa:

1. Provera da početni endpoint `/` vraća HTTP 200.
2. Provera da `/health` vraća HTTP 200 i odgovarajući JSON kada je Redis dostupan, uz korišćenje mock objekta.

Provera kvaliteta Python koda pomoću Ruff-a:

```bash
ruff check .
```

## 8. CI — GitHub Actions

CI workflow je definisan u:

```text
.github/workflows/ci.yml
```

Automatski se pokreće prilikom:

- Push-a na `main` granu.
- Otvaranja ili ažuriranja Pull Request-a prema `main` grani.

Workflow redom:

1. Preuzima izvorni kod.
2. Podešava Python 3.13.
3. Instalira potrebne biblioteke.
4. Pokreće Ruff linter.
5. Pokreće pytest testove.
6. Gradi Docker image.

Ako bilo koji korak ne uspe, CI pipeline se označava kao neuspešan.

Status pipeline-a prikazan je na početku README dokumentacije.

