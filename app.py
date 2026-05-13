# app.py

import streamlit as st
from PIL import Image, ImageOps, ImageFilter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import tempfile
import os

st.set_page_config(page_title="Document Scanner", page_icon="📄")

st.title("📄 Adobe Scan Style Document Scanner")
st.write("Upload a document image, convert it to black & white, and download it as PDF.")

uploaded_file = st.file_uploader(
    "Upload Document Image",
    type=["png", "jpg", "jpeg"]
)

def process_document(image):
    """
    Convert image into scanned black & white style
    """
    
    # Convert to grayscale
    gray = ImageOps.grayscale(image)

    # Increase sharpness
    gray = gray.filter(ImageFilter.SHARPEN)

    # Convert to pure black & white
    threshold = 150
    bw = gray.point(lambda x: 255 if x > threshold else 0, mode='1')

    return bw.convert("RGB")

def create_pdf(image):
    """
    Convert PIL image to PDF
    """
    
    pdf_buffer = BytesIO()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        image.save(tmp.name, format="JPEG")

        c = canvas.Canvas(pdf_buffer, pagesize=letter)

        page_width, page_height = letter

        # Fit image properly on page
        c.drawImage(
            tmp.name,
            20,
            20,
            width=page_width - 40,
            height=page_height - 40,
            preserveAspectRatio=True
        )

        c.showPage()
        c.save()

    os.unlink(tmp.name)

    pdf_buffer.seek(0)
    return pdf_buffer

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    if st.button("Convert to Scan PDF"):

        scanned_image = process_document(image)

        st.subheader("Scanned Black & White Image")
        st.image(scanned_image, use_container_width=True)

        pdf_file = create_pdf(scanned_image)

        st.download_button(
            label="⬇ Download PDF",
            data=pdf_file,
            file_name="scanned_document.pdf",
            mime="application/pdf"
        )
