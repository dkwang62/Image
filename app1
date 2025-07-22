import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(layout="wide")
st.title("🔍 Azure Vision API Image Analyzer")

# --- User Inputs: Key and Endpoint ---
st.sidebar.header("🔐 Azure Credentials")
api_key = st.sidebar.text_input("Enter your Azure Vision API Key", type="password")
endpoint = st.sidebar.text_input("Enter your Azure Endpoint (e.g. https://xxx.cognitiveservices.azure.com)")

features = [
    "tags",
    "read",
    "caption",
    "denseCaptions",
    "smartCrops",
    "objects",
    "people"
]

# --- Image Upload ---
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file and api_key and endpoint:
    # Load image
    image_bytes = uploaded_file.read()
    image = Image.open(io.BytesIO(image_bytes))
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # --- API Call ---
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/octet-stream"
    }

    params = {
        "features": ",".join(features),
        "language": "en"
    }

    try:
        with st.spinner("Analyzing image using Azure Vision API..."):
            response = requests.post(
                f"{endpoint}/computervision/imageanalysis:analyze?api-version=2023-10-01",
                headers=headers,
                params=params,
                data=image_bytes
            )
            response.raise_for_status()
            result = response.json()

        st.success("Image analyzed successfully!")

        # --- Display Results ---
        if "captionResult" in result and "text" in result["captionResult"]:
            st.subheader("📝 Caption")
            st.write(result["captionResult"]["text"])

        if "tagsResult" in result:
            st.subheader("🏷️ Detected Tags")
            for tag in result["tagsResult"]["values"]:
                st.markdown(f"- {tag['name']} (Confidence: {tag['confidence']:.2f})")

        if "readResult" in result and "blocks" in result["readResult"]:
            st.subheader("📄 Text Read")
            for block in result["readResult"]["blocks"]:
                st.write(block["text"])

        if "denseCaptionsResult" in result:
            st.subheader("🪄 Dense Captions")
            for item in result["denseCaptionsResult"]["values"]:
                st.write(f"• {item['text']}")

        if "objectsResult" in result:
            st.subheader("🧱 Objects Detected")
            for obj in result["objectsResult"]["values"]:
                st.write(f"- {obj['name']} (Confidence: {obj['confidence']:.2f})")

        if "peopleResult" in result:
            st.subheader("🧍 People Detected")
            people = result["peopleResult"]["values"]
            st.write(f"Detected {len(people)} person(s).")

    except Exception as e:
        st.error(f"❌ Error: {e}")

elif uploaded_file:
    st.warning("Please enter your Azure Vision API key and endpoint in the sidebar.")
