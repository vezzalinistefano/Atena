# Athena course shop

Progetto per il corso di Tecnologie Web svolto per il terzo anno presso
l'UniMoRe a cura di Stefano Vezzalini.

## Come installare

Per l'installazione è necessario avere `pipenv` installato sul proprio sistema. Per installare pipenv
è sufficente lanciare il seguente comando:

```shell
pip install --user pipenv
```

A questo punto basta entrare nella cartella del progetto (quella dove è presente il file `Pipfile`)
e lanciare il comando

```shell
pipenv install
```

che provvederà a installare tutte le dipendenze necessarie per avviare l'applicazione.
Ora è possibile avviare l'applicazione tramite il comando 

```shell
python manage.py runserver
```

## Utenti

Sul sistema sono già presenti diversi utenti visualizzabili nel pannello admin, nel caso si volesse usarli la password per tutti è `tecweb123`