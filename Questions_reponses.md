

###  Question 1 : Architecture MLOps et "Lazy Loading" (Blocs E3 / E4)
« Bonjour. Sur Drink Safe, vous parlez de "Lazy Loading" pour charger vos modèles d'IA en RAM à la volée lors de la première requête d'inférence, ce qui vous permet d'atteindre le "Zero Downtime". Mais en faisant cela, vous imposez un temps d'attente potentiellement énorme (le fameux Cold Start) au tout premier agent de terrain qui va faire une analyse, le temps que le lourd fichier .pkl soit téléchargé. Est-ce vraiment une bonne pratique d'expérience utilisateur ? Et que se passe-t-il pour cet agent si votre serveur MLflow est en panne exactement au moment de cette première requête ?

> *"Le Cold Start de quelques millisecondes pour le tout premier utilisateur est un compromis assumé pour garantir la stabilité au démarrage. Surtout, notre architecture est résiliente : les modèles téléchargés sont stockés physiquement dans un volume Docker partagé (`./mlruns_artifacts`). Si le serveur MLflow tombe en panne au moment de l'inférence, mon API ne crashe pas : elle va utiliser le dernier modèle qu'elle a déjà placé dans son cache en mémoire vive (RAM). C'est ce qui nous garantit un véritable Zero Downtime, même en cas de perte partielle de l'infrastructure."*

***

###  Question 2 : Cybersécurité et DNS Rebinding (Bloc E5)
« Dans votre rapport d'incidents, vous expliquez avoir résolu une erreur 403 (liée à la protection contre le DNS Rebinding de MLflow) en falsifiant l'en-tête Host de vos requêtes HTTP internes à la volée avec un "patch d'interception". En tant qu'architecte Sécurité, je trouve que bidouiller des en-têtes HTTP ressemble fortement à un "hack". Pourquoi avoir fait cela dans le code de votre API plutôt que de simplement configurer les hôtes autorisés (CORS / Allowed Hosts) proprement sur le serveur MLflow ? »

**Commentaire :** En production dans un cluster Docker ou Kubernetes, les conteneurs continuent d'utiliser des noms de domaine internes (comme `mlflow:5000`). Il ne faut donc pas retirer le patch.

> *"Ce n'est pas un 'hack', c'est un choix d'architecture assumé. Dans un réseau Docker isolé, modifier la configuration de sécurité native du serveur MLflow pour ouvrir ses CORS et ses Allowed Hosts à tout le réseau affaiblirait sa sécurité globale. J'ai préféré patcher la requête sortante au niveau de mon API FastAPI. Le spoofing d'en-tête en interne me permet de faire communiquer mes micro-services de manière fluide, tout en préservant la forteresse de sécurité native du serveur MLflow."*

***

###  Question 3 : Data Engineering et Big Data (Bloc E1)
« Pour l'Observatoire de la Mobilité, vous justifiez l'utilisation du moteur DuckDB par sa capacité à faire du Predicate Pushdown sur des fichiers Parquet, évitant ainsi de saturer la RAM. Or, vous savez sûrement que la librairie Pandas (couplée au moteur PyArrow) permet déjà de lire des fichiers Parquet en filtrant directement les colonnes à la source via les paramètres de pd.read_parquet(). Pourquoi avoir ajouté la complexité d'un nouveau moteur SQL comme DuckDB à votre stack technologique, alors que Pandas pouvait techniquement faire la même chose ? »

**Mon commentaire :** technique de gestion de la mémoire (RAM vs Disque).

> *"Il est vrai que le référentiel demande d'explorer les technologies Big Data, mais le choix de DuckDB est techniquement justifié. Pandas charge l'intégralité du DataFrame en mémoire vive (RAM). Si mon fichier d'historique de trottinettes atteint 15 Go, mon serveur va crasher avec une erreur 'Out Of Memory'. Avec DuckDB, j'exécute des requêtes analytiques en SQL directement sur le disque. Grâce au 'Predicate Pushdown', la requête filtre les données avant même de les charger en RAM, ce qui est infiniment plus scalable et éco-responsable."*

***







---
----
---

