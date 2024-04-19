# GraphDB

## Comandi utili

``` bash
docker run -e ARANGO_RANDOM_ROOT_PASSWORD=1 -e ARANGO_NO_AUTH=1 -p 8529:8529 -d arangodb
```

``` bash
pip install pyarango
```

## Struttura del progetto

**Nodi**:

- Utente
- Categoria del film
- Film
- Università
- Città

**Relazioni**:

- Utente-Film: il film preferito dell'utente
- Utente-Università: l'università che frequenta o ha frequentato
- Film-Categoria del film: la categoria del film
- Utente-Città: la città in cui vive l'utente
