import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import zipfile
import os
import tempfile
import io

st.set_page_config(page_title="PDF Splitter", layout="centered")

st.title("📄 PDF Splitter")
st.write("Upload een PDF en download losse pagina’s + ZIP bestand.")
st.markdown("---")

uploaded_file = st.file_uploader("Upload je PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("⏳ PDF wordt gesplitst..."):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, uploaded_file.name)

            with open(input_path, "wb") as f:
                f.write(uploaded_file.read())

            reader = PdfReader(input_path)
            base_name = os.path.splitext(uploaded_file.name)[0]

            pdf_buffers = []  # 👈 hier slaan we alles in geheugen op

            # Split PDF
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)

                pdf_buffer = io.BytesIO()
                writer.write(pdf_buffer)
                pdf_buffer.seek(0)

                filename = f"{base_name}_page_{i+1}.pdf"
                pdf_buffers.append((filename, pdf_buffer))

            # ZIP maken in geheugen
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zipf:
                for filename, buffer in pdf_buffers:
                    zipf.writestr(filename, buffer.getvalue())

            zip_buffer.seek(0)

    st.success(f"✅ Klaar! {len(pdf_buffers)} pagina’s gesplitst.")

    # ZIP download
    st.download_button(
        label="📦 Download alles als ZIP",
        data=zip_buffer,
        file_name=f"{base_name}_pages.zip",
        mime="application/zip"
    )

    st.markdown("---")
    st.markdown("### 📄 Download losse pagina’s")

    # Individuele downloads (nu uit geheugen)
    for filename, buffer in pdf_buffers:
        st.download_button(
            label=f"Download {filename}",
            data=buffer,
            file_name=filename,
            mime="application/pdf"
        )
