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

```bash
docker run -e ARANGO_RANDOM_ROOT_PASSWORD=1 -e ARANGO_NO_AUTH=1 -p 8529:8529 -d arangodb
```

### Versione distribuita

```bash
docker compose up
```

### Comandi python 

```bash
```bash
pip install pyarango
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

## Esempio di query

Vogliamo ottenere tutte le città che si trovano in Australia.

```AQL
FOR city IN 1..1 OUTBOUND "Country/AU" LocatedIn RETURN city
```

```AQL
FOR v, e, p IN 1..1 OUTBOUND "User/123" GRAPH SoulSyncGraph RETURN { "edge": e, "destination": v }
FOR user IN 1..1 ANY "User/123" Matches RETURN user
FOR user IN Matches FILTER  user._from == "User/123" OR user._to == "User/123" RETURN user
FOR u IN User FILTER u._key == "123" RETURN u
```

### Query usate per testare il progetto

Trovare tutti gli utenti che hanno un film preferito in comune con l'utente `@user`.

```AQL
FOR v, e IN 1..1 OUTBOUND @user IntMovieCategory
  FOR v1, e1 IN 1..1 INBOUND v IntMovieCategory
    FILTER v1 != v
RETURN v1
```

Trovare tutti gli utenti che hanno frequentato la stessa università dell'utente
`@user`.

```AQL
FOR v, e IN 1..1 OUTBOUND @user StudiesAt
  FOR v1, e1 IN 1..1 INBOUND v StudiesAt
    FILTER v1 != v
  RETURN v1
```

Trovare tutti gli utenti che vivono nella stessa città dell'utente `@user`.

```AQL
FOR v, e IN 1..1 OUTBOUND @user LivesIn 
  FOR v1, e1 IN 1..1 INBOUND v LivesIn
    FILTER v1 != v
  RETURN v1
```

Trovare tutti gli utenti che hanno un film preferito in comune con l'utente `@user`
 e che hanno frequentato la stessa università.
  
  ```AQL
  FOR v, e IN 1..1 OUTBOUND @user IntMovieCategory
    FOR v1, e1 IN 1..1 INBOUND v IntMovieCategory
      FILTER v1 != v
    FOR v2, e2 IN 1..1 OUTBOUND @user StudiesAt
      FOR v3, e3 IN 1..1 INBOUND v2 StudiesAt
        FILTER v3 != v2
      FILTER v3 == v1
    RETURN v3
  ```

Trovare tutte le persone che hanno messo like all'utente `@user`.

```AQL
FOR v, e IN 1..1 INBOUND @user Likes
RETURN v
```

Trovare tutti i like degli utenti che hanno fatto match con l'utente `@user`.

Trovare tutti gli utenti che hanno messo like all'utente `@user` e che hanno fatto match.

Trovare tutti gli utenti che vivono nella stessa nazione.

Trovare il numero di utenti per ogni città.
