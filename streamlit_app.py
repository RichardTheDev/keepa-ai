import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import re


# Function to process the input text and get the ASIN
def extract_asin(question):
    asin = re.search(r'\b[A-Z0-9]{10}\b', question)
    if asin:
        return asin.group(0)
    return None


# Function to get the image from the Keepa API
def get_keepa_image(asin):
    url = f"https://api.keepa.com/graphimage?key=2tdbbivnlmp7bgq6vbm33hu48k8m2v22uii8udr0hbtjlp5cc1rkgpskgv6g45bd&domain=1&asin={asin}"
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    return None


# Streamlit application
def main():
    st.title("ASIN Image Fetcher")

    question = st.text_input("Ask your question:")

    if st.button("Submit"):
        asin = extract_asin(question)
        if asin:
            st.write(f"Extracted ASIN: {asin}")
            image = get_keepa_image(asin)
            if image:
                st.image(image, caption='Keepa Graph Image')
            else:
                st.write("Failed to retrieve image from Keepa API.")
        else:
            st.write("No valid ASIN found in the question. Please make sure to include a 10-character ASIN.")


if __name__ == "__main__":
    main()
