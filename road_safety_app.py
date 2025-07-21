
import streamlit as st
import json
from PIL import Image, ImageDraw

# Load the JSON file
uploaded_json = st.file_uploader("Upload Azure Vision JSON output", type="json")
uploaded_image = st.file_uploader("Upload corresponding image", type=["jpg", "png"])

if uploaded_json and uploaded_image:
    data = json.load(uploaded_json)
    image = Image.open(uploaded_image)
    draw = ImageDraw.Draw(image)

    st.image(image, caption="Original Image", use_column_width=True)

    st.markdown("### Caption")
    st.write(data.get("captionResult", {}).get("text", "No caption found"))

    st.markdown("### Detected Tags")
    for tag in data.get("tagsResult", {}).get("values", []):
        st.write(f"- {tag['name']} (Confidence: {tag['confidence']:.2f})")

    st.markdown("### Highlighted Safety Items")
    for obj in data.get("objectsResult", {}).get("values", []):
        box = obj["boundingBox"]
        tag = obj["tags"][0]["name"]
        confidence = obj["tags"][0]["confidence"]
        draw.rectangle([box["x"], box["y"], box["x"] + box["w"], box["y"] + box["h"]], outline="red", width=3)
        draw.text((box["x"], box["y"] - 10), f"{tag} ({confidence:.2f})", fill="red")

    st.image(image, caption="Image with Safety Items Highlighted", use_column_width=True)

    st.markdown("### Auto Safety Tips")
    tips = {
        "helmet": "Always wear a helmet when cycling.",
        "footwear": "Wear proper footwear to avoid injury.",
        "bicycle": "Ride your bicycle with supervision in safe areas."
    }
    detected_tags = [tag["name"] for tag in data.get("tagsResult", {}).get("values", [])]
    for tag in detected_tags:
        if tag in tips:
            st.info(tips[tag])
