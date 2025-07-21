
import streamlit as st
import requests
from PIL import Image, ImageDraw
import io

st.set_page_config(page_title="Full Azure Vision Analyzer", layout="centered")
st.title("🧠 Azure Vision AI – Full Feature Analyzer")

uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Azure credentials
AZURE_KEY = "397PyLBxU2mqZ6vBZBa9jNy3WRCR3S4LdE3j6NgnpbR7w8stGv3MJQQJ99BGACYeBjFXJ3w3AAAFACOGUWrm"
AZURE_ENDPOINT = "https://desmondvision1962.cognitiveservices.azure.com/"
VISION_URL = AZURE_ENDPOINT + "computervision/imageanalysis:analyze?api-version=2023-10-01&features=tags,read,caption,denseCaptions,smartCrops,objects,people"

if uploaded_image:
    image_bytes = uploaded_image.read()

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/octet-stream"
    }

    with st.spinner("Analyzing image with Azure Vision API..."):
        response = requests.post(VISION_URL, headers=headers, data=image_bytes)
        result = response.json()

    # Show caption
    st.subheader("Caption")
    st.write(result.get("captionResult", {}).get("text", "No caption detected."))

    # Dense Captions
    st.subheader("Dense Captions")
    for cap in result.get("denseCaptionsResult", {}).get("values", []):
        st.write(f"- {cap['text']} (Confidence: {round(cap['confidence'], 2)})")

    # Tags
    st.subheader("Detected Tags")
    for tag in result.get("tagsResult", {}).get("values", []):
        st.write(f"- {tag['name']} (Confidence: {round(tag['confidence'], 2)})")

    # Read (OCR)
    st.subheader("Detected Text (OCR)")
    lines = result.get("readResult", {}).get("blocks", [])
    if lines:
        for block in lines:
            for line in block.get("lines", []):
                st.markdown(f"> {line['text']}")
    else:
        st.write("No text detected.")

    # Smart Crops
    st.subheader("Suggested Smart Crop Areas")
    for crop in result.get("smartCropsResult", {}).get("values", []):
        st.write(f"- Aspect ratio {crop['aspectRatio']} with crop box: {crop['boundingBox']}")

    # Load image
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    draw = ImageDraw.Draw(image)

    # Draw object bounding boxes
    st.subheader("Detected Objects")
    objects = result.get("objectsResult", {}).get("values", [])
    for obj in objects:
        tag = obj["tags"][0]["name"]
        box = obj["boundingBox"]
        draw.rectangle(
            [box["x"], box["y"], box["x"] + box["w"], box["y"] + box["h"]],
            outline="red", width=3
        )
        draw.text((box["x"], box["y"] - 10), f"{tag}", fill="red")

    # Draw people
    st.subheader("Detected People")
    for person in result.get("peopleResult", {}).get("values", []):
        box = person["boundingBox"]
        draw.rectangle(
            [box["x"], box["y"], box["x"] + box["w"], box["y"] + box["h"]],
            outline="blue", width=3
        )
        draw.text((box["x"], box["y"] - 10), "Person", fill="blue")

    st.image(image, caption="Annotated Image")
