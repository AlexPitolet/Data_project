from dash import html

layout = html.Div([
    html.H2("À propos"),
    html.H4("Présentation du projet"),
    html.P(
            "Ce projet a été réalisé par Alex PITOLET et Antoine MARMOL dans le cadre de l’UE Projet Multidisciplinaire 1. "
            "Il vise à analyser la consommation d’électricité en France à travers une approche "
            "géographique et temporelle, afin de mettre en évidence les disparités territoriales "
            "et les dynamiques de consommation entre 2011 et 2024."
        ),
    html.H4("Choix des données"),
    html.P(
            "Les données utilisées proviennent de sources publiques en open data (license Apache 2.0) et décrivent "
            "la consommation annuelle d’électricité à l’échelle communale. "
            "Lien vers la page du dataset : https://www.data.gouv.fr/datasets/consommation-annuelle-delectricite-et-gaz-par-commune"
        ),
    html.H4("Traitement des données"),
    html.P(
            "Un pipeline de traitement a été mis en place pour assurer la récupération, le nettoyage "
            "et l’agrégation des données. Les fichiers sont organisés selon une arborescence claire "
            "séparant les données brutes, nettoyées et les scripts de traitement, garantissant "
            "la reproductibilité du projet."
            "Les données ont été agrégées aux niveaux départemental et régional afin de permettre "
            "une analyse multi-échelle du territoire français. Les valeurs aberrantes (infinies ou absentes sont filtées) "
            "puis de nouveaux fichiers .csv sont générés avec des valeurs exploitables."
        ),
    html.H4("Fonctionnalités du dashboard"),
    html.P(
            "Le dashboard est interactif, cela permet à l’utilisateur de naviguer entre différentes pages."
            "Sur la page d'accueil, l'utilisateur voit un bref résumé du dashboard et de ses fonctionnalités"
            "Sur la page \"carte\", il trouveras une carte intéractive de la France munie de trois menus déroulants."
            "Grâce à eux, il peut modifier un des trois paramètres de visualisation : l'année,l'échelle et le type de consommation"
            "Le dashboard présente aussi deux histogrammes, l'un d'eux est un histogramme non catégoriel montrant la répartition des communes en fonction de leur consommation annuelle. "
            "Le second histogramme est un graphique dynamique, il représente la consommation moyenne de chaque régions (variable catégorielle) en fonction de l'année."
            "Et enfin la dernière page (à propos), présente en détail le dashboard et son fonctionnement."
        ),
    html.H4("Limites et difficultées rencontrées"),
    html.P(
            "Certaines limites doivent être prises en compte dans l’interprétation des résultats. "
            "La consommation moyenne repose sur des données agrégées et peut être affectée par "
            "des valeurs manquantes ou instables, notamment pour les années récentes. "
            "De nombreuses colonnes du dataset sont vide; par exemple , l’absence de données démographiques empêche une normalisation par habitant. "
            "Pour ce qui est des difficultés, nous en avons eu plusieurs majeures."
            "La taille conséquente de celui-ci (800 Mo, 3 400 000 lignes et 46 colonnes) nous a bloqué pendant un moment. En effet, il est trop lourd pour être push sur le répertoire distant. "
            "Nous avions fait l'erreur de commit avec le dataset... Quand nous avons push, github refusait de recevoir ce fichier trop important."
            "Suite à cela, l'historique de commit a du être effacé et nous avons décider de créer un nouveau répertoire distant ainsi que de travailler dans "
            "des branches différentes du main afin qu'elles puissent être supprimées en cas de problème."
            "Nous avons du mettre en place une méthode python qui vérifie si le dataset et déjà installé ou non. Et s'il n'y est pas, "
            "il est automatiquement récupéré via le lien de téléchargement du fichier .csv"
            "Deuxième problème, la technologie aprise dans le cours pour faire des cartes chloropleth était folium. Or, nous nous sommes vite"
            "rendus compte que le chargement des donnée était beaucoup trop long et ce n'était pas fluide."
            "De plus nous ne savions pas comment l'intégrer au sein de l'application Dash."
            "Nous avons donc pris un tournant en nous dirigeant vers la librairie plotly_express qui propose également une carte chloropleth fonctionnant de manière similaire. "
            "Au début, nous voulions une carte affichant trois niveau de précisions : communale, départementale et régionnale. "
            "Mais nous avons constaté que l'échelle communale était bien trop lente à générer et elle n'était pas très pertinente "
            "alors nous avons décider de ne garder que les deux échelles restantes."
            ""
        ),
    html.H4("Axes d'améliorations"),
    html.P(
            "Ce travail pourrait être enrichi par l’ajout de données de population, "
            "une comparaison avec d’autres sources d’énergie, ou encore une analyse de l’évolution "
            "temporelle plus fine. Des indicateurs normalisés ou des projections futures "
            "pourraient également compléter l’analyse."
            "Un chantier de design pourrait être bénéfique pour rendre le dashboard plus visuel. "
            ""
        ),
    html.H4("Organisation du projet"),
    html.Ul([
        html.Li([
            html.B("Antoine – Carte & récupération des données : "),
            "recupération des données (pipeline get_data.py url → data/raw), et nettoyage des données pour la carte, "
            "conception et implémentation de la carte intéractive, "
            "structuration de l’application Dash (navigation multi-pages, callbacks, composants), "
            "et gestion de l’interactivité globale du dashboard."
            "ainsi que la rédaction des pages descriptives et des contenus d’analyse de la carte."
        ]),
        html.Li([
            html.B("Alex – Histogrammes & traitement des données : "),
            "nettoyage et préparation des données (pipeline data/raw → data/cleaned) pour les histogrammes, "
            "développement de l’histogramme dynamique basé sur une variable non catégorielle, "
            "création de l’histogramme catégoriel, "
            "ainsi que la rédaction des pages descriptives et des contenus d’analyse liés aux histogrammes. "
        ]),
    ]),
    html.H4("Technologies utilisées"),
    html.Ul([
        html.Li("Python 3.1x.x"),
        html.Li("pandas"),
        html.Li("numpy"),
        html.Li("dash"),
        html.Li("plotly-express"),
    ]),
],
style={
        "margin":"auto",
        "width":"50vw",
        "textAlign": "justify"
    })
