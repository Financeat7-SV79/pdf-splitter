import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import zipfile
import os
import tempfile

# Page config
st.set_page_config(page_title="PDF Splitter", layout="centered")

# Custom styling
st.markdown("""
    <style>
    .main {
        text-align: center;
    }
    .block-container {
        padding-top: 2rem;
    }
    .upload-box {
        border: 2px dashed #4CAF50;
        padding: 30px;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📄 PDF Splitter")
st.markdown("### Split je PDF in losse pagina’s + download als ZIP")

st.markdown("---")

# Upload section
st.markdown('<div class="upload-box">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("📤 Upload je PDF bestand", type=["pdf"])
st.markdown('</div>', unsafe_allow_html=True)

# Processing
if uploaded_file:
    with st.spinner("⏳ PDF wordt gesplitst..."):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, uploaded_file.name)
            
            with open(input_path, "wb") as f:
                f.write(uploaded_file.read())

            reader = PdfReader(input_path)
            base_name = os.path.splitext(uploaded_file.name)[0]

            split_files = []

            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)

                output_filename = f"{base_name}_page_{i+1}.pdf"
                output_path = os.path.join(temp_dir, output_filename)

                with open(output_path, "wb") as f:
                    writer.write(f)

                split_files.append(output_path)

            zip_path = os.path.join(temp_dir, f"{base_name}_pages.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file in split_files:
                    zipf.write(file, os.path.basename(file))

    st.success(f"✅ Klaar! {len(split_files)} pagina’s gesplitst.")

    st.markdown("### ⬇️ Download je bestanden")

    # ZIP download
    with open(zip_path, "rb") as f:
        zip_bytes = f.read()

    st.download_button(
        label="📦 Download alles als ZIP",
        data=zip_bytes,
        file_name=f"{base_name}_pages.zip",
        mime="application/zip"
    )

    st.markdown("---")

    # Individual files
    st.markdown("### 📄 Of download losse pagina’s")
    for file_path in split_files:
        with open(file_path, "rb") as f:
            st.download_button(
                label=f"Download {os.path.basename(file_path)}",
                data=f,
                file_name=os.path.basename(file_path),
                mime="application/pdf"
            )
