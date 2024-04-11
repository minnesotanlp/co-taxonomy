import streamlit as st
from PIL import Image

import openai
# openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = st.secrets["OPENAI_API_KEY"]

def start_instruction():

    """
    Input: participant, role, writing task, writing content (prompt)
    -> Generate GPT-4 original text, and participants will revise the text
    -> Store them as a json (original, revision, change)
    """

    if 'gpt4_done' not in st.session_state:
        st.session_state.gpt4_done = False

    ### Instruction on the top page
    st.markdown("Thank you for participating in our research. Please read the instruction carefully, and follow them accordingly. Please contact at Minhwa Lee (lee03533@umn.edu) if you face any problem or seek help.")
    instruction_text = """ 
    <h2> Welcome! </h2>
    <br>
    The objective of this study is to examine the writing behaviors and strategy for different groups of people on several topics. 
    Here are the detailed instructions:
    <ol>
        <li> Go to <b>Revise GPT-4 Texts</b>, where you will revise a GPT-4 generated writing template. Please follow the instruction there. 
        <li> Navigate to the page <b> Review Your Edits </b> on the left sidebar. You will see a visualization of edits with the original text. 
        <li> Then, go to <b> Annotate Your Edits </b> to annotate your edits. Please read and follow the instruction carefully.
    </ol>
    <br>
    <p> <span style="color:red"> WARNING : </span> Please follow each of steps in the instructions responsibly. Your response will be manually reviewed for the approval. 
    <br><br>
    """
    st.markdown(instruction_text, unsafe_allow_html=True)
    st.markdown(""" <h2> Instructions </h2> """, unsafe_allow_html=True)

    post_instruction_images()



def post_instruction_images():

    img_1 = Image.open('../Instructions/1.png')
    img_2 = Image.open('../Instructions/2.png')
    img_3 = Image.open('../Instructions/3.png')
    img_4 = Image.open('../Instructions/4.png')
    img_5 = Image.open('../Instructions/5.png')
    img_6 = Image.open('../Instructions/6.png')

    
    st.markdown(" <h3> 1. Revise GPT-4 Texts </h3>", unsafe_allow_html=True)
    st.image(img_1)
    st.image(img_2)
    st.image(img_3)
    
    st.markdown("<hr><h3> 2. Review Your Edits </h3>", unsafe_allow_html=True)
    st.image(img_4)

    st.markdown("<hr><h3> 3. Annotate Your Edits </h3>", unsafe_allow_html=True)
    st.image(img_5)
    st.image(img_6)

    st.markdown("<hr><h5> If you are ready, please first navigate to the page 'Revise GPT-4 Texts.'</h5>", unsafe_allow_html=True)

        
def main():
    st.set_page_config(page_title="Make Your Revision on GPT-4 Generated Writing Template!", 
                       page_icon="📝")
    
    start_instruction()

if __name__ == '__main__':
    main() 