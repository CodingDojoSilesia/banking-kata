# Bank PKO, Profesjonalnie Kradniemy Oszczędności

## TDD

### mam pipenv

    pipenv install  # tworzenie środowiska
    pipenv run test  # uruchomienie testów

### nie mam pipenv

    python3 -m venv env  # tworzenie środowiska
    source env/bin/activate  # aktywacja środowiska
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

## Jak i z co bank pobiera prowizję

### za przelewy

Kazdy przelew w banku obarczony jest kosztem. Koszt pobierany jest od wysyłającego przelew.

Przykład:
Jeśli ja przelewam do Bartka 100zł to z mojego konta oprócz kwoty 100 zostanie pobrana prowizja.

### za przechowywanie gotówki

Cyklicznie co 200 operacji w banku (kazda czynnośc którą wykonuje bank to operacja) pobierana jest prowizja
od przetrzymywanej gotówki. Prowizja pobierana jest od wszystkich kont.

Przykład:
Ja, Batek i Noemi mamy konta po 100zł. Po 200 operacjach bankowych z naszych kont zostanie pobrana prowizja
za przetrzymywanie gotówki.
