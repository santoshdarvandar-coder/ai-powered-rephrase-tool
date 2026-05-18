import streamlit as st
import requests
import json

# -----------------------------------
# API Gateway URL
# -----------------------------------
API_URL = "https://xtuhozvl6h.execute-api.ap-southeast-2.amazonaws.com/dev/rephrase"

# -----------------------------
# Page Title
# -----------------------------
st.title("Paraphrase Sentence")

# -----------------------------
# Language Selection
# -----------------------------
language = st.selectbox(
    "Language",
    ["English", "Spanish", "French", "Hindi", "Marathi", "Kannada", "Telugu", "Tamil", "German"]
)

# -----------------------------
# Input Text Area
# -----------------------------
input_text = st.text_area(
    "Enter text",
    placeholder="e.g. Your text goes here ...",
    height=200,
    max_chars=2048
)

# -----------------------------
# Layout
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    tone = st.selectbox(
        "Writing tone",
        [
            "Formal",
            "Friendly",
            "Casual",
            "Professional",
            "Academic",
            "Simplified",
            "Funny",
            "Romantic",
            "Shorten",
            "Creative"
        ]
    )

with col2:
    variants = st.selectbox(
        "Variants",
        [1,2,3,4,5]
    )

# -----------------------------
# Submit Button
# -----------------------------
paraphrase_clicked = st.button("Paraphrase")

# -------------------------------------------------
# RESPONSE SECTION
# -------------------------------------------------
if paraphrase_clicked:

    if input_text.strip() == "":
        st.warning("Please enter text.")

    else:

        st.divider()

        # Character and word count
        char_count = len(input_text)
        word_count = len(input_text.split())

        st.caption(
            f"{char_count} characters · "
            f"{word_count} words · "
            f"{tone} · "
            f"{language}"
        )

        # -----------------------------------
        # Request Payload
        # -----------------------------------
        payload = {
            "language": language,
            "tone": tone,
            "variants": variants,
            "text": input_text
        }

        try:

            with st.spinner("Generating paraphrases..."):

                response = requests.post(
                    API_URL,
                    headers={
                        "Content-Type": "application/json"
                    },
                    data=json.dumps(payload),
                    timeout=60
                )

                response.raise_for_status()

                result = response.json()

                # -----------------------------------
                # Expected Response Format
                # {
                #   "results": [
                #       "paraphrase 1",
                #       "paraphrase 2"
                #   ]
                # }
                # -----------------------------------

                paraphrases = result.get("results", [])

                if not paraphrases:
                    st.error("No paraphrases returned from API.")

                else:

                    for i, text in enumerate(paraphrases):

                        st.text_area(
                            label=f"Rephrase Output {i+1}",
                            value=text,
                            height=180
                        )

        except requests.exceptions.RequestException as e:
            st.error(f"API Request Failed: {str(e)}")

        except Exception as e:
            st.error(f"Unexpected Error: {str(e)}")