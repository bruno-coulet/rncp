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
        {"title": "Hacker News", "xmlUrl": "https://news.ycombinator.com/rss"},
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
