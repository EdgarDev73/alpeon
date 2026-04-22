#!/usr/bin/env python3
"""
Translate FR estimateur station pages → EN.
Usage: python3 translate_estimateur.py
"""
import re, os

# ── Universal text replacements (FR → EN) ─────────────────────────────────
UNIVERSAL = [
    # HTML lang
    ('<html lang="fr">', '<html lang="en">'),
    # og:locale
    ('content="fr_FR"', 'content="en_GB"'),
    # Nav labels
    ('>Accueil<', '>Home<'),
    ('>Propriétaires<', '>Property Owners<'),
    # Estimateur nav link text only (not inside URLs)
    # handled via regex below
    ('>Réserver<', '>Book<'),
    ('>Destinations<', '>Destinations<'),
    ('>À propos<', '>About<'),
    ('>Appelez-nous<', '>Call us<'),
    # Breadcrumb aria-label
    ('aria-label="Fil d\'Ariane"', 'aria-label="Breadcrumb"'),
    # Breadcrumb text
    ('>Accueil</a></li>', '>Home</a></li>'),
    ('>Estimateur</a></li>', '>Estimator</a></li>'),
    # Hero buttons
    ('>Estimer mes revenus gratuitement\n', '>Estimate my income for free\n'),
    ('Estimer mes revenus gratuitement', 'Estimate my income for free'),
    ('>Découvrir nos services<', '>Discover our services<'),
    # Stats label
    ('Revenus moy/an', 'Avg. income/yr'),
    # Widget head
    ('3 questions pour affiner votre estimation', '3 questions to refine your estimate'),
    # Step tracker labels
    ('>Station<', '>Resort<'),
    ('>Bien<', '>Property<'),
    ('>Niveau<', '>Level<'),
    # Step 1
    ('<h3>Dans quelle station est votre bien ?</h3>', '<h3>Which resort is your property in?</h3>'),
    ('placeholder="Sélectionner une station…"', 'placeholder="Select a resort…"'),
    ('placeholder="Rechercher…"', 'placeholder="Search…"'),
    ('Veuillez sélectionner une station.', 'Please select a resort.'),
    # Step 2
    ('<h3>Parlez-nous de votre bien</h3>', '<h3>Tell us about your property</h3>'),
    ('>Type de propriété<', '>Property type<'),
    ('data-t="appartement" onclick="selTypeProp(this)">Appartement<', 'data-t="appartement" onclick="selTypeProp(this)">Apartment<'),
    ('data-t="penthouse" onclick="selTypeProp(this)">Penthouse<', 'data-t="penthouse" onclick="selTypeProp(this)">Penthouse<'),
    ('Veuillez sélectionner un type de propriété.', 'Please select a property type.'),
    ('>Surface habitable<', '>Living area<'),
    ('<strong>Couchages</strong>', '<strong>Sleeping capacity</strong>'),
    ('Tous lits confondus, canapé-lit inclus', 'All beds combined, sofa bed included'),
    # Step 3
    ('<h3>Comment est votre intérieur ?</h3>', '<h3>How is your interior?</h3>'),
    ('>Entrée de gamme<', '>Entry level<'),
    ('Mobilier standard, équipements basiques', 'Standard furniture, basic equipment'),
    ('>Correct<', '>Good condition<'),
    ('Bon état général, entretenu', 'Good overall condition, well-maintained'),
    ('>Standing<', '>High-end<'),
    ('Finitions qualitatives, cuisine équipée', 'Quality finishes, fitted kitchen'),
    ('>Prestige<', '>Prestige<'),
    ('Décoration soignée, équipements premium', 'Refined décor, premium equipment'),
    ('>Luxe &amp; exception<', '>Luxury &amp; exceptional<'),
    ('Mobilier haut de gamme, spa, vue ou services exclusifs', 'High-end furniture, spa, views or exclusive services'),
    ('Veuillez sélectionner le niveau du bien.', 'Please select the property level.'),
    # Equipment section
    ('>Équipements<', '>Amenities<'),
    ('style="margin-top:24px;display:block">Équipements<', 'style="margin-top:24px;display:block">Amenities<'),
    # Equipment names
    ('>Sauna / Hammam<', '>Sauna / Hammam<'),
    ('>Piscine intérieure<', '>Indoor pool<'),
    ('>Spa / Jacuzzi<', '>Spa / Jacuzzi<'),
    ('>Cheminée / Poêle<', '>Fireplace / Wood burner<'),
    ('>Salle de sport<', '>Gym<'),
    ('>Home cinéma<', '>Home cinema<'),
    # Step 4 contact
    ('>Votre estimation est prête<', '>Your estimate is ready<'),
    ('>votre station</span>, plus qu\'une étape.<', '>your resort</span>, just one more step.<'),
    # Contact labels
    ('>Prénom<', '>First name<'),
    ('placeholder="Jean"', 'placeholder="John"'),
    ('>Nom<', '>Last name<'),
    ('placeholder="Dupont"', 'placeholder="Smith"'),
    ('>Téléphone<', '>Phone<'),
    ('Champ requis.', 'Required field.'),
    ('Email invalide.', 'Invalid email.'),
    ('Vous devez accepter pour continuer.', 'You must accept to continue.'),
    # GDPR
    ("J'accepte qu'ALPÉON me recontacte pour discuter de mon bien.", "I agree that ALPÉON may contact me to discuss my property."),
    ('Politique de confidentialité.', 'Privacy policy.'),
    # Step nav
    ('>← Retour<', '>← Back<'),
    ('>Continuer →<', '>Continue →<'),
    # Sidebar
    ('>Votre projection<', '>Your projection<'),
    ('Complétez les étapes pour voir votre estimation.', 'Complete the steps to see your estimate.'),
    ('>Loyer garanti versé mensuellement<', '>Guaranteed rent paid monthly<'),
    ('Données réelles · 200+ biens gérés', 'Real data · 200+ properties managed'),
    ('4 étapes, résultat immédiat', '4 steps, instant result'),
    ('Visite gratuite, sans engagement', 'Free visit, no commitment'),
    # Results section
    ('>Votre estimation ALPÉON<', '>Your ALPÉON Estimate<'),
    ('>Revenus estimés pour votre bien<', '>Estimated income for your property<'),
    ('>Revenus annuels estimés<', '>Estimated annual income<'),
    ('>nette de charges locatives<', '>net of rental charges<'),
    ('>Loyer garanti<', '>Guaranteed rent<'),
    ('Calendrier des versements · Saison hiver', 'Payment schedule · Winter season'),
    ('>ALPÉON en action<', '>ALPÉON in action<'),
    ('* Estimation indicative basée sur les données de performance du parc ALPÉON. Les résultats réels dépendent de la disponibilité effectivement accordée, de la dynamique de la station et des conditions du marché. Un conseiller ALPÉON vous contactera pour affiner cette projection.',
     '* Indicative estimate based on performance data from the ALPÉON portfolio. Actual results depend on availability granted, resort dynamics and market conditions. An ALPÉON advisor will contact you to refine this projection.'),
    # CTA section
    ('>Prochaine étape<', '>Next step<'),
    ('<h2>Planifiez votre<br><em>visite gratuite</em></h2>', '<h2>Schedule your<br><em>free visit</em></h2>'),
    ("Un conseiller ALPÉON se déplace dans votre bien, affine l'estimation et vous présente notre offre de gestion. 45 minutes, sans engagement, à votre convenance.",
     'An ALPÉON advisor visits your property, refines the estimate and presents our management offer. 45 minutes, no commitment, at your convenience.'),
    ('>Planifier ma visite gratuite<', '>Schedule my free visit<'),
    ('>Gratuit<', '>Free<'),
    ('>Sans engagement<', '>No commitment<'),
    ('>Réponse sous 24h<', '>Reply within 24h<'),
    # Other stations section
    ('>Estimateurs<', '>Estimators<'),
    ('>Autres stations alpines<', '>Other Alpine resorts<'),
    ('>Estimer ', '>Estimate '),
    # FAQ section
    ('>Questions fréquentes<', '>Frequently asked questions<'),
    # Destination CTA generic
    ('>Planifiez votre visite<', '>Schedule your visit<'),
    ('>Prendre rendez-vous<', '>Book an appointment<'),
    ("Lancer l'estimateur", 'Launch the estimator'),
    ('Analyse de votre bien, projection de revenus personnalisée, sans engagement.', 'Property analysis, personalised income projection, no commitment.'),
    # Footer
    ("Estimez votre loyer garanti", "Estimate your guaranteed rent"),
    ('>Alpine Property Management<', '>Alpine Property Management<'),
    ('Gestionnaire premium de la location saisonnière alpine. Loyer fixe garanti, conciergerie haut de gamme, transparence totale.',
     'Premium manager of Alpine short-term rentals. Guaranteed fixed rent, premium concierge, full transparency.'),
    ('>Destinations<', '>Destinations<'),
    ('>Services<', '>Services<'),
    ('>Contact<', '>Contact<'),
    ('>Légal<', '>Legal<'),
    # Footer links text
    ('>Propriétaires<', '>Property Owners<'),
    ("ALPÉON Signatures", "ALPÉON Signatures"),
    ("Estimateur de revenus", "Rental Income Estimator"),
    (">À propos<", ">About<"),
    (">FAQ<", ">FAQ<"),
    (">Mentions légales<", ">Legal notice<"),
    (">Politique de confidentialité<", ">Privacy policy<"),
    (">Conditions générales<", ">Terms & conditions<"),
    (">Réseaux sociaux<", ">Social media<"),
    (">Newsletter<", ">Newsletter<"),
    ('placeholder="votre@email.fr"', 'placeholder="your@email.com"'),
    (">S'inscrire<", ">Subscribe<"),
    ('Nouvelles propriétés, offres de saison et actualités alpines.', 'New properties, seasonal offers and alpine news.'),
    ('© 2026 ALPÉON. Tous droits réservés.', '© 2026 ALPÉON. All rights reserved.'),
    ('ALPÉON est une marque de VerSpi Real Estate', 'ALPÉON is a brand of VerSpi Real Estate'),
    # Callpop
    ('>Obtenez une estimation précise<', '>Get a precise estimate<'),
    ('Votre estimation est une première base solide. Un conseiller ALPÉON visite votre bien et affine la projection, gratuitement et sans engagement.',
     'Your estimate is a solid first step. An ALPÉON advisor visits your property and refines the projection, free of charge and with no commitment.'),
    ('>Réserver un appel<', '>Book a call<'),
    ('aria-label="Fermer"', 'aria-label="Close"'),
    # Modal
    ('>On prépare votre estimation…<', '>Preparing your estimate…<'),
    ('>Vérification des données de la station<', '>Checking resort data<'),
    ("Estimation du potentiel de votre bien", "Estimating your property's potential"),
    ('>Préparation de votre rapport personnalisé<', '>Preparing your personalised report<'),
    # Callback popup
    ('aria-label="Être rappelé par un expert"', 'aria-label="Get a call from an expert"'),
    ('Offre personnalisée · Gratuit · Sans engagement', 'Personalised offer · Free · No commitment'),
    ('>Transformez votre bien en revenu garanti<', '>Turn your property into guaranteed income<'),
    ('Nos experts analysent votre estimation et vous proposent une offre personnalisée.', 'Our experts analyse your estimate and propose a personalised offer.'),
    ('placeholder="Jean"', 'placeholder="John"'),  # cb form first name
    ('>Être rappelé par un expert<', '>Get a call from an expert<'),
    ('>Non merci, je reviendrai plus tard<', ">No thanks, I'll come back later<"),
    (">C'est noté !<", ">Noted!<"),
    ("Un expert ALPÉON vous rappelle prochainement pour affiner votre estimation.", "An ALPÉON expert will call you back shortly to refine your estimate."),
    # Cookie bar
    ('Nous utilisons des cookies analytiques pour mesurer l\'audience et améliorer votre expérience.',
     'We use analytics cookies to measure audience and improve your experience.'),
    ('>En savoir plus<', '>Learn more<'),
    ('>Refuser<', '>Decline<'),
    ('>Accepter<', '>Accept<'),
    # WhatsApp
    ('>Besoin d\'aide ?<', '>Need help?<'),
    # JS strings
    ("'Complétez les étapes pour révéler votre estimation.'", "'Complete the steps to reveal your estimate.'"),
    ("'Renseignez les étapes pour voir votre projection.'", "'Fill in the steps to see your projection.'"),
    ("'Choisir le niveau →'", "'Choose level →'"),
    ("'Révéler mon estimation →'", "'Reveal my estimate →'"),
    ("'Obtenir mon estimation'", "'Get my estimate'"),
    # step indicator
    ("`Étape ${visStep} sur 3`", "`Step ${visStep} of 3`"),
    ("'votre station'", "'your resort'"),
    # selTypeProp labels
    ("'Appartement sélectionné.'", "'Apartment selected.'"),
    ("'Chalet sélectionné.'", "'Chalet selected.'"),
    ("'Penthouse sélectionné.'", "'Penthouse selected.'"),
    # location picker
    ("isChalet ? 'Quartier' : 'Résidence'", "isChalet ? 'Area' : 'Residence'"),
    ("'Choisir une résidence'", "'Choose a residence'"),
    # Toast bonus
    ("'emplacement premium, <strong>+15%</strong> sur l\\'estimation.'", "'premium location, <strong>+15%</strong> on your estimate.'"),
    ("'bon emplacement, dans la moyenne.'", "'good location, within average.'"),
    ("'emplacement standard, estimation ajustée.'", "'standard location, estimate adjusted.'"),
    # EQ_LABELS JS
    ("spa:'Spa / Jacuzzi'", "spa:'Spa / Jacuzzi'"),
    ("ski:'Ski au pied'", "ski:'Ski-in/ski-out'"),
    ("parking:'Parking privatif'", "parking:'Private parking'"),
    ("terrasse:'Terrasse / balcon'", "terrasse:'Terrace / balcony'"),
    ("cheminee:'Cheminée / poêle'", "cheminee:'Fireplace / wood burner'"),
    ("concierge:'Conciergerie'", "concierge:'Concierge'"),
    ("sauna:'Sauna / Hammam'", "sauna:'Sauna / Hammam'"),
    ("piscine:'Piscine intérieure'", "piscine:'Indoor pool'"),
    ("salle:'Salle de sport'", "salle:'Gym'"),
    ("cinema:'Home cinéma'", "cinema:'Home cinema'"),
    # EQ_FR JS (submit payload)
    ("spa:'Spa / Jacuzzi'", "spa:'Spa / Jacuzzi'"),
    # removed eq
    ("' retiré.'", "' removed.'"),
    ("' ajouté.'", "' added.'"),
    # buildResRecap labels
    ("{ label:'Station',", "{ label:'Resort',"),
    ("{ label:'Surface',", "{ label:'Area',"),
    ("{ label:'Capacité',", "{ label:'Capacity',"),
    ("{ label:'État',", "{ label:'Condition',"),
    # etatLabels
    ("budget:'Entrée de gamme'", "budget:'Entry level'"),
    ("correct:'Correct'", "correct:'Good condition'"),
    ("standing:'Standing'", "standing:'High-end'"),
    ("luxe:'Luxe'", "luxe:'Luxury'"),
    # typeBienLabels
    ("appartement:'Appartement'", "appartement:'Apartment'"),
    # ETAT_FR
    ("budget:'Entrée de gamme',", "budget:'Entry level',"),
    ("correct:'Correct',", "correct:'Good condition',"),
    ("standing:'Standing',", "standing:'High-end',"),
    ("luxe:'Luxe'", "luxe:'Luxury'"),
    # EQ_FR object
    ("spa:'Spa / Jacuzzi', ski:'Ski au pied', parking:'Parking privatif', terrasse:'Terrasse / balcon', cheminee:'Cheminée / poêle', concierge:'Conciergerie', sauna:'Sauna / Hammam', piscine:'Piscine intérieure', salle:'Salle de sport', cinema:'Home cinéma'",
     "spa:'Spa / Jacuzzi', ski:'Ski-in/ski-out', parking:'Private parking', terrasse:'Terrace / balcony', cheminee:'Fireplace / wood burner', concierge:'Concierge', sauna:'Sauna / Hammam', piscine:'Indoor pool', salle:'Gym', cinema:'Home cinema'"),
    # source tag
    ("source:'estimateur-station'", "source:'estimateur-station-en'"),
    # newsletter
    ("'Entrez votre email.'", "'Please enter your email.'"),
    ("'Inscription…'", "'Subscribing…'"),
    ("msg.textContent='Merci ! Vous êtes inscrit.';", "msg.textContent='Thank you! You are subscribed.';"),
    ("msg.textContent='Erreur. Réessayez.';", "msg.textContent='Error. Please try again.';"),
    ("msg.textContent='Erreur réseau.';", "msg.textContent='Network error.';"),
    # station list empty
    ('"Aucune station trouvée"', '"No resort found"'),
]

# ── Station-specific data ───────────────────────────────────────────────────
STATIONS = {
    'courchevel': {
        'slug': 'courchevel',
        'name': 'Courchevel',
        'meta_title': 'Courchevel Rental Income Estimator · 2025/2026 Rental Returns | ALPÉON',
        'meta_desc': 'How much does your apartment or chalet in Courchevel earn from short-term rental? Estimate your rental income: from €20,000 to €130,000/year. The most prestigious ski resort in the Alps. Free simulation.',
        'og_title': 'Courchevel Rental Income Estimator · 2025/2026 Rental Returns | ALPÉON',
        'og_desc': 'How much does your apartment or chalet in Courchevel earn? From €20,000 to €130,000/year. The most prestigious resort in the Alps. Free simulation.',
        'hero_h1': 'Courchevel Rental Income Estimator :<br><em>how much does your property earn?</em>',
        'hero_sub': 'The most prestigious ski resort in France: ultra-premium clientele, the highest rental rates per m² in the Alps, 600 km of the 3 Vallées. Discover the true potential of your property.',
        'schema_breadcrumb_name': 'Courchevel Estimator',
        'alpeon_eyebrow': 'ALPÉON in Courchevel',
        'alpeon_h2': 'Premium management for an exceptional resort',
        'faq_h2': 'Everything about renting in Courchevel',
        'cta_h2': 'Meet an ALPÉON advisor<br>in <em>Courchevel</em>',
        'footer_owner': 'Own a property in Courchevel?',
        'footer_bottom_last': 'Premium Alpine short-term rental management · Courchevel · French Alps',
        'newsletter_source': 'footer-courchevel-en',
        'faq_items': [
            ('How much does an apartment earn from rental in Courchevel?',
             'An apartment in Courchevel generates between €20,000 and €68,000 in annual rental income depending on size, finish and location within the resort. An apartment in Courchevel 1850 with prestige finishes can reach €68,000/year, among the highest in the French Alps. Weekly rents in peak season range from €1,500 for a studio in 1550 to over €15,000 for a large prestige apartment in 1850.'),
            ('What rental income for a chalet in Courchevel?',
             'Chalets in Courchevel command the highest annual rents in the French Alps: between €60,000 and €130,000/year depending on size and finish. In peak season, large luxury chalets in Courchevel 1850 rent for between €30,000 and €60,000 per week, with private chef, integrated spa and indoor pool. Demand far exceeds supply in this segment, justifying unrivalled rents in France.'),
            ('Courchevel 1850 or Courchevel 1650: what rent by village?',
             'Courchevel comprises four villages at different altitudes with distinct rental markets. Courchevel 1850 (Le Belvédère) is the ultra-premium segment: rents up to €130,000/year for large chalets. Courchevel 1650 (Moriond) offers excellent value with revenues between €30,000 and €80,000/year. The 1550 and 1300 villages target a more regional clientele with rents between €15,000 and €40,000/year. At any altitude, proximity to ski lifts remains the number-one value factor.'),
            ('Who rents property in Courchevel?',
             'Courchevel attracts the wealthiest clientele in the French Alps. At Courchevel 1850, the main tenants are wealthy French, British, Middle Eastern and Asian families and groups, often with assets exceeding €10 million. This UHNW clientele associates Courchevel with social status and returns every season, often booking the same properties year after year. Client retention is a key advantage for owners committed to professional quality management.'),
            ('Does ALPÉON manage properties in Courchevel 1850?',
             'Yes, ALPÉON manages apartments and chalets across the different Courchevel villages, including Courchevel 1850. Our approach is tailored to each segment: for ultra-premium properties in 1850, we coordinate hotel-level concierge services, private chefs and bespoke services. For properties in other villages, we provide professional, efficient management that optimises rental income while preserving long-term property quality.'),
        ],
        'alpeon_p1': 'In Courchevel, property owners expect impeccable management befitting the resort\'s prestige. ALPÉON operates across the four Courchevel villages, offering rental management that respects the premium positioning of each property, from Moriond apartments to the exceptional chalets of 1850.',
        'alpeon_p2': 'Our network of local service providers (private chefs, helicopter transfer services, private ski instructors, mobile spa) allows us to offer guests a complete experience that justifies premium rents and builds loyalty among a highly demanding international clientele.',
    },
    'megeve': {
        'slug': 'megeve',
        'name': 'Megève',
        'meta_title': 'Megève Rental Income Estimator · 2025/2026 Rental Returns | ALPÉON',
        'meta_desc': 'How much does your apartment or chalet in Megève earn from short-term rental? Estimate your rental income: from €22,000 to €140,000/year. One of the most charming Alpine resorts. Free simulation.',
        'og_title': 'Megève Rental Income Estimator · 2025/2026 Rental Returns | ALPÉON',
        'og_desc': 'How much does your apartment or chalet in Megève earn? From €22,000 to €140,000/year. The most charming resort in the French Alps. Free simulation.',
        'hero_h1': 'Megève Rental Income Estimator :<br><em>how much does your property earn?</em>',
        'hero_sub': 'The Rothschild village at 1,113 m, discreet French luxury, a loyal Parisian and international clientele, the Évasion Mont Blanc ski area. The highest rental incomes in the Northern Alps.',
        'schema_breadcrumb_name': 'Megève Estimator',
        'alpeon_eyebrow': 'ALPÉON in Megève',
        'alpeon_h2': 'Your property in an exceptional resort',
        'faq_h2': 'Everything about renting in Megève',
        'cta_h2': 'Meet an ALPÉON advisor<br>in <em>Megève</em>',
        'footer_owner': 'Own a property in Megève?',
        'footer_bottom_last': 'Premium Alpine short-term rental management · Megève · French Alps',
        'newsletter_source': 'footer-megeve-en',
        'faq_items': [
            ('How much does an apartment earn from rental in Megève?',
             'An apartment in Megève generates between €22,000 and €75,000 in annual rental income depending on size, location and finish. Apartments in the village centre or close to the ski lifts command the highest rents, with weekly rates in peak season ranging from €2,000 for a small studio to over €12,000 for a large prestige apartment.'),
            ('What rental income for a chalet in Megève?',
             'Chalets in Megève reach the highest annual rents in the Northern Alps, between €65,000 and €140,000/year depending on size and amenities. Chalets with Mont Blanc views, an indoor pool or private spa command a significant premium. In peak season, the finest Megève chalets rent for between €15,000 and €40,000 per week.'),
            ('Who is the rental clientele in Megève?',
             "Megève's clientele is characterised by loyalty and financial strength. The primary tenants are wealthy Parisian families who often have a multigenerational relationship with the resort, alongside a growing international clientele — Belgian, Swiss, British and American. This loyal clientele tends to book well in advance and return to the same properties each season, which is a major advantage for property owners."),
            ('Is Megève a good resort for investment and rental?',
             'Megève is one of the best destinations in the Alps for a prestigious rental investment. The resort\'s century-old reputation, its preserved authenticity and the loyalty of its clientele make it a highly resilient market. Prices are more stable than in higher-altitude resorts, and the rental season extends beyond the winter with a spring and summer season that generates additional income.'),
            ('Does ALPÉON offer property management in Megève?',
             "Yes, ALPÉON manages apartments and chalets in Megève with an approach tailored to the resort's spirit. Our management in Megève focuses on the quality of the tenant experience rather than maximising occupancy. We work with selected local craftsmen and service providers to maintain the high standards expected by a discerning clientele."),
        ],
        'alpeon_p1': 'Megève embodies discreet, authentic French luxury. ALPÉON manages apartments and chalets in the resort\'s most sought-after locations, from the historic village centre to the prestigious Mont d\'Arbois plateau, delivering management that matches the exceptional character of each property.',
        'alpeon_p2': 'Our in-depth knowledge of Megève\'s loyal and demanding clientele allows us to optimise pricing week by week while maintaining the quality standards expected by guests who have been returning to the same resort for generations.',
    },
    'meribel': {
        'slug': 'meribel',
        'name': 'Méribel',
        'meta_title': 'Méribel Rental Income Estimator · 2025/2026 Rental Returns | ALPÉON',
        'meta_desc': 'How much does your apartment or chalet in Méribel earn from short-term rental? Estimate your rental income: from €16,000 to €100,000/year. The heart of Les 3 Vallées. Free simulation.',
        'og_title': 'Méribel Rental Income Estimator · 2025/2026 Rental Returns | ALPÉON',
        'og_desc': 'How much does your apartment or chalet in Méribel earn? From €16,000 to €100,000/year. The heart of the 3 Vallées. Free simulation.',
        'hero_h1': 'Méribel Rental Income Estimator :<br><em>how much does your property earn?</em>',
        'hero_sub': 'Central resort of the 3 Vallées at 1,400 m, loyal and affluent British clientele, 600 km of skiing, authentic Savoyard architecture. The heart of the world\'s largest ski area.',
        'schema_breadcrumb_name': 'Méribel Estimator',
        'alpeon_eyebrow': 'ALPÉON in Méribel',
        'alpeon_h2': 'Expertise in the British market',
        'faq_h2': 'Everything about renting in Méribel',
        'cta_h2': 'Meet an ALPÉON advisor<br>in <em>Méribel</em>',
        'footer_owner': 'Own a property in Méribel?',
        'footer_bottom_last': 'Premium Alpine short-term rental management · Méribel · French Alps',
        'newsletter_source': 'footer-meribel-en',
        'faq_items': [
            ('How much does an apartment earn from rental in Méribel?',
             'An apartment in Méribel generates between €16,000 and €52,000 in annual rental income depending on size, location and finish. Apartments in Méribel Village centre or at Méribel-Mottaret close to the slopes command the highest rents, with weekly rates in peak season ranging from €1,200 for a small apartment to over €10,000 for a large prestige property.'),
            ('What rental income for a chalet in Méribel?',
             'Chalets in Méribel reach between €48,000 and €100,000/year. The British clientele, which accounts for 40% of rental demand, willingly rents large chalets for week-long family stays. In peak Christmas and February half-term weeks, the finest chalets rent for between €15,000 and €35,000 per week.'),
            ('Why does Méribel attract so many British guests?',
             'Méribel was founded in 1938 by a Scotsman, Peter Lindsay, who wanted to create a resort preserving traditional Savoyard architecture. This British origin explains the multigenerational attachment of UK families to the resort. Today, British guests represent around 40% of international visitors, attracted by direct flights from UK airports, English-speaking services and a strong sense of community.'),
            ('Is Méribel a good resort for investment and rental?',
             "Méribel has a very strong investment profile. Its central position in the 3 Vallées guarantees lasting appeal regardless of snow conditions at isolated resorts. The clientele is loyal, financially strong and tends to book well in advance. The international reputation of the resort, reinforced by its profile as a British favourite, ensures sustained demand across all property segments."),
            ('Does ALPÉON offer property management in Méribel?',
             'Yes, ALPÉON manages apartments and chalets in Méribel with particular expertise in the English-speaking market. Our bilingual team handles the entire tenant relationship — English-language listings, direct communication and a welcome adapted to British guests. This allows us to reach a loyal, solvent clientele and optimise revenues week by week.'),
        ],
        'alpeon_p1': 'Méribel sits at the heart of the 3 Vallées, the world\'s largest ski area, making it one of the most sought-after destinations for British and international property investors. ALPÉON manages apartments and chalets across all of Méribel\'s villages — Méribel Village, Les Allues, and Méribel-Mottaret — with full bilingual management.',
        'alpeon_p2': 'Our deep knowledge of the British rental market in Méribel allows us to position your property on the most relevant platforms and build a loyal clientele that returns each season, generating stable and predictable rental income.',
    },
    'tignes': {
        'slug': 'tignes',
        'name': 'Tignes',
        'meta_title': 'Tignes Rental Income Estimator · 2025/2026 Rental Returns | ALPÉON',
        'meta_desc': "How much does your apartment or chalet in Tignes earn from short-term rental? Estimate your rental income: from €17,000 to €90,000/year. Glacier skiing, Europe's longest season. Free simulation.",
        'og_title': 'Tignes Rental Income Estimator · 2025/2026 Rental Returns | ALPÉON',
        'og_desc': "How much does your apartment or chalet in Tignes earn? From €17,000 to €90,000/year. Europe's longest ski season. Free simulation.",
        'hero_h1': 'Tignes Rental Income Estimator :<br><em>how much does your property earn?</em>',
        'hero_sub': 'High-altitude resort at 2,100 m, Grande Motte glacier, Espace Killy 300 km, skiing 10 months a year. The Alpine resort with the longest season in Europe.',
        'schema_breadcrumb_name': 'Tignes Estimator',
        'alpeon_eyebrow': 'ALPÉON in Tignes',
        'alpeon_h2': 'Maximising the <em>long season</em>',
        'faq_h2': 'Everything about renting in Tignes',
        'cta_h2': 'Meet an ALPÉON advisor<br>in <em>Tignes</em>',
        'footer_owner': 'Own a property in Tignes?',
        'footer_bottom_last': 'Premium Alpine short-term rental management · Tignes · French Alps',
        'newsletter_source': 'footer-tignes-en',
        'faq_items': [
            ('How much does an apartment earn from rental in Tignes?',
             'An apartment in Tignes generates between €17,000 and €55,000 in annual rental income depending on size, location and amenities. The resort\'s high altitude guarantees exceptional snow coverage that attracts guests from October to May, maximising annual occupancy. Weekly peak season rents range from €1,400 for a small apartment to over €9,000 for a large prestige property.'),
            ('Is Tignes open for skiing all year round?',
             'Tignes generally opens in October and keeps its ski area open until May — around 10 months of skiing per year. The Grande Motte glacier (3,456 m) also allows summer skiing in June and July. This exceptional season length is a major advantage for property owners, as it significantly increases annual rental yield compared to lower-altitude resorts.'),
            ("What is the difference between Tignes and Val d'Isère for rental?",
             "Tignes and Val d'Isère share the same Espace Killy ski area (300 km) but present different market profiles. Val d'Isère attracts a more upmarket clientele and commands higher rents, especially for chalets. Tignes, with more accessible property prices, appeals to a broader international clientele and offers a longer season. For investors, Tignes offers a better rental yield thanks to its longer season and more accessible entry prices."),
            ('Is Tignes a good resort for investment and rental?',
             "Tignes has an excellent rental investment profile. The 10-month season maximises annual occupancy rates. Property prices, more accessible than Val d'Isère or Courchevel, offer better entry conditions for investors. The international clientele attracted by the glacier and the long season ensures sustained year-round demand."),
            ('Does ALPÉON offer property management in Tignes?',
             'Yes, ALPÉON manages apartments and chalets in Tignes with a strategy adapted to the long season and international clientele. We optimise rates week by week, distribute across the main ski-property platforms and ensure professional management throughout the entire season from autumn to spring.'),
        ],
        'alpeon_p1': 'Tignes\' exceptional 10-month season is a unique advantage that ALPÉON leverages fully. We manage properties across all of Tignes\' villages — Val Claret, Le Lac, Les Brévières and Les Boisses — adapting our pricing strategy to each period of the season to maximise rental income.',
        'alpeon_p2': 'Our presence throughout the long season — from the first autumn snowfalls to the May closing — means we generate rental income for your property months longer than most resorts in the Alps.',
    },
    'val-d-isere': {
        'slug': 'val-d-isere',
        'name': "Val d'Isère",
        'meta_title': "Val d'Isère Rental Income Estimator · 2025/2026 Rental Returns | ALPÉON",
        'meta_desc': "How much does your apartment or chalet in Val d'Isère earn from short-term rental? Estimate your rental income: from €20,000 to €120,000/year. World-class skiing, international clientele. Free simulation.",
        'og_title': "Val d'Isère Rental Income Estimator · 2025/2026 Rental Returns | ALPÉON",
        'og_desc': "How much does your apartment or chalet in Val d'Isère earn? From €20,000 to €120,000/year. World-class skiing, international clientele. Free simulation.",
        'hero_h1': "Val d'Isère Rental Income Estimator :<br><em>how much does your property earn?</em>",
        'hero_sub': "International prestige resort at 1,850 m, Espace Killy 300 km, FIS Alpine Ski World Cup every winter, ultra-premium global clientele. One of the world's finest ski resorts.",
        'schema_breadcrumb_name': "Val d'Isère Estimator",
        'alpeon_eyebrow': "ALPÉON in Val d'Isère",
        'alpeon_h2': '<em>Premium</em> service for an international clientele',
        'faq_h2': "Everything about renting in Val d'Isère",
        'cta_h2': "Meet an ALPÉON advisor<br>in <em>Val d'Isère</em>",
        'footer_owner': "Own a property in Val d'Isère?",
        'footer_bottom_last': "Premium Alpine short-term rental management · Val d'Isère · French Alps",
        'newsletter_source': 'footer-val-d-isere-en',
        'faq_items': [
            ("How much does an apartment earn from rental in Val d'Isère?",
             "An apartment in Val d'Isère generates between €20,000 and €65,000 in annual rental income depending on size, location and amenities. Apartments in the resort centre near the ski lifts command the highest rents. During the World Cup week in December, demand peaks and rents can be 2 to 3 times the standard seasonal rate."),
            ("What rental income for a chalet in Val d'Isère?",
             "Chalets in Val d'Isère reach between €55,000 and €120,000/year. During the World Cup week, the finest chalets command exceptional rates. The international clientele — British, Scandinavian, American and Middle Eastern — readily invests in premium accommodation, justifying rents among the highest in the French Alps."),
            ("Does the World Cup affect rents in Val d'Isère?",
             "Yes, the FIS Alpine Ski World Cup held every December in Val d'Isère generates a unique peak in rental demand. The competition week sees rates soar, with demand from fans, ski racers' entourages and media professionals from around the world. This event alone can represent a significant portion of annual rental income for well-positioned properties."),
            ("Is Val d'Isère a good resort for investment and rental?",
             "Val d'Isère is one of the best rental investment destinations in the French Alps. The resort's international reputation, its permanent media presence and the loyalty of its demanding clientele guarantee sustained demand year after year. The Espace Killy domain guarantees skiing in all snow conditions, and the resort's international profile attracts tenants from every continent."),
            ("Does ALPÉON offer property management in Val d'Isère?",
             "Yes, ALPÉON manages apartments and chalets in Val d'Isère with an approach adapted to the resort's international demands. Our multilingual team handles relationships with a global clientele, from English and Scandinavian guests to guests from the Middle East and Americas, ensuring professional management throughout the season."),
        ],
        'alpeon_p1': "In Val d'Isère, the international standard of the clientele demands irreproachable management and multilingual service. ALPÉON is present across all of the resort's neighbourhoods — from the village centre to La Daille and Le Fornet — providing premium management befitting the world-class status of this destination.",
        'alpeon_p2': "Our multilingual team manages the full guest experience, from booking in English, Scandinavian or Arabic through to professional on-site services, ensuring your property attracts and retains the most demanding international clientele.",
    },
    'val-thorens': {
        'slug': 'val-thorens',
        'name': 'Val Thorens',
        'meta_title': 'Val Thorens Rental Income Estimator · 2025/2026 Rental Returns | ALPÉON',
        'meta_desc': "How much does your apartment or chalet in Val Thorens earn from short-term rental? Estimate your rental income: from €18,000 to €90,000/year. Europe's highest ski resort. Free simulation.",
        'og_title': 'Val Thorens Rental Income Estimator · 2025/2026 Rental Returns | ALPÉON',
        'og_desc': "How much does your apartment or chalet in Val Thorens earn? From €18,000 to €90,000/year. Europe's highest ski resort. Free simulation.",
        'hero_h1': 'Val Thorens Rental Income Estimator :<br><em>how much does your property earn?</em>',
        'hero_sub': "Europe's highest resort at 2,300 m, 7-month season, guaranteed snow, the 3 Vallées domain. Discover the true rental potential of your apartment or chalet.",
        'schema_breadcrumb_name': 'Val Thorens Estimator',
        'alpeon_eyebrow': 'ALPÉON in Val Thorens',
        'alpeon_h2': 'Your rental partner at altitude',
        'faq_h2': 'Everything about renting in Val Thorens',
        'cta_h2': 'Meet an ALPÉON advisor<br>in <em>Val Thorens</em>',
        'footer_owner': 'Own a property in Val Thorens?',
        'footer_bottom_last': 'Premium Alpine short-term rental management · Val Thorens · French Alps',
        'newsletter_source': 'footer-val-thorens-en',
        'faq_items': [
            ('How much does an apartment earn from rental in Val Thorens?',
             'An apartment in Val Thorens generates between €18,000 and €58,000 in annual rental income depending on size and condition. A studio or one-bedroom apartment of 40 m² in good condition earns around €18,000/year, while a large 100 m² prestige apartment can reach €55,000/year. The exceptionally long 7-month season maximises annual occupancy rates.'),
            ('What rental income for a chalet in Val Thorens?',
             'Chalets in Val Thorens generate annual rents between €45,000 and €90,000 depending on size and amenities. A 150 m² well-finished chalet earns around €45,000/year, while a 250 m² prestige chalet can reach €75,000/year. Chalets with a sauna, spa or panoramic views command a significant premium.'),
            ('What is the rental season in Val Thorens?',
             "Val Thorens benefits from the longest rental season in the French Alps: from October to May, around 7 consecutive months. The exceptional altitude of 2,300 m guarantees natural snow from November even in mild winters. This long season is a major differentiator compared to lower-altitude resorts, significantly increasing annual rental yield."),
            ('Which residences does ALPÉON manage in Val Thorens?',
             'ALPÉON manages properties in several of Val Thorens\' most prestigious residences: Val Chavière, Cimes de Caron, Portillo, Montana and other well-located ski-in ski-out developments at the heart of the village. Our on-site team ensures professional management throughout the full season.'),
            ('Why invest in an apartment in Val Thorens?',
             "Val Thorens offers unique investment advantages: the longest season in the French Alps (7 months), guaranteed snow thanks to its 2,300 m altitude even in mild winters, and entry property prices significantly lower than Courchevel or Megève for comparable rental yields. The resort's continuous modernisation and its position at the heart of the 3 Vallées guarantee sustained long-term demand."),
        ],
        'alpeon_p1': "ALPÉON has been present in Val Thorens since the early seasons of our development. We manage apartments and chalets in the resort's most sought-after residences: Val Chavière, Cimes de Caron, Portillo, Montana and several ski-in ski-out developments at the heart of the village.",
        'alpeon_p2': "Our 7-month season presence in Val Thorens — one of the longest in the Alps — means we generate rental income for your property well beyond what standard winter-only management can achieve.",
    },
}

def rewrite_urls(content, slug):
    """Add /en/ prefix to all internal FR links, fix lang switcher."""
    # List of FR path prefixes to rewrite
    fr_paths = [
        '/accueil/', '/proprietaires/', '/estimateur/', '/destinations/',
        '/about/', '/reserver/', '/faq/', '/politique-confidentialite/',
        '/mentions-legales/', '/cgv/',
    ]
    for path in fr_paths:
        # Replace href="/path" and href='/path' — but NOT if already /en/
        content = re.sub(
            r'(href=["\'])' + re.escape(path),
            r'\1/en' + path,
            content
        )
    # Fix double /en/en/ if any
    content = content.replace('/en/en/', '/en/')
    # Fix lang switcher: set FR as non-active, EN as active
    # Pattern: href="/estimateur/SLUG/" class="active">FR  →  no active
    content = re.sub(
        r'(href="/estimateur/' + slug + r'/")\s+class="active"',
        r'\1',
        content
    )
    # EN link: href="/en/estimateur/SLUG/"  →  add active
    content = re.sub(
        r'(href="/en/estimateur/' + re.escape(slug) + r'/">)(?!\s*class="active")',
        r'\1 class="active"',
        content
    )
    return content

def fix_seo(content, st):
    slug = st['slug']
    # canonical
    content = re.sub(
        r'<link rel="canonical" href="https://alpeon\.fr/estimateur/' + slug + r'/">',
        f'<link rel="canonical" href="https://alpeon.fr/en/estimateur/{slug}/">',
        content
    )
    # hreflang — replace existing block
    old_hreflang = re.search(
        r'<link rel="alternate" hreflang="fr".*?>\s*<link rel="alternate" hreflang="x-default".*?>',
        content, re.DOTALL
    )
    new_hreflang = f'''<link rel="alternate" hreflang="fr" href="https://alpeon.fr/estimateur/{slug}/">
  <link rel="alternate" hreflang="en" href="https://alpeon.fr/en/estimateur/{slug}/">
  <link rel="alternate" hreflang="x-default" href="https://alpeon.fr/estimateur/{slug}/">'''
    if old_hreflang:
        content = content[:old_hreflang.start()] + new_hreflang + content[old_hreflang.end():]
    # meta title
    content = re.sub(r'<title>[^<]*</title>', f'<title>{st["meta_title"]}</title>', content)
    # meta description
    content = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{st["meta_desc"]}">',
        content
    )
    # og:title
    content = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{st["og_title"]}">',
        content
    )
    # og:description
    content = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{st["og_desc"]}">',
        content
    )
    # og:url
    content = re.sub(
        r'<meta property="og:url" content="[^"]*">',
        f'<meta property="og:url" content="https://alpeon.fr/en/estimateur/{slug}/">',
        content
    )
    return content