###  **Question 4 :**
en examinant vos rapports et vos captures d'écran de couverture de code (pytest-cov), nous constatons que votre route critique ocr.py est testée à 70%
, ce qui est bien. Cependant, des fichiers fondamentaux pour le Machine Learning comme experiment.py, init_mlflow.py ou models.py affichent une couverture de test de 0%
. Pouvez-vous justifier ce choix d'ingénierie devant nous ? Comment garantissez-vous que votre modèle reste fiable en production si les scripts d'entraînement ne sont pas couverts par vos tests unitaires ?


>Si ces scripts affichent une couverture de 0%, ce n'est pas un oubli, c'est un choix architectural délibéré lié au découplage de nos conteneurs.
Ma suite de tests PyTest s'exécute à l'intérieur du conteneur de production de l'API. Son rôle est de valider le code qui expose le modèle. Or, les fichiers comme experiment.py ou init_mlflow.py constituent mon pipeline d'entraînement. Ils s'exécutent dans un conteneur éphémère totalement isolé (mlops-training)
. L'API n'a pas à connaître le code d'entraînement, ce qui garantit la sécurité et la légèreté de l'infrastructure de production
.
Pour garantir la fiabilité du modèle en production, je n'utilise pas des tests unitaires classiques, mais une véritable stratégie MLOps basée sur 3 niveaux de tests
 :
Les tests unitaires et fonctionnels : Ils vérifient le bon fonctionnement du conteneur API et le cycle de vie complet de bout en bout (comme l'ingestion OCR, l'écriture en base de données et l'authentification)
.
Le monitoring continu : Le modèle est mesuré en permanence sur MLflow. L'analyste Qualité dispose d'un tableau de bord pour traquer d'éventuelles dérives (Data Drift) sur les nouvelles données
.
Les tests de non-régression : C'est le véritable garde-fou de mon modèle. Mon script test_non_regression.py est lancé par GitHub Actions à chaque livraison. Il charge dynamiquement le dernier modèle depuis MLflow et l'évalue sur un jeu de données standardisé (water_std.csv). Si le F1-Score du modèle chute sous la barre d'acceptabilité des 60 %, le test échoue et la livraison continue (CI/CD) est instantanément bloquée
.
En résumé, je ne teste pas le script qui fabrique le modèle avec des tests unitaires, je teste de manière automatisée la performance du modèle final généré avant qu'il ne touche la production.


### Question 5
apport E4 concernant le développement de l'interface et de l'API de 'Drink Safe'. Vous mettez en avant une démarche d'éco-conception (Green IT) très intéressante. Concrètement, dans votre code, comment votre application évite-t-elle de consommer des ressources inutilement avant même de solliciter vos modèles de Machine Learning ?
Par ailleurs, en observant l'interface Web que vous avez développée pour les agents, votre audit d'accessibilité Lighthouse affiche un score de 74/100. En tant que concepteur, avez-vous identifié ce qu'il manque à votre code HTML/CSS pour améliorer ce score et vous rapprocher d'une conformité totale au RGAA ?"


>mon application évite effectivement de consommer des ressources inutilement avant même de solliciter les modèles de Machine Learning. J'ai implémenté un système de garde-fous sanitaires basé sur les standards admis par l'OMS
. Concrètement, dans mon fichier src/routes/predictions.py, le code vérifie les valeurs soumises
. Si un échantillon présente des valeurs aberrantes, comme un pH inférieur à 6.5 ou une turbidité supérieure à 5.0 NTU, l'API rejette immédiatement la requête
. Je m'assure de ce comportement grâce au test unitaire test_garde_fou_oms_turbidite_elevee
. Ce blocage précoce évite de réveiller un modèle ML lourd et d'effectuer des calculs inutiles, ce qui réduit directement l'empreinte énergétique du serveur
.
Pour votre seconde question sur l'accessibilité numérique et mon score Lighthouse, j'ai effectivement analysé ce résultat. Pour me rapprocher d'une conformité totale au RGAA, j'ai identifié trois actions correctives à mener sur mes templates HTML/CSS : je dois encore peaufiner les contrastes visuels, combler quelques lacunes dans les hiérarchies sémantiques des balises de titres pour faciliter la navigation au clavier, et surtout, il faut que j'ajoute les étiquettes (labels) qui sont actuellement manquantes sur les champs de mon formulaire
. Ces ajustements permettront une prise en charge parfaite par les lecteurs d'écran



### question 6
