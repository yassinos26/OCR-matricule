import easyocr

# Initialiser le lecteur avec la langue arabe
reader = easyocr.Reader(['ar'])

# Chemin de l'image à traiter
image_path = '6.jpg'

# Lire le texte dans l'image
results = reader.readtext(image_path)

# Afficher les résultats
for (bbox, text, prob) in results:
    print(f"Texte: {text}, Confiance: {prob:.2f} , coordonee : {bbox}" )