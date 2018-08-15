# winlinktodapnet
Checks emails on winlink and sends infos on dapnet
--------------

Semplice script che si collega a Winlink.org via telnet
e controlla le nuove emails.
Se ve ne è una nuova, ne invia l'intestazione via DAPNET.

Per renderlo automatico inserire l'esecuzione nel crontab
```
*/15 * * * * /opt/dapnet/winlinktodapnet/winlinktodapnet.py
```

Si consiglia di non utilizzare un tempo inferiore ai 15 minuti
per evitare di ricevere più messaggi con la stessa intestazione email.
Winlink attende circa 10 minuti, dopo il comando **LM** prima di giudicare *OLD Message*
un messaggio già listato.
