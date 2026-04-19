import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import zipfile
import os
import tempfile

st.set_page_config(page_title="PDF Splitter", layout="centered")

st.title("📄 PDF Splitter")
st.write("Upload een PDF en download losse pagina’s + ZIP bestand.")

uploaded_file = st.file_uploader("Upload je PDF", type=["pdf"])

if uploaded_file:
    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = os.path.join(temp_dir, uploaded_file.name)
        
        # Save uploaded file
        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())

        reader = PdfReader(input_path)
        base_name = os.path.splitext(uploaded_file.name)[0]

        split_files = []

        # Split PDF
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)

            output_filename = f"{base_name}_page_{i+1}.pdf"
            output_path = os.path.join(temp_dir, output_filename)

            with open(output_path, "wb") as f:
                writer.write(f)

            split_files.append(output_path)

        # Create ZIP
        zip_path = os.path.join(temp_dir, f"{base_name}_pages.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in split_files:
                zipf.write(file, os.path.basename(file))

        st.success(f"PDF gesplitst in {len(split_files)} pagina's.")

        # Download ZIP
        with open(zip_path, "rb") as f:
            st.download_button(
                label="⬇️ Download ZIP",
                data=f,
                file_name=f"{base_name}_pages.zip",
                mime="application/zip"
            )

        # Individual downloads
        st.subheader("Losse pagina’s downloaden")
        for file_path in split_files:
            with open(file_path, "rb") as f:
                st.download_button(
                    label=f"Download {os.path.basename(file_path)}",
                    data=f,
                    file_name=os.path.basename(file_path),
                    mime="application/pdf"
                )