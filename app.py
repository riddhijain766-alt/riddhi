!pip install pandas openai streamlit PyPDF2 plotly

import requests

# Publicly available Reliance annual report
url = "https://www.ril.com/ar2023-24/pdf/consolidated.pdf"
with open("reliance_consolidated.pdf", "wb") as f:
    f.write(requests.get(url).content)


import streamlit as st

users = {
    "analyst": "analystpw",
    "ceo_jio": "jio123",
    "ceo_retail": "retail123",
    "ambani_family": "ambani123"
}

def login():
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        if username in users and users[username] == password:
            st.session_state['user'] = username
            st.success('Logged in!')
        else:
            st.error('Invalid credentials.')
    return st.session_state.get('user')

user = login()
if not user:
    st.stop()


def get_user_companies(user):
    if user == "ambani_family":
        return ["Reliance Jio", "Reliance Retail", "Reliance Industries"]
    elif user == "ceo_jio":
        return ["Reliance Jio"]
    elif user == "ceo_retail":
        return ["Reliance Retail"]
    else:
        return ["Reliance Industries"]
    
def plot_metrics(df):
    import plotly.express as px
    st.subheader("Key Metrics Over Years")
    fig = px.line(df, x='Year', y=['Revenue', 'Assets', 'Liabilities'])
    st.plotly_chart(fig)

import openai

openai.api_key = "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"

def ask_gpt(question, context):
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer:",
        temperature=0,
        max_tokens=200
    )
    return response.choices[0].text.strip()

with st.form("question_form"):
    user_query = st.text_input("Ask about the company's performance")
    submit = st.form_submit_button("Ask GPT")
    if submit:
        context = balance_sheet_df.to_string()
        answer = ask_gpt(user_query, context)
        st.write("GPT says:", answer)

