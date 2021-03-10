import streamlit as st
import v3_1 as sign 

#unsafe_allow_html = True
#This mockup website displays the YT video they asked for
col1, col2, col3 = st.beta_columns(3)

with col2:
    st.image("SignVidLogo.jpg", width = 150)
#st.title('Welcome to SignVid!')
st.markdown("<h1 style='text-align: center; color: black;'>Welcome to SignVid!</h1>", unsafe_allow_html=True)
#st.subheader('Enter a YouTube URL and we will translate it into British Sign Language')
st.markdown("<p style='text-align: center; color: black;'>Enter a YouTube URL and we will translate it into British Sign Language", unsafe_allow_html=True)

# video_url = st.text_input("Enter text here")

video_file_name = st.text_input(" ")

# check if file is local to directory or url link to YouTube
if video_file_name:

    sign.main(video_file_name)

    video_file = open("video_with_signs.mp4", 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

# allow for the upload of video files in mp4 format
message = "Please upload a file in .mp4 format."
uploaded_file = st.file_uploader(message, type=['mp4'])

# check if uploaded file exists
if uploaded_file:
    
    # if it does, read its byte data and use streamlit to access the video
    bytes_data = uploaded_file.read()
    st.video(bytes_data)

about = st.sidebar.beta_expander("About us")
about.write("We are a team of students from Imperial College London who made this WebApp for our DAPP2 project")
#Let's rewrite this
contact = st.sidebar.beta_expander("Get in touch")
contact.write("For any questions or concerns, please contact us on: ...")
#Let's rewrite this
