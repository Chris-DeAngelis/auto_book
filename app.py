#Inspiration: https://github.com/prateekralhan/Streamlit-ChatGPT-DALLE-2
import openai
import streamlit as st

# Authenticate API Key
openai.api_key = st.secrets["api_secret"]

# Build page
st.set_page_config(
    page_title="ChatGPT + DALL-E 2",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/topherdea/auto_book',
        'About': "# Chris DeAngelis, CFA | topherdea@gmail.com | https://www.linkedin.com/in/chris-deangelis-cfa-4019a914/"
    }
)

@st.cache_data(persist=True,show_spinner=False)#,suppress_st_warning=True), allow_output_mutation=False,
def openai_completion(prompt):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      max_tokens=2400,
      temperature=0.9
    )
    return response['choices'][0]['text']

@st.cache_data(persist=True,show_spinner=False)#,suppress_st_warning=True), allow_output_mutation=False,
def openai_image(prompt):
    response = openai.Image.create(
      prompt=prompt,
      n=1,
      size="256x256"
    )
    image_url = response['data'][0]['url']
    return image_url

# Title
st.markdown("<h1><center><strong>Write a Children's Book with ChatGPT | DALL·E</strong></center></h1>", unsafe_allow_html=True)

#st.title("Write...")
#st.markdown("-----")
#st.title(":book::dragon::bear::whale::camel::tiger:")
#st.markdown("-----")

# Input text
input_text = st.text_area("Write and illustrate a book for toddlers that is about...", "", height=100)
columns = st.columns((1, 1, 1)) # Centering button
chat_button = columns[1].button(":open_book:✨ Create Book ✨:open_book:")
chat_pages = []
image_list = []
chat_response = ""

# Execute API calls for ChatGPT and Dalle
pretext = "Write me a children's story for kids aged 3-8 that's about "
posttext = ". Be imaginative, creative, and include a life lesson. Describe characters' appearence in detail"
image_disclaimer = "illustrate like a children’s book. It should be very bright, bold, colorful, and vibrant. Preferably fantastical and epic. Using vector illustrations. "
if chat_button and input_text.strip() != "":
    with st.spinner("Loading..."):
            chat_response = openai_completion(pretext + input_text + posttext)
            #st.success(chat_response)
            chat_pages = chat_response.splitlines()
            while("" in chat_pages):
                chat_pages.remove("")
            for i in range(0, len(chat_pages)):    
                image_list.append(openai_image(image_disclaimer + chat_pages[i]))

                
# Output results to page
#col1, col2 = st.columns(2)
if chat_response:
    for i in range(0, len(chat_pages)):
        #with col1:
                #st.write(chat_pages[i])
        #with col2:
                st.image(image_list[i], caption=chat_pages[i], width=400)#, use_column_width='always')              
             


st.markdown("<br><hr><center>❤️ <a href='mailto:topherdea@gmail.com?subject=GPT | DALL·E Childrens Book?&body=Please let me know what you think of the app!'><strong>Chris DeAngelis</strong></a></center><hr>", unsafe_allow_html=True)
