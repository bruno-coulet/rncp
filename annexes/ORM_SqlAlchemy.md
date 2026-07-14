# SQLAlchemy

Principalement connu et utilisé comme un ORM (Object-Relational Mapper) pour Python.

[SQLAlchemy](https://www.sqlalchemy.org/) est conçu pour faciliter la communication entre le code Python et une base de données relationnelle (comme PostgreSQL, MySQL, SQLite, etc.).

Dans son architecture, SQLAlchemy se divise en réalité en deux couches distinctes qui peuvent être utilisées séparément ou ensemble :

- **L'ORM (Object-Relational Mapper)**

    C'est la couche de haut niveau. Elle permet de "mapper" (lier) des tables de bases de données à des classes Python.<br>
    Donc d'interagir avec la base de données en manipulant directement des objets Python, sans avoir à écrire la moindre requête SQL brute.

- **Le Core (SQL Expression Language)**

    C'est la couche de bas niveau sur laquelle repose l'ORM. Elle permet de construire et d'exécuter des requêtes SQL de manière programmatique via des fonctions Python.<br>
    Elle est très utile lorsque pour 'optimiser des requêtes complexes ou faire des opérations massives en base de données où l'ORM serait trop lent.
