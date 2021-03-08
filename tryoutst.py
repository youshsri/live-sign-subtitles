import streamlit as st
import pytube
#unsafe_allow_html = True
#This mockup website displays the YT video they asked for
col1, col2, col3 = st.beta_columns(3)

with col2:
    st.image("SignVid_Logo.jpg", width = 150)
#st.title('Welcome to SignVid!')
st.markdown("<h1 style='text-align: center; color: black;'>Welcome to SignVid!</h1>", unsafe_allow_html=True)
#st.subheader('Enter a YouTube URL and we will translate it into British Sign Language')
st.markdown("<p style='text-align: center; color: black;'>Enter a YouTube URL and we will translate it into British Sign Language", unsafe_allow_html=True)


video_url = st.text_input(" ")

if video_url:
    #Run the code and return the YT video
    #Later on, this will show our video
    st.video(video_url)


about = st.sidebar.beta_expander("About us")
about.write("We are a team of students from Imperial College London who made this WebApp for our DAPP2 project")
#Let's rewrite this
contact = st.sidebar.beta_expander("Get in touch")
contact.write("For any questions or concerns, please contact us on: ...")
#Let's rewrite this
