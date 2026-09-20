import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.markdown("Generate tailored posts, captions, and articles in seconds.")

# 2. Sidebar for API Key
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Groq API Key", type="password", help="Get this from console.groq.com")
    st.markdown("[Get your free Groq API key here](https://console.groq.com/keys)")

# 3. User Inputs
col1, col2 = st.columns(2)

with col1:
    platform = st.selectbox("Platform", ["LinkedIn", "Twitter / X", "Instagram", "Facebook", "Blog"])
    content_type = st.selectbox("Content Type", ["Post", "Article", "Thread", "Caption"])

with col2:
    tone = st.selectbox("Tone", ["Professional", "Casual", "Humorous", "Inspirational", "Persuasive"])
    target_audience = st.text_input("Target Audience", placeholder="e.g., Tech Startup Founders")

topic = st.text_area("Topic / Main Idea", placeholder="e.g., How AI is transforming remote work...")

# 4. Content Generation
if st.button("Generate Content ✨"):
    if not api_key:
        st.error("⚠️ Please enter your Groq API Key in the sidebar.")
    elif not topic:
        st.warning("⚠️ Please enter a topic to generate content.")
    else:
        try:
            # Initialize the Groq client
            client = Groq(api_key=api_key)
            
            # Construct the prompt
            prompt = f"""
            You are an expert social media manager and content creator. 
            Create a highly engaging {content_type} for {platform}.
            
            Topic: {topic}
            Target Audience: {target_audience}
            Tone: {tone}
            
            Include relevant hashtags and emojis. Ensure the formatting suits {platform}. Output ONLY the final content, no conversational filler.
            """
            
            with st.spinner("Generating your content..."):
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a professional content creator."},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.3-70b-versatile", # Groq's fast Llama 3.3 model
                    temperature=0.7,
                )
                
                generated_content = response.choices[0].message.content
                
                st.success("Content Generated!")
                st.write(generated_content)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
