import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="Azure Vision Analyzer", layout="wide")

st.title("🧠 Azure AI Vision - Image Intelligence App")

st.info("Upload an image and provide your Azure Vision Key and Endpoint.")

# User Input for Azure Credentials
endpoint = st.text_input("Azure Vision Endpoint (e.g. https://your-resource.cognitiveservices.azure.com/)", "")
subscription_key = st.text_input("Azure Vision Key", type="password")

features = ["tags", "read", "caption", "denseCaptions", "smartCrops", "objects", "people"]

image_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if image_file and endpoint and subscription_key:
    try:
        image_data = image_file.read()
        image = Image.open(io.BytesIO(image_data))
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Call Azure Vision API
        headers = {
            "Ocp-Apim-Subscription-Key": subscription_key,
            "Content-Type": "application/octet-stream"
        }
        params = {"features": ",".join(features), "language": "en"}
        vision_url = f"{endpoint}/computervision/imageanalysis:analyze"
        response = requests.post(vision_url, headers=headers, params=params, data=image_data)

        if response.status_code != 200:
            st.error(f"Azure API Error {response.status_code}: {response.text}")
        else:
            result = response.json()

            # Caption
            try:
                if "captionResult" in result:
                    st.subheader("📝 Caption")
                    st.write(result["captionResult"].get("text", "No caption found."))
            except Exception as e:
                st.error(f"Caption section error: {e}")

            # Tags
            try:
                if "tagsResult" in result:
                    st.subheader("🏷️ Tags")
                    for tag in result["tagsResult"]["values"]:
                        name = tag.get("name", "Unknown")
                        conf = tag.get("confidence", 0.0)
                        st.write(f"- {name} (Confidence: {conf:.2f})")
            except Exception as e:
                st.error(f"Tags section error: {e}")

            # Dense Captions
            try:
                if "denseCaptionsResult" in result:
                    st.subheader("🔍 Dense Captions")
                    for item in result["denseCaptionsResult"]["values"]:
                        st.write(f"- {item.get('text', 'No text')} (Confidence: {item.get('confidence', 0):.2f})")
            except Exception as e:
                st.error(f"Dense captions error: {e}")

            # Smart Crops
            try:
                if "smartCropsResult" in result:
                    st.subheader("📐 Smart Crops")
                    for crop in result["smartCropsResult"]["values"]:
                        st.write(f"- Aspect Ratio: {crop.get('aspectRatio')} → {crop.get('boundingBox')}")
            except Exception as e:
                st.error(f"Smart Crops error: {e}")

            # Objects
            try:
                if "objectsResult" in result:
                    st.subheader("🧱 Objects Detected")
                    for obj in result["objectsResult"]["values"]:
                        name = obj.get("name", "Unknown")
                        conf = obj.get("confidence", 0.0)
                        st.write(f"- {name} (Confidence: {conf:.2f})")
            except Exception as e:
                st.error(f"Objects section error: {e}")

            # People
            try:
                if "peopleResult" in result:
                    st.subheader("👥 People Detected")
                    people_count = len(result["peopleResult"].get("values", []))
                    st.write(f"{people_count} person{'s' if people_count != 1 else ''} detected.")
            except Exception as e:
                st.error(f"People section error: {e}")

            # Read (OCR)
            try:
                if "readResult" in result:
                    st.subheader("📖 Text Detected (OCR)")
                    for line in result["readResult"].get("blocks", []):
                        for ln in line.get("lines", []):
                            st.write(f"- {ln.get('text')}")
            except Exception as e:
                st.error(f"OCR section error: {e}")

    except Exception as e:
        st.error(f"Unexpected error: {e}")