def fix_schema(content, st):
    slug = st['slug']
    name = st['name']
    # Breadcrumb items
    content = content.replace(
        f'"name": "Accueil", "item": "https://alpeon.fr/accueil/"',
        f'"name": "Home", "item": "https://alpeon.fr/en/accueil/"'
    )
    content = content.replace(
        f'"name": "Estimateur", "item": "https://alpeon.fr/estimateur/"',
        f'"name": "Estimator", "item": "https://alpeon.fr/en/estimateur/"'
    )
    # Station breadcrumb
    content = re.sub(
        r'"name": "Estimateur [^"]+", "item": "https://alpeon\.fr/estimateur/[^/]+/"',
        f'"name": "{st["schema_breadcrumb_name"]}", "item": "https://alpeon.fr/en/estimateur/{slug}/"',
        content
    )
    return content

def fix_hero(content, st):
    # h1
    content = re.sub(
        r'<h1 class="dest-hero-title">.*?</h1>',
        f'<h1 class="dest-hero-title">{st["hero_h1"]}</h1>',
        content, flags=re.DOTALL
    )
    # sub
    content = re.sub(
        r'<p class="dest-hero-sub">.*?</p>',
        f'<p class="dest-hero-sub">{st["hero_sub"]}</p>',
        content, flags=re.DOTALL
    )
    return content

def fix_alpeon_section(content, st):
    slug = st['slug']
    name = st['name']
    # eyebrow: ALPÉON à [Station]
    content = re.sub(
        r'<div class="sec-eyebrow">ALPÉON à [^<]+</div>',
        f'<div class="sec-eyebrow">{st["alpeon_eyebrow"]}</div>',
        content
    )
    # h2 of alpeon section (the one right after the ALPÉON eyebrow)
    content = re.sub(
        r'(sec-eyebrow">' + re.escape(st['alpeon_eyebrow']) + r'</div>\s*)<h2 class="sec-title">.*?</h2>',
        r'\g<1><h2 class="sec-title">' + st['alpeon_h2'] + r'</h2>',
        content, flags=re.DOTALL
    )
    # Simpler approach: replace text between sec-eyebrow ALPÉON and why-grid
    # Replace first p in why-text after ALPÉON section
    pattern = r'(sec-eyebrow">ALPÉON[^<]*</div>.*?<div class="why-text">\s*)<p>(.*?)</p>(\s*)<p>(.*?)</p>'
    replacement = (
        r'\g<1><p>' + st['alpeon_p1'].replace('\\', '\\\\') + r'</p>\g<3><p>' +
        st['alpeon_p2'].replace('\\', '\\\\') + r'</p>'
    )
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    # Card title: "[Station] en chiffres"
    content = content.replace(
        f'<div class="alpeon-card-title">{name} en chiffres</div>',
        f'<div class="alpeon-card-title">{name} in numbers</div>'
    )
    # Translate number labels
    label_map = {
        'Altitude village haut': 'Top village altitude',
        'Villages distincts': 'Distinct villages',
        'Station prestige France': "France's top prestige resort",
        'Saison locative': 'Rental season',
        'Km de pistes': 'km of pistes',
        'Domaine skiable': 'Ski area',
        "Domaine des 3 Vallées": "3 Vallées domain",
        'Résidences gérées': 'Properties managed',
        'Durée de saison': 'Season length',
        "De la demande": "Of demand",
        "Clientèle brit.": "British clientele",
        "Mois de saison": "Month season",
        "3 Vallées": "3 Vallées",
        "Les 3 Vallées": "Les 3 Vallées",
        "Villages": "Villages",
        "Résidences premium": "Premium residences",
    }
    for fr, en in label_map.items():
        content = content.replace(
            f'<div class="alpeon-num-label">{fr}</div>',
            f'<div class="alpeon-num-label">{en}</div>'
        )
    return content

def fix_faq(content, st):
    slug = st['slug']
    name = st['name']
    # FAQ section h2
    content = re.sub(
        r'(<div class="sec-eyebrow">Fréquentes</div>|<div class="sec-eyebrow">Questions fréquentes</div>)(\s*)<h2 class="sec-title">[^<]*</h2>',
        r'\1\2<h2 class="sec-title">' + st['faq_h2'] + r'</h2>',
        content, flags=re.DOTALL
    )
    # Translate all FAQ items
    faq_items = st['faq_items']
    # Find all faq-item blocks and replace them
    faq_blocks = re.findall(r'<div class="faq-item">.*?</div>\s*</div>', content, re.DOTALL)
    if len(faq_blocks) >= len(faq_items):
        for i, (q_en, a_en) in enumerate(faq_items):
            old_block = faq_blocks[i]
            new_block = f'''<div class="faq-item">
        <button class="faq-q" onclick="toggleFaq(this)" aria-expanded="false">
          {q_en}
          <span class="faq-icon"><svg viewBox="0 0 24 24"><path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></span>
        </button>
        <div class="faq-a">{a_en}</div>
      </div>'''
            content = content.replace(old_block, new_block, 1)
    return content

def fix_cta_section(content, st):
    name = st['name']
    slug = st['slug']
    # Destination CTA h2
    content = re.sub(
        r'<h2 class="dest-cta-title">Rencontrez un conseiller ALPÉON<br>à <em>[^<]*</em></h2>',
        f'<h2 class="dest-cta-title">{st["cta_h2"]}</h2>',
        content
    )
    # Estimateur button in dest-cta → EN URL
    content = re.sub(
        r'<a href="/en/estimateur/' + slug + r'/" class="btn-ghost">Lancer l\'estimateur</a>',
        f'<a href="/en/estimateur/{slug}/" class="btn-ghost">Launch the estimator</a>',
        content
    )
    return content

def fix_footer(content, st):
    name = st['name']
    slug = st['slug']
    # Owner text
    content = content.replace(
        f'<span class="footer-owner-text">Propriétaire d\'un bien à {name} ?</span>',
        f'<span class="footer-owner-text">{st["footer_owner"]}</span>'
    )
    # Footer bottom last span
    content = re.sub(
        r'<span>Gestion locative alpine premium[^<]*</span>',
        f'<span>{st["footer_bottom_last"]}</span>',
        content
    )
    # Newsletter source
    content = content.replace(
        f"source:'footer-{slug}'",
        f"source:'{st['newsletter_source']}'"
    )
    # Also handle variations like footer-courchevel, footer-megeve etc.
    return content

def fix_other_stations(content, st):
    """Change /estimateur/[slug]/ → /en/estimateur/[slug]/ in the other-stations grid."""
    # The other stations section links — all already rewritten by rewrite_urls
    # but we need to ensure the "Estimer" text is translated
    content = content.replace('>Estimer ', '>Estimate ')
    return content

def apply_universal(content):
    for fr, en in UNIVERSAL:
        content = content.replace(fr, en)
    return content

def translate_page(slug):
    st = STATIONS[slug]
    src = f'estimateur/{slug}/index.html'
    dst = f'en/estimateur/{slug}/index.html'

    with open(src, encoding='utf-8') as f:
        content = f.read()

    print(f'  [{slug}] Read {len(content)} chars')

    # 1. Universal text replacements
    content = apply_universal(content)
    print(f'  [{slug}] Applied universal replacements')

    # 2. URL rewriting
    content = rewrite_urls(content, slug)
    print(f'  [{slug}] Rewrote URLs')

    # 3. SEO (canonical, hreflang, meta tags)
    content = fix_seo(content, st)
    print(f'  [{slug}] Fixed SEO tags')

    # 4. Schema.org
    content = fix_schema(content, st)
    print(f'  [{slug}] Fixed schema')

    # 5. Hero
    content = fix_hero(content, st)
    print(f'  [{slug}] Fixed hero')

    # 6. ALPÉON section
    content = fix_alpeon_section(content, st)
    print(f'  [{slug}] Fixed ALPÉON section')

    # 7. FAQ
    content = fix_faq(content, st)
    print(f'  [{slug}] Fixed FAQ')

    # 8. CTA section
    content = fix_cta_section(content, st)
    print(f'  [{slug}] Fixed CTA')

    # 9. Footer
    content = fix_footer(content, st)
    print(f'  [{slug}] Fixed footer')

    # 10. Other stations
    content = fix_other_stations(content, st)

    # Write output
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  [{slug}] Written → {dst}')
    return dst

if __name__ == '__main__':
    os.chdir('/Users/edgarvernet/claude/alpeon')
    for slug in ['courchevel', 'megeve', 'meribel', 'tignes', 'val-d-isere', 'val-thorens']:
        print(f'\n=== Translating {slug} ===')
        try:
            translate_page(slug)
        except Exception as e:
            print(f'  ERROR: {e}')
            import traceback; traceback.print_exc()
    print('\nDone.')
