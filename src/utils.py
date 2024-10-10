
import os
import glob

def remove_existing_pdfs(directory='./'):
    """Remove all PDF files in the specified directory."""
    pdf_files = glob.glob(f'{directory}/*.pdf')
    for pdf_file in pdf_files:
        try:
            os.remove(pdf_file)
            print(f"Deleted: {pdf_file}")
        except Exception as e:
            print(f"Failed to delete {pdf_file}: {e}")
