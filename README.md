# EIG Cohesion

*Le plus on se parle, le plus on se connait*

# Installation

## Requirements

Pour pouvoir travailler sur ce projet :
- python3.8
- docker / docker-compose
- virtualenv (pour le dev en local) / mkvurtalenv
- make (pour les commandes classiques)

## Installation

Cloner le projet :

    git clone https://github.com/antoan2/eig-cohesion.git
    cd eig-cohesion

Création de l'environnement virtuel :

    mkvirtualenv -a . --python=3.8 eig-cohesion
    add2virtualenv eig-cohesion/src

Copier le template de la configuration :

    cp env.template .env

Remplacer les différentes variables :
- PORT_API_DEV : le port d'exposition de l'api en mode dev
- PORT_API_PROD : le port d'exposition de l'api en mode prod

Vous pouvez maintenant lancer les commandes suivantes :

    # Build des différents services
    make build
    # Insertion de fausses données (WIP)
    docker-compose exec eig-cohesion python tool.py
    # Up l'application en mode developpement
    make up-dev