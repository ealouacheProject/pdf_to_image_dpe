import os
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import re

class PDFTextExtractor:
    def extract_text_from_pdf(self, pdf_path):
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
                # Définir les paramètres de mise en page minimaux
                laparams = LAParams(
                    all_texts=True,
                    detect_vertical=False,
                    line_margin=0.3,
                    char_margin=3.0,
                    word_margin=0.2,
                    boxes_flow=0.5,
                    line_overlap=0.5
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
                
                # Nettoyer le texte
                text = self.clean_text(text)
                
                # Nettoyer
                device.close()
                output_string.close()
                
                return text
        except Exception as e:
            print(f"Erreur lors de l'extraction du texte du PDF {pdf_path}: {str(e)}")
            return None

    def clean_text(self, text):
        """
        Nettoie le texte extrait en supprimant les informations inutiles.
        """
        # Supprimer les espaces en début et fin de ligne
        text = '\n'.join(line.strip() for line in text.splitlines())
        
        # Supprimer les lignes vides
        text = '\n'.join(line for line in text.splitlines() if line.strip())
        
        # Supprimer les caractères spéciaux et les formatages
        text = re.sub(r'[_*]', '', text)
        
        # Supprimer les indications de mise en page
        text = re.sub(r'p\.\d+', '', text)
        
        # Supprimer les lignes qui ne contiennent que des caractères spéciaux
        text = re.sub(r'^\W+$\n', '', text, flags=re.MULTILINE)
        
        # Supprimer les répétitions d'informations
        text = re.sub(r'(DPE diagnostic de performance énergétique \(logement\))\s*\n.*\n\1', r'\1', text, flags=re.MULTILINE)
        
        # Supprimer les lignes avec uniquement des lettres isolées
        text = re.sub(r'^\s*[A-G]\s*$\n', '', text, flags=re.MULTILINE)
        
        return text.strip()

def process_pdfs():
    """
    Traite tous les fichiers PDF dans le dossier input et sauvegarde le texte dans le dossier output.
    """
    # Créer le dossier output s'il n'existe pas
    if not os.path.exists("output"):
        os.makedirs("output")
    
    # Parcourir tous les fichiers PDF dans le dossier input
    for filename in os.listdir("input"):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join("input", filename)
            
            # Extraire le texte
            extractor = PDFTextExtractor()
            text = extractor.extract_text_from_pdf(pdf_path)
            
            if text:
                # Créer le nom du fichier de sortie
                output_filename = os.path.splitext(filename)[0] + ".txt"
                output_path = os.path.join("output", output_filename)
                
                # Écrire le texte dans le fichier
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"Texte extrait avec succès : {output_filename}")

if __name__ == "__main__":
    process_pdfs()
