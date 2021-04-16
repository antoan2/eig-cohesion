EIG Cohésionneur<a name="TOP"></a>
===================
*Le plus on se parle, le plus on se connait*

- - - - 
# Installation

## Requirements

Pour pouvoir travailler sur ce projet :
- python3.8
- docker / docker-compose
- virtualenv (pour le dev en local) / mkvurtalenv
- make (pour les commandes classiques)

## Installation

Cloner le projet :

    git clone https://github.com/antoan2/eig-cohesionneur.git
    cd eig-cohesionneur

Création de l'environnement virtuel :

    mkvirtualenv -a . --python=3.8 eig-cohesionneur
    add2virtualenv eig-cohesionneur/src

Instalation des requirements:

    workon eig-cohesionneur
    pip install -r eig-cohesionneur/src/requirements.txt

Copier le template de la configuration :

    cp env.template .env

Remplacer les différentes variables :
- PORT_API_DEV : le port d'exposition de l'api en mode dev
- PORT_API_PROD : le port d'exposition de l'api en mode prod

Vous pouvez maintenant lancer les commandes suivantes :

    # Build des différents services
    make build
    # Lancer les tests
    make test
    # Insertion de fausses données (WIP)
    docker-compose exec eig-cohesion python tool.py
    # Up l'application en mode developpement
    make up-dev

## CLI

Un petit cli permet de créer de nouvelle semaines :

    # Création d'une nouvelle semaine
    python cli.py new-week -s 2021-01-01
    # Création de la semaine suivante (rajoute les 1:1 fait dans l'historique)
    python cli.py next-week
    # Supprime tout
    python cli.py flush-all