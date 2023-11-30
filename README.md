# CurrencyExchange-Backend
Aplikacja w frameworku Django - pobiera wybrane kursy i udostępnia endpoint z danymi. Cashowanie widoku na 60sek oraz odpytywanie API co 60 sekund. Wykorzystano Redis do wykonywania tasków.

**Pobranie kodu źródłowego**

git clone https://github.com/KennyDaktyl/CurrencyExchange-Backend.git

**Uruchomienie przez docker-compose:**
 - docker-compose up --build
 - docker-compose down (aby usunąć kontenery)

**Utworzenie superuzytkownika dla korzystania z django-admin**
 - docker exec -it currencyexchange-web-1 bash
 - python manage.py createsuperuser

**testy**
 - docker exec -it currencyexchange-web-1 bash
 - python manage.py test

**Uruchomienie lokalnie:**
  - utworzyć baze danych w postgres
    - psql -U postgres -h localhost
    - create database NAZWA BAZY;
    - q\
- virtualenv -p python3 env  (utworzenie środowiska python)
- source env/bin/activate
- cd env
- touch export.txt (Tworzymy zmienne środowiskowe)

**Wymagane pola:**
    - export SECRET_KEY="Jakis secret key wygenerowany dla django"\n
    - export POSTGRES_DB= NAZWA BAZY UTWORZONEJ W PSQL\n
    - export DB_USER= NAZWA URZYTKOWNIKA W PSQL\n
    - export DB_PASSWORD= HASŁO DO PSQL\n
    - export DB_HOST="127.0.0.1"\n
    - export REDIS_URL="redis://127.0.0.1:6379/"\n

    - cd ..
    - source /env/export.txt
    - python manage.py migrate
    - python manage.py runserver

**testy**
 - python manage.py test


**Uruchamiamy koniecznie beat i worker do wykonywania cyklicznych zapytań o kursy walut**

**Otwieramy terminal i przechodzimy do katalogu z projektem**
- source env/bin/activate
- source env/export.txt
- celery -A CurrencyExchange worker -l info --loglevel=info

**Otwieramy kolejny terminal i przechodzimy do katalogu z projektem**
- source env/bin/activate
- source env/export.txt
- celery -A CurrencyExchange beat -l info
