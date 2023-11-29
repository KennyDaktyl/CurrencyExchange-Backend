**Pobranie kodu źródłowego**

git clone https://github.com/KennyDaktyl/CurrencyExchange-Backend.git

**Uruchomienie przez docker-compose:**
 - docker-compose up --build
 - docker-compose restart

**Utworzenie superuzytkownika dla korzystania z django-admin**
 - docker exec -it rekrutacja-web-1 bash
    w dockerze: python manage.py createsuperuser


**Uruchomienie lokalnie:**
    - utworzyć baze danych w postgres
        - psql -U postgres -h localhost
        - create database NAZWA BAZY;
        - q\
- virtualenv -p python3 env  (utworzenie środowiska python)
- source env/bin/activate
- cd env
- touch export.txt (Tworzymy zmienne środowiskowe)

    Wymagane pola:
        export SECRET_KEY="Jakis secret key wygenerowany dla django"
        export POSTGRES_DB= NAZWA BAZY UTWORZONEJ W PSQL
        export DB_USER= NAZWA URZYTKOWNIKA W PSQL
        export DB_PASSWORD= HASŁO DO PSQL
        export DB_HOST="127.0.0.1"
        export REDIS_URL="redis://127.0.0.1:6379/"

    - cd ..
    - source /env/export.txt
    - python manage.py migrate
    - python manage.py runserver


**Otwieramy terminal i przechodzimy do katalogu z projektem**
- source env/bin/activate
- source env/export.txt
- celery -A CurrencyExchange worker -l info --loglevel=info

**Otwieramy kolejny terminal i przechodzimy do katalogu z projektem**
- source env/bin/activate
- source env/export.txt
- celery -A CurrencyExchange beat -l info