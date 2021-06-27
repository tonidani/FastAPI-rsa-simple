# FastAPI-simple-rsa - zadanie rekr.
## _Antonio Rodriguez_


### Cechy ogólne i opis

Kwałek kodu widniejący na tym repozytorium jest zrobiony na potrzebę zadania rekrutacyjneg i nie powinno się stosować niniejszego rozwiązania w środowisku podrukcyjnym - implementacja poszczególnych metod oraz rozwiązania tutaj zawarte mają sprawdzać wiedzę programistyczną i umiejętność radzenia sobie z problemami, sama logika jest dość "prymitywna".

Jak prypadkowo tutaj trafiłeś, to już wiesz że to tylko 4hobby :)


#### Szyfr zastosowany

Program korzysta z prostej implementacji szyfru **RSA** - powszechnie znanego i stosowanego w celu generowania pary kluczy asymetrzycznych na różnych środowiskach. Najbardziej kojarzony może być z protokołem ssh, gdzie bardzo często aby nie korzystać z logowania za pomocą swoich danych na stacjach roboczych opartych o kernele Unix'owe, stacje wymieniają się parą kluczy, które służą do uwierzytelniania danego użytkownika.


### Podział projektu

* **app** - tutaj jest cała aplikacja;
    * **/utils**  - w tym folderze znajdują się potrzebne klasy i elementy aby móc wykonać odpowiednio obliczenia dla algorytmu RSA
    * **/utils/rsa.py**  - plik z klasą Rsa()
    * **/utils/number_utils.py** - plik wspomagający operacje matematyczne dla klasy Rsa(), jest w osobnym pliku, gdyż można by było wykorzystać implementacje tych metod na innecych obiektach - dlatego składa się ze statycznych metod.
    * **/tests** - folder zawierający testy do klas znajdujących się w **/utils/**
    * **main.py** - plik z całą aplikacją FastAPI
    * **schemas.py** - plik ze schematem do wysyłania requestów
    * **config.py** - konfiguracja aplikacji, a bardziej konfiguracja użytkownika i hasła do BasicHTTPAuth
    * **test_main.py** - test FastAPI.Client dla endpointów

## Końcówki - Endpoints
## GET
* **/**  - Jeżeli jesteś uwierzytelniony wyświetla się pole w formularzu do wpisaniu swojej wiadomości - przeglądarkowa wersja
 * **/api/encode/**  - Jeżeli jesteś uwierzytelniony, odpowiada:
    * 'Send your text in this format {"message" : "textoencrypt"} '
 * **/api/decode/**  - Jeżeli jesteś uwierzytelniony, odpowiada:
    * 'Send your text and public_key in this format {"message" : "textoencrypt", "private_key" : { "key": int, ' \
           '"n": int} } '



## POST
*  **/**  - Jeżeli jesteś uwierzytelniony wyświetla się pole w formularzu do wpisania swojej wiadomości, służy tylko do zaszyfrowania i zwrócenia klucza publicznego w celu odszyfrowania wiadomości za pomocą innych końcówek, zwraca dane w postaci:
    *    "message: {} | encrypted: {} | username: {} | pub_key {}".format(message, encrypted, username, rsa.public_key)
 * **/api/encode/**  - Jeżeli jesteś uwierzytelniony, słuzy do szyfrowania wiadomości, należy wysłać wiadomość w postaci:
    * **{"message" : "textoencrypt"}**  - nie potrzeba więcej pól
    * Odpowiedź wygląda następująco:
    * > {"username": "admin",  "message": "ḟằᚴḟằᚴḟ","public_key": { "key": 5, "n": 8051},"private_key": { "key": 3149,"n" :"8051}}
 * **/api/decode/**  - Jeżeli jesteś uwierzytelniony, słuzy do odszyfrowania wiadomości, należy wysłać zaszyfrowaną wiadomość oraz klucz publiczny w postaci:
    * **{"message" : "encrypted", ,"public_key": { "key": int, "n": int }**  - nie potrzeba więcej pól
    * Odpowiedź wygląda następująco:
    * > {"username": "admin",  "message": "textoencrypt","public_key": { "key": 5, "n": 8051},"private_key": { "key": 3149,"n" :"8051}}

## Auth
DANE:
> * config.py
>USER ="admin"
>USER_PASSW ="admin"

Przed dostaniem się do każdego endpointa należy z powodzeniem wcześniej przejśc BasicAuth (zwykłe uwierzytelnianie WWW - najprymitywniejsze :P). Użytkownik i hasło powinny być w formacie 
> "username:password" zakodowane do base64

Ja do testów używałem pary ***"toni:123"*** ale można sobie ustawić użytkownika jakiego się chce w pliku config.py pod zmienną **USER** i hasło w **USER_PASSW**

Przykładowe zapytanie z powodzeniem w curl-u:

```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/encode/' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic dG9uaToxMjM=' \
  -H 'Content-Type: application/json' \
  -d '{
  "message": "ffdsffs"
}'
```

Odpowiedź

```
{
  "username": "toni",
  "message": "ӋӋɿݰӋӋݰ",
  "public_key": {
    "key": 7,
    "n": 2077
  },
  "private_key": {
    "key": 283,
    "n": 2077
  }
}
```

## Wymagania

> pip -r install requirements.txt

# Działanie szyfru
Założenia:

Generowanie klucza publicznego:
> * Wybieramy 2 liczby pierwsze **p** i **q**
> * Liczymy pierwszą cześć klucza publicznego **n = p * q**
> * liczymy ***phi = (p-1)(q-1)***
> * Ustalamy mały wykładnik **e** taki że:
>   * **jest liczbą całkowina i nie jest czynnikiem n**
>   * **1 < e < phi**

> * **klucz publiczny** =  {n , e}

Generowanie klucza prywatnego:
>   * **d = (k* phi + 1) / e* dla wybranej liczby całkowitej k 

W przypadku algorytmu ja zostosowalem pętle while gdzie d zaczyna się od -1 i za każdą zakonczoną iterację dodaje sie k + 1, tak aby wiedzieć jaka liczba jest odpowiednim odwróceniem 
> * *d = (k* phi - 1) / e** dla wybranej liczby całkowitej k w odwrotny sposób, aby znależć odpowiednie d.
```
private_key: dict = {"key": 0, "n": n}
while x != 0:
            private_key["key"] += 1
            x = (public_key["key"] * private_key["key"] - 1 ) % phi
```
> * **klucz prywatny** =  {d, e}


Działanie szyfru można zaleźć [RSA Algorithm in Cryptography](https://www.geeksforgeeks.org/rsa-algorithm-cryptography/) i nie ma sensu tłumaczyć to samo co jest na tej stronie, zaś warto o czymś wspomnieć. Implemtacja którą zastosowalem opierda się na zamianie znaków na kody unicode za pomocą chr(<str>) i wrzucenia odpowiedniej wartości wczesniej obliczonej za pomocą wzrou algebraicznego, całe działanie algorytmu jest opisane w pliku rsa.py oraz number_utils.py. Kod sam w sobie ma zrobione komentarze pod methodami, tak aby wiedzieć co się dzieje w danym momemcie.

## Szyfrowanie znaków

```
''' Here uses algebra for encrypt the message with the int representation of characters in ascii table '''
    # c = (letters to int) ^ e % n

    def encrypt_RSA(self, message: str, public_key: int) -> str:

        message = [ord(i) for i in message]
        encryptedMessage = ''.join([chr(i ** public_key["key"] % public_key["n"]) for i in message])

        return encryptedMessage

    ''' Same as above, but in reverse '''
    # c ^ e % n

    def decrypt_RSA(self, encryptedMessage: str, private_key: int) -> str:

        encryptedMessage = [ord(i) for i in encryptedMessage]
        decryptedMessage =''.join([chr(i ** private_key["key"] % private_key["n"] ) for i in encryptedMessage])

        return decryptedMessage
```

Biorąc pod uwagę, że algorytm szyfruje za pomocą Uicode to możemy mu ustawić limit, który ma osiągać, generalnie w tej implementacji to p * q ( czyli N) ustatala ile znaków będzie brał do szyfrowania:
Wczesniej ustawiłem limit na 255 aby pokryć całą tablicę ASCII, ale po kilku testach zdałem sobie sprawę, że często pojawiały się kwadraciki z niewidocznymi znakami, wiec podwyższyłem limit do 1000. 


```
 '''For encrypt and decrypt with the values of the ASCII table its necessary to have a range 
    of all of the Unicode codes, in this case algorithm uses 255 chars limit '''

    '''If you need more Unicode characters, you can change the value above, not every browser has too many codes
       P * q < `value`  '''

    @staticmethod
    def check_all_ascii_codes(p: int, q: int) -> bool:

        if p * q < 1000:
            return True
        return False

    '''As in the name function, Euclid algorithm for cheking if 2 numbers are not factor '''
```


# Białe znaki
Z bialymi znakami algorytm nie powieniem mieć problemów - funkcja w /**test_main.py**   --- **TestMain().test_encode_and_decode_withespaces** sprawdza białe znaki i przechodzi test z powodzeniem:
> test_message: dict = {"message": '\n \t \t \v \b \r \f \a \\ \' \" '}



##TL:DR
Jeżeli nie chce Ci się tego czytac, to openApi wszystko Ci powie! Do tego pliki mają komentarze w miejscach mniej zrozumiałych. Miłego korzystania :)

