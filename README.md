# GraphDB

## Descrizione

In questa repository è presente un progetto di GraphDB realizzato con ArangoDB e
PyArango.

Lo scopo di questo progetto è quello di analizzare il funzionamento di un database
a grafo nell'ambito di un sistema stile Tinder.

I dati utilizzati per il progetto sono stati generati casualmente attraverso il
sito [Mockaroo](https://www.mockaroo.com/).

## Comandi utili

``` bash
docker run -e ARANGO_RANDOM_ROOT_PASSWORD=1 -e ARANGO_NO_AUTH=1 -p 8529:8529 -d arangodb
```

``` bash
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
- Film-Categoria del film: la categoria del film
- Utente-Città: la città in cui vive l'utente
