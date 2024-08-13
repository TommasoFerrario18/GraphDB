# GraphDB

## Descrizione

In questa repository è presente un progetto di GraphDB realizzato con ArangoDB e
PyArango.

Lo scopo di questo progetto è quello di analizzare il funzionamento di un database
a grafo nell'ambito di un sistema stile Tinder.

I dati utilizzati per il progetto sono stati generati casualmente attraverso il
sito [Mockaroo](https://www.mockaroo.com/).

## Comandi utili

### Versione centralizzata

Per la versione centralizzata è possibile utilizzare il seguente comando per
avviare il container di ArangoDB. Una volota avviato il container sarà possibile
accedere alla web interface di ArangoDB all'indirizzo `http://localhost:8529/`.

```bash
docker run -e ARANGO_RANDOM_ROOT_PASSWORD=1 -e ARANGO_NO_AUTH=1 -p 8529:8529 -d arangodb
```

### Versione distribuita

Per la versione distribuita abbiamo deciso di utilizzare docker compose per
semplificare il processo di creazione e gestione del cluster. Una volta avviato
il cluster sarà possibile accedere alla web interface di ArangoDB all'indirizzo
`http://localhost:8000/` e `http://localhost:8001/`.

```bash
docker compose up -d
```

**N.B.** Nella user interface di ArangoDB è necessario selezionare attraverso il menù
a tendina posizionato nell'angolo in alto a destra il database che si vuole
visualizzare.

### Comandi python

Per eseguire il codice python è necessario installare la libreria `python-arango`.

```bash
pip install requirements.txt
```

Mentre per ripetere gli esperimenti realizzati con ArangoDB è necessario eseguire
il codice python contenuto nella cartella `code`. In particolare, nel file `main.py`
è presente tutta la pipeline necessaria per la creazione del database, l'inserimento
dei dati e l'esecuzione delle query. In base alla versione del database che si vuole
utilizzare (centralizzata o distribuita) è necessario modificare il valore della
variabile `typeDB` presente nel file `main.py`.

- `typeDB` = 0: versione centralizzata
- `typeDB` = 1: versione distribuita

```bash
python ./code/main.py
```

### Partizionamento della rete

Per il partizionamento della rete si è scelto di utilizzare spostare in un'altra
rete docker alcuni nodi del cluster. Questo è stato realizzato utilizzando il
comando `docker network connect` e `docker network disconnect`.

Per prima cosa si è creata una nuova rete docker con il comando:

```bash
docker network isolated_network
```

Una volta fatto ciò si è proceduto alla simulazione di un partizionamento della
rete sfruttando i seguenti comandi:

```bash
docker network disconnect progettographdb_default progettographdb-db1-1
docker network connect isolated_network progettographdb-db1-1
```

## Struttura del database

**Nodi**:

- User
  - first_name
  - last_name
  - email
  - phone
  - birthday
  - gender
  - Latitude
  - Longitude
- Movie
  - title
- MovieCategory
  - Name
- City
  - Name
- Country
  - Name
  - Code
  - Continent
- University
  - Name
- Color
  - Name

**Relazioni**:

- Utente-Film: il film preferito dell'utente
- Utente-Università: l'università che frequenta o ha frequentato
- Utente-Città: la città in cui vive l'utente

### Query usate per testare il progetto

Ottenere tutte le informazioni sull'utente `@user`.

```AQL
  WITH User 
  FOR u IN User 
    FILTER u._id == @user 
  RETURN u
```

Trovare tutte le persone che hanno messo like all'utente `@user`.

```AQL
WITH User
FOR user, edge IN 1..1 INBOUND @user Likes
RETURN user
```

Trovare tutti gli utenti che hanno la categoria di film preferita in comune con
l'utente `@user`.

```AQL
  WITH User, MovieCategory
  FOR category, e IN 1..1 OUTBOUND @user IntMovieCategory
    FOR user, edge IN 1..1 INBOUND category IntMovieCategory
      FILTER user != @user
  RETURN category
```

Trovare tutti gli utenti che vivono nella stessa città dell'utente `@user`.

```AQL
  WITH User, City
  FOR city, e IN 1..1 OUTBOUND @user LivesIn 
    FOR user, edge IN 1..1 INBOUND city LivesIn
      FILTER user != @user
  RETURN user
```

Trovare tutti gli utenti che hanno la categoria di film preferita in comune con
l'utente `@user` e che hanno frequentato la stessa università.
  
  ```AQL
  WITH User, MovieCategory, University
  FOR category, e IN 1..1 OUTBOUND @user IntMovieCategory
    FOR user1, e1 IN 1..1 INBOUND category IntMovieCategory
      FILTER user1 != @user
    FOR colleague, e2 IN 1..1 OUTBOUND @user StudiesAt
      FOR user2, e3 IN 1..1 INBOUND colleague StudiesAt
        FILTER user2 != @user
    FILTER user1 == user2
  RETURN user1
  ```

Trovare tutti i like degli utenti che hanno fatto match con l'utente `@user`.

```AQL
  WITH User
  FOR v, e IN 1..1 ANY @user Matches
    FOR v1, e1 IN 1..1 OUTBOUND v Likes
  RETURN v1
```

Trovare tutti gli utenti che vivono nella nazione `@country`.
  
  ```AQL
  WITH Country, City, User
  FOR city, edge IN 1..1 ANY  @country LocatedIn 
    FOR user, edge1 IN 1..1 ANY city LivesIn
  RETURN {"User": user._id, "City": city.name}
```

Trovare il numero di utenti per ogni città.

```AQL
  FOR city IN City
    LET usersCount = LENGTH(
      FOR v, e, p IN 1..1 INBOUND city LivesIn
      RETURN v
    )
  RETURN { city: city.name, numberOfUsers: usersCount }
```
