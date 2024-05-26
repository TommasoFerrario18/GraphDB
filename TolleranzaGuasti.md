# Start the database

All up
    - Time to create database:  0.019860267639160156

Coordinator 1 up and Coordinator 2 down
    - Time to create database:  0.015251636505126953

Coordinator 2 up and Coordinator 1 down
    - Time to create database:  22.292737245559692

Con 1 DB server up il database parte ma da errore quando si tenta di eseguire
qualunque tipo di operazione.

Non si può spegnere un DBServer in fase di inserimento dei dati, viene generata
un'eccezione.

Non si possono eseguire le query se si ha un solo DBServer attivo.
