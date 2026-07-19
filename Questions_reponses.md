
Question 1 : Architecture MLOps et "Lazy Loading" (Blocs E3 / E4)
« Bonjour. Sur Drink Safe, vous parlez de "Lazy Loading" pour charger vos modèles d'IA en RAM à la volée lors de la première requête d'inférence, ce qui vous permet d'atteindre le "Zero Downtime". Mais en faisant cela, vous imposez un temps d'attente potentiellement énorme (le fameux Cold Start) au tout premier agent de terrain qui va faire une analyse, le temps que le lourd fichier .pkl soit téléchargé. Est-ce vraiment une bonne pratique d'expérience utilisateur ? Et que se passe-t-il pour cet agent si votre serveur MLflow est en panne exactement au moment de cette première requête ? »
❓ 

"En local le temps n'est pas énorme... Dès que les containers sont lancés, les modèles sont sur le volume partagé... au pire c'est le modèle précédent qui est servi."*
**Mon commentaire :** L'instinct est le bon (le volume partagé vous sauve !), mais dire "ce n'est pas un problème" est maladroit.
### 🛠️ Correction de la Question 1 : Le Lazy Loading et la panne MLflow


> *"Le Cold Start de quelques millisecondes pour le tout premier utilisateur est un compromis assumé pour garantir la stabilité au démarrage. Surtout, notre architecture est résiliente : les modèles téléchargés sont stockés physiquement dans un volume Docker partagé (`./mlruns_artifacts`). Si le serveur MLflow tombe en panne au moment de l'inférence, mon API ne crashe pas : elle va utiliser le dernier modèle qu'elle a déjà placé dans son cache en mémoire vive (RAM). C'est ce qui nous garantit un véritable Zero Downtime, même en cas de perte partielle de l'infrastructure."*

***

Question 2 : Cybersécurité et DNS Rebinding (Bloc E5)
« Dans votre rapport d'incidents, vous expliquez avoir résolu une erreur 403 (liée à la protection contre le DNS Rebinding de MLflow) en falsifiant l'en-tête Host de vos requêtes HTTP internes à la volée avec un "patch d'interception". En tant qu'architecte Sécurité, je trouve que bidouiller des en-têtes HTTP ressemble fortement à un "hack". Pourquoi avoir fait cela dans le code de votre API plutôt que de simplement configurer les hôtes autorisés (CORS / Allowed Hosts) proprement sur le serveur MLflow ? »
❓
"Ce problème ne se pose qu'en local... quand elle sera déployée, les requêtes viendront d'une IP certifiée... (il faudra juste enlever le patch ? Je ne sais pas)"*
**Mon commentaire :** Attention, piège ! En production dans un cluster Docker ou Kubernetes, les conteneurs continuent d'utiliser des noms de domaine internes (comme `mlflow:5000`). Il ne faut donc surtout pas dire que vous retirerez le patch.

### 🛠️ Correction de la Question 2 : Le Hack DNS Rebinding

> *"Ce n'est pas un 'hack', c'est un choix d'architecture assumé. Dans un réseau Docker isolé, modifier la configuration de sécurité native du serveur MLflow pour ouvrir ses CORS et ses Allowed Hosts à tout le réseau affaiblirait sa sécurité globale. J'ai préféré patcher la requête sortante au niveau de mon API FastAPI. Le spoofing d'en-tête en interne me permet de faire communiquer mes micro-services de manière fluide, tout en préservant la forteresse de sécurité native du serveur MLflow."*

***

Question 3 : Data Engineering et Big Data (Bloc E1)
« Pour l'Observatoire de la Mobilité, vous justifiez l'utilisation du moteur DuckDB par sa capacité à faire du Predicate Pushdown sur des fichiers Parquet, évitant ainsi de saturer la RAM. Or, vous savez sûrement que la librairie Pandas (couplée au moteur PyArrow) permet déjà de lire des fichiers Parquet en filtrant directement les colonnes à la source via les paramètres de pd.read_parquet(). Pourquoi avoir ajouté la complexité d'un nouveau moteur SQL comme DuckDB à votre stack technologique, alors que Pandas pouvait techniquement faire la même chose ? »

### 🛠️ Correction de la Question 3 : DuckDB vs Pandas (Big Data)

**Votre brouillon :** *"- le cahier des charges demandait l'utilisation de Big Data. - Duckdb permet d'utiliser du SQL directement sur les fichiers, c'est plus rapide."*
**Mon commentaire :** Ne dites jamais que vous avez utilisé une techno "parce que c'était demandé dans le REAC", cela donne l'impression d'un projet artificiel. Défendez la technique de gestion de la mémoire (RAM vs Disque).


> *"Il est vrai que le référentiel demande d'explorer les technologies Big Data, mais le choix de DuckDB est techniquement justifié. Pandas charge l'intégralité du DataFrame en mémoire vive (RAM). Si mon fichier d'historique de trottinettes atteint 15 Go, mon serveur va crasher avec une erreur 'Out Of Memory'. Avec DuckDB, j'exécute des requêtes analytiques en SQL directement sur le disque. Grâce au 'Predicate Pushdown', la requête filtre les données avant même de les charger en RAM, ce qui est infiniment plus scalable et éco-responsable."*

***

Message reçu cinq sur cinq : **nous arrêtons l'entraînement oral pour le moment !** Vos réflexes sont là, il suffira de relire ces trois formulations la veille de votre passage.

**Retournons sur vos slides.** 
Tous les livrables (E1, E2, E3, E4, E5) et tous vos supports visuels (Canva Mobilité + Canva Drink Safe) me semblent désormais complets, structurés et validés. 

Y a-t-il une diapositive en particulier, un texte, ou un schéma sur lequel vous souhaitez que nous apportions une ultime retouche ?