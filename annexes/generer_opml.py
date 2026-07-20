"""
===============================================================================
Bloc         : E2 - Intégrer des modèles et services d'IA
Compétence   : C6 - Organiser et réaliser une veille technique et réglementaire

Description  :
Ce script automatise la génération d'un fichier d'export de flux RSS au format
standard OPML 2.0 à partir d'un dictionnaire Python. Il démontre la capacité à 
déployer et configurer des outils de veille de manière programmatique (DevOps).

Particularité technique :
Le dictionnaire de données intègre des URL pré-filtrées (via siftrss.com) 
permettant d'isoler le signal du bruit (ex: ciblage exclusif des alertes "CVE" 
sur GitHub ou des "Post-mortems" techniques sur Hacker News).
===============================================================================
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom

# 1. Données structurées par thématiques
veille_data = {
    "Réglementaire": [
        {"title": "CNIL", "xmlUrl": "https://www.cnil.fr/fr/rss.xml"}
    ],
    "Sécurité": [
        {"title": "CERT-FR (ANSSI)", "xmlUrl": "https://www.cert.ssi.gouv.fr/feed/"},
        {"title": "OWASP", "xmlUrl": "https://owasp.org/feed.xml"}
    ],
    "Technologique IA & Data": [
        {"title": "Hacker News", "xmlUrl": "https://siftrss.com/f/QVvj31xDbn"},
        {"title": "Towards Data Science", "xmlUrl": "https://medium.com/feed/towards-data-science"},
        {"title": "FastAPI (Releases)", "xmlUrl": "https://github.com/fastapi/fastapi/releases.atom"},
        {"title": "Scikit-Learn (Releases)", "xmlUrl": "https://github.com/scikit-learn/scikit-learn/releases.atom"}
    ],
    "Accessibilité": [
        {"title": "Association Valentin Haüy", "xmlUrl": "https://www.avh.asso.fr/fr/rss.xml"}
    ]
}

# 2. Construction de l'arbre XML au format OPML 2.0
opml = ET.Element('opml', version='2.0')
head = ET.SubElement(opml, 'head')
ET.SubElement(head, 'title').text = 'Veille Technologique et Réglementaire'

body = ET.SubElement(opml, 'body')

# Ajout des dossiers (catégories) et de leurs flux
for category, feeds in veille_data.items():
    category_outline = ET.SubElement(body, 'outline', text=category, title=category)
    for feed in feeds:
        ET.SubElement(
            category_outline, 'outline',
            type='rss',
            text=feed['title'],
            title=feed['title'],
            xmlUrl=feed['xmlUrl']
        )

# 3. Formatage pour obtenir un XML propre et indenté
xml_brut = ET.tostring(opml, encoding='utf-8')
xml_formate = minidom.parseString(xml_brut).toprettyxml(indent="    ")

# 4. Écriture du fichier final
nom_fichier = "veille_inoreader.opml"
with open(nom_fichier, "w", encoding="utf-8") as f:
    f.write(xml_formate)

print(f"Le fichier '{nom_fichier}' a été généré avec succès.")
