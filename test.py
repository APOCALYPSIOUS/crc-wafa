import requests
from PyPDF2 import PdfReader

# Fonction pour télécharger un PDF depuis une URL
def download_pdf_from_url(url, download_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(download_path, "wb") as file:
            file.write(response.content)
        print(f"Fichier téléchargé : {download_path}")
        return download_path
    else:
        raise Exception(f"Échec du téléchargement du PDF. Statut HTTP : {response.status_code}")

# Fonction pour rechercher un texte dans un fichier PDF
def find_text_in_pdf(pdf_path, search_text):
    reader = PdfReader(pdf_path)
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if search_text.lower() in text.lower():
            return page_number
    return None

# Script principal
def main():
    # URL publique du PDF
    pdf_url = input("Entrez l'URL du fichier PDF : ")
    local_pdf_path = "temp_downloaded_file.pdf"
    search_text = input("Entrez le texte à rechercher : ")

    # Télécharger le PDF depuis l'URL
    download_pdf_from_url(pdf_url, local_pdf_path)

    # Rechercher le texte dans le PDF
    page_number = find_text_in_pdf(local_pdf_path, search_text)

    if page_number:
        print(f"Le texte '{search_text}' a été trouvé à la page {page_number}.")
    else:
        print(f"Le texte '{search_text}' n'a pas été trouvé dans le fichier PDF.")

if __name__ == "__main__":
    main()
