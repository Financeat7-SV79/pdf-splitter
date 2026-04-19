import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import zipfile
import os
import tempfile
import io

# Page config
st.set_page_config(
    page_title="PDF Splitter",
    page_icon="📄",
    layout="centered"
)

# Custom CSS (design upgrade)
st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}

.block-container {
    max-width: 700px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Title */
h1 {
    text-align: center;
    font-weight: 700;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #555;
    margin-bottom: 30px;
}

/* Upload box */
.upload-box {
    border: 2px dashed #4CAF50;
    padding: 40px;
    border-radius: 12px;
    background-color: white;
    text-align: center;
    margin-bottom: 20px;
}

/* Buttons */
.stDownloadButton > button {
    width: 100%;
    border-radius: 8px;
    height: 45px;
    font-weight: 600;
}

/* Success box */
.stAlert {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("📄 PDF Splitter")
st.markdown('<p class="subtitle">Split je PDF in losse pagina’s — snel, veilig en gratis</p>', unsafe_allow_html=True)

# Upload UI
st.markdown('<div class="upload-box">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("📤 Sleep je PDF hier of klik om te uploaden", type=["pdf"])
st.markdown('</div>', unsafe_allow_html=True)

# Processing
if uploaded_file:
    with st.spinner("⏳ Bezig met splitsen..."):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, uploaded_file.name)

            with open(input_path, "wb") as f:
                f.write(uploaded_file.read())

            reader = PdfReader(input_path)
            base_name = os.path.splitext(uploaded_file.name)[0]

            pdf_buffers = []

            # Split PDF
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)

                pdf_buffer = io.BytesIO()
                writer.write(pdf_buffer)
                pdf_buffer.seek(0)

                filename = f"{base_name}_page_{i+1}.pdf"
                pdf_buffers.append((filename, pdf_buffer))

            # ZIP in memory
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zipf:
                for filename, buffer in pdf_buffers:
                    zipf.writestr(filename, buffer.getvalue())

            zip_buffer.seek(0)

    # Success message
    st.success(f"✅ Klaar! {len(pdf_buffers)} pagina’s gesplitst.")

    st.markdown("### ⬇️ Download je bestanden")

    # Primary CTA
    st.download_button(
        label="📦 Download alles als ZIP",
        data=zip_buffer,
        file_name=f"{base_name}_pages.zip",
        mime="application/zip"
    )

    st.markdown("---")

    # Secondary downloads
    with st.expander("📄 Of download losse pagina’s"):
        for filename, buffer in pdf_buffers:
            st.download_button(
                label=f"Download {filename}",
                data=buffer,
                file_name=filename,
                mime="application/pdf"
            )
