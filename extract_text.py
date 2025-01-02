import os
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def extract_text_from_pdf(pdf_path):
    """
    Extrait le texte d'un fichier PDF en utilisant PDFMiner.
    """
    try:
        # Ouvrir le fichier PDF en mode binaire
        with open(pdf_path, 'rb') as file:
            # Créer un parseur PDF
            parser = PDFParser(file)
            # Créer un document PDF
            doc = PDFDocument(parser)
            # Vérifier si le document est extractible
            if not doc.is_extractable:
                raise Exception("Le document PDF n'est pas extractible")
            
            # Créer un gestionnaire de ressources
            rsrcmgr = PDFResourceManager()
            # Créer un buffer pour stocker le texte
            output_string = StringIO()
            # Définir les paramètres de mise en page
            laparams = LAParams(
                line_margin=0.5,         # Marge entre les lignes
                word_margin=0.1,         # Marge entre les mots
                char_margin=2.0,         # Marge entre les caractères
                boxes_flow=0.5,          # Contrôle le flux des boîtes de texte
                detect_vertical=True,    # Détecte le texte vertical
                all_texts=True,          # Extrait tout le texte, même décoratif
                line_overlap=0.5,        # Contrôle la superposition des lignes
            )
            
            # Créer un convertisseur de texte
            device = TextConverter(rsrcmgr, output_string, laparams=laparams)
            # Créer un interpréteur
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            
            # Traiter chaque page
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
            
            # Récupérer le texte
            text = output_string.getvalue()
            
            # Nettoyer
            device.close()
            output_string.close()
            
            return text
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte du PDF {pdf_path}: {str(e)}")
        return None

def process_pdfs():
    """
    Traite tous les fichiers PDF dans le dossier input et sauvegarde le texte dans le dossier output.
    """
    # Vérifier si le dossier input existe
    if not os.path.exists("input"):
        print("Le dossier 'input' n'existe pas.")
        return

    # Créer le dossier output s'il n'existe pas
    os.makedirs("output", exist_ok=True)

    # Parcourir tous les fichiers dans le dossier input
    for filename in os.listdir("input"):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join("input", filename)
            
            # Extraire le texte
            text = extract_text_from_pdf(pdf_path)
            
            if text:
                # Créer le nom du fichier de sortie
                output_filename = os.path.splitext(filename)[0] + ".txt"
                output_path = os.path.join("output", output_filename)
                
                # Sauvegarder le texte dans un fichier
                try:
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(text)
                    print(f"Texte extrait avec succès : {output_filename}")
                except Exception as e:
                    print(f"Erreur lors de la sauvegarde du fichier {output_filename}: {str(e)}")
            else:
                print(f"Impossible d'extraire le texte de {filename}")

if __name__ == "__main__":
    process_pdfs()
