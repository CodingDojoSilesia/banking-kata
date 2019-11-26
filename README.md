# Bank PKO, Profesjonalnie Kradniemy Oszczędności

## TDD

### mam pipenv

    pipenv install  # tworzenie środowiska
    pipenv run test  # uruchomienie testów

### nie mam pipenv

    python3 -m venv env  # tworzenie środowiska
    source env/bin/acivate  # aktywacja środowiska
    pip install -r requirements.txt  # instalacja pakietów
    pytest  # uruchomienie testów

## Bank

- Ma konta
- Ma chronologiczny rejestr wszystkich transakcji
- Ma swoją gotówkę z prowizji
- Stan gotówki z prowizji oraz rejestr jest dostępny
- Rejestr transakcji pozwala odtworzyć stan banku oraz wszystkich kont
- Pozwala otwierać konta
- Pozwala dokonywać transakcji poza bank oraz wewnątrz banku
- Powinna być możliwość podania oprocentowania dziennego (naliczane po każdym dniu) jak i tego przy transakcji w postaci floata (np 0.00001).
- Pobiera opłaty od przetrzymywanej gotówki na koniec dnia (0.0002%, lub coś)
- Dzień to 200 operacji

## Konto

- Ma obecny stan
- Ma indywidualny rejestr transakcji
- Pozwala na wpłaty
- Pozwala na wypłaty
- Gotówka nie może spaść poniżej zera

## Transakcja

- Uznanie konta
- Obciążenie konta
- Transfer między kontami wewnątrz banku
- Prowizja jest pobierana podczas transakcji
- Kwota obciążenia i prowizja nie mogę być większe niż stan konta