import streamlit as st
import reddit_util
from transformers import pipeline

@st.cache_resource
def load_pipeline():
    return pipeline("summarization")

summarizer = load_pipeline()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Provide subreddit name to get latest posts"):
    if prompt.startswith("r/"):
        subreddit_name = prompt[2:]
    else:
        subreddit_name = prompt
        prompt = f"r/{subreddit_name}"
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    posts = reddit_util.get_subreddit_content(subreddit_name)

    if not posts:
        with st.chat_message("assistant"):
            st.markdown("No posts found or an error occurred.")
        st.session_state.messages.append({"role": "assistant", "content": "No posts found or an error occurred."})
    else:
        articles = [f"TITLE:{post['title'].strip()}\nCONTENT:{post['selftext'].strip()}\n\n" for post in posts if post['selftext'].strip()]
        if not articles:
            with st.chat_message("assistant"):
                st.markdown("No valid posts found.")
            st.session_state.messages.append({"role": "assistant", "content": "No valid posts found."})
            st.stop()

        summaries = []
        for article in articles:
            text = summarizer(
                article,
                max_length=min(100, len(article) // 2),
                min_length=10,
                do_sample=False
            )
            
            summaries.append(text[0]["summary_text"])
            print(text[0]["summary_text"])
    
        text = summarizer(
            "".join(summaries),
            max_length=100,
            min_length=30,
            do_sample=False
        )


        with st.chat_message("assistant"):
            st.markdown(str(text[0]["summary_text"]))
            st.session_state.messages.append({"role": "assistant", "content": str(text[0]["summary_text"])})

