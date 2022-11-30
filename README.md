![Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Python_logo_and_wordmark.svg/2560px-Python_logo_and_wordmark.svg.png)

**Python-rootkit** est un projet issu d'un cours d'1 jour. Il s'agit d'un rootkit en cours de développement permettant de l'exécution de code à distance (**RCE: Remote Code Execution**)

> **Il s'agit d'un programme à portée éducative uniquement et ne doit être utilisé que comme tel sur du matériel appartenant à l'utilisateur.**

# Description du projet
### Fonctionnement
- Ouverture d'un socket TCP entre la victime (client) et l'attaquant (seveur)
- *Switch-case* permettant à l'attaquant de choisir parmis une sélection de choix (ouverture d'un shell, transfert de fichier,...)
- Exécution "transparente" côté victime: pas d'impression en console des commandes saisies par l'attaquant


### Description des fichiers
```attaquant.py``` contient le code "serveur" ouvrant un socket TCP pour communiquer avec le code déployé côté victime

```victime.py``` contient le code "client" à déployer sur la machine victime communiquant avec le serveur

### Etat d'avancement du projet

- [x] Ouverture d'un socket TCP
- [x] Création d'un menu type *prompt*
- [x] Conversion du menu en switch-case 
- [ ] Création d'un menu interactif côté attaquant
- [ ] Compatibilité Windows pour l'exécution de code (encodage défaillant)
- [ ] Transfert de fichiers

### Dépendances du projet
Ce programme ne repose que sur des bibliothèques Python de base.

### Mise en réseau
Sur la machine exécutant le code attaquant, il est nécessaire de s'assurer que le flux TCP puisse passer. Il convient de: 

1) Créer une **règle de pare-feu** en conséquences côté **serveur**
2) En cas de NAT: **rediriger le port** spécifié dans ```victime.py``` vers celui spécifié dans ```attaquant.py```

# Utilisation
## Prérequis
### Préparation de l'environnement de travail
Il est fortement recommandé d'exécuter ce programme dans une machine virtuelle.

- Création d'un environnement virtuel: ```python -m venv env```

- Activation de cet environnement virtuel: ```./env/Scripts/activate```

## Modification des variables

Plusieurs variables sont à modifier:
- Côté client (victime):
  -  Adresse IP du serveur
  -  Port du serveur
- Côté serveur:
   - Port à utiliser
   - Adresse IP sur laquelle écouter le flux

## Exécution

Le programme s'exécute en saisissant ```python attaquant.py``` côté serveur et ```python victime.py``` côté client.

Si l'exécution fonctionne, le prompt côté serveur devient ```FB >>``` et attend que l'on spécifie une fonction.

### Fonctions

- ```shell``` : permet d'ouvrir un shell distant
- ```help``` : affiche un prompt d'aide
- ```exit``` : permet de quitter le programme
- ```recv_file``` (à venir) : permet de télécharger un fichier distant

# Crédits
## Auteur

Par François B, étudiant à l'école IPSSI en première année de master Cybersécurité & cloud-computing

Merci à Christian A, enseignants chercheurs

## Licence

Ce programme a été créé dans un but purement éducatif et n'est soumis en tant que tel à aucune licence.
Les licences des bibliothèques et interprêteurs utilisés s'appliquent.


