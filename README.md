# winlinktodapnet
Checks emails on winlink and sends infos on dapnet
--------------

Semplice script che si collega a Winlink.org via telnet
e controlla le nuove emails.
Se ve ne è una nuova, ne invia l'intestazione via DAPNET.

Per renderlo automatico inserire l'esecuzione nel crontab
```
*/5 * * * * /opt/dapnet/winlinktodapnet/winlinktodapnet.py
```


