import streamlit as st
import json
from collections import defaultdict
import json
import re
import boto3
import os
from bs4 import BeautifulSoup

# def split_html_into_sentences(html_text):
#     # Replace <br><br> with a unique delimiter
#     html_text = html_text.replace('<br><br>', '__BR__')

#     # Split content into sentences
#     sentences = re.split(r'(?<=[.!?])|(?<=__BR__)', html_text)

#     # Filter and clean sentences
#     html_sentences = []
#     for sentence in sentences:
#         sentence = sentence.strip()
#         if sentence and '<' in sentence and '>' in sentence:  # Check for HTML tags
#             # Clean up sentence to remove the unique delimiter
#             sentence = sentence.replace('__BR__', '').strip()
#             html_sentences.append(sentence)

#     return html_sentences


def split_html_into_sentences(html_text):
    text = html_text.split('<br><br>')
    split_lst = []
    # Regular expression pattern to match sentences containing <s> or <span> tags
    pattern = r'[^.!]*<s[^>]*>.*?</s>[^.!]*[.!]|[^.!]*<span[^>]*>.*?</span>[^.!]*[.!]'

    # Find all matches in the text and return them as a list
    for parag in text:
        print(parag)
        matches = re.findall(pattern, parag)
        if matches:
            split_lst.extend(matches)
        
    return split_lst


class StKeys:
    QUERY_POOL = []
    CUR_QUERY_ID = -1
    ANNOTATION_TARGETS = ""

class RevisionAnnotation():
    def __init__(self) -> None:

        if 'is_annotation' not in st.session_state:
            st.session_state.is_annotation = False

        # Create annotation key to st.session_state
        if 'sent_annotation' not in st.session_state:
            st.session_state.sent_annotation = json.loads(st.session_state.differences_json)
        
        self.is_done = False
        self._get_sentences() 
        self._select_annotation_targets()
        self.show_annotation_targets()

    @property
    def cur_query_id(self):
        if StKeys.CUR_QUERY_ID not in st.session_state:
            st.session_state[StKeys.CUR_QUERY_ID] = 0
        return st.session_state[StKeys.CUR_QUERY_ID]
    
    @cur_query_id.setter
    def cur_query_id(self, id):
        st.session_state[StKeys.CUR_QUERY_ID] = id

    @property
    def annotation_targets(self):
        if StKeys.ANNOTATION_TARGETS not in st.session_state:
            st.session_state[StKeys.ANNOTATION_TARGETS] = []
        return st.session_state[StKeys.ANNOTATION_TARGETS]    

    @annotation_targets.setter
    def annotation_targets(self, targets):
        st.session_state[StKeys.ANNOTATION_TARGETS] = targets

    @property
    def query_pool(self):
        if StKeys.QUERY_POOL not in st.session_state:
            st.session_state[StKeys.QUERY_POOL] = []

        return st.session_state[StKeys.QUERY_POOL]

    @query_pool.setter
    def query_pool(self, queries):
        st.session_state[StKeys.QUERY_POOL] = queries

    def _get_sentences(self): # returns only edited sentences -> send to annotation_targets
        self.query_pool = split_html_into_sentences(st.session_state.visual_edit) # here, this visual_edit is the revision with the last iteration.

    def _select_annotation_targets(self):
        if self.cur_query_id >= len(self.query_pool):
            self.is_done = True 
        else:
            cur_query = self.query_pool[self.cur_query_id]
            self.annotation_targets = cur_query 

    def show_annotation_targets(self):
        if not self.is_done:
            if len(self.annotation_targets) == 0:
                self._select_annotation_targets()
                self.cur_query_id += 1 
            

            # Sentence & Intention Input
            st.markdown(f"<h3> Sentence </h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='border: 2px solid blue; padding: 10px; width: auto; height: auto; max-width: 100%; word-wrap: break-word; overflow: auto;'>{self.annotation_targets}</div>", unsafe_allow_html=True)
            st.markdown(f"""
                        <br>
                        <mark>Note: The removed span of texts in the original text were <u>crossed out</u>, while newly added edits from you are colored in <b style="color:red">red</b>. </mark>
                        <br>""", unsafe_allow_html=True)
            # Intention text box
            st.markdown(f"<br>", unsafe_allow_html=True)
            edit_intention = st.text_area("Give Your Reasons Behind those Edits in Standard English (If you don't see any edits, then write N/A .)", 
                                                height=100, max_chars=700, 
                                                placeholder="e.g., I want the sentence to sound more catchy to customer.")
                

            label_annotations = defaultdict(bool)

            form = st.form("checkboxes", clear_on_submit=True)
            with form:                    
                # Intention checkbox
                fluency = st.checkbox("**Fluency** (e.g., Fix grammatical errors)")
                coherency = st.checkbox("**Coherency** (e.g., Improve logical linking and consistency as a whole)")
                clarity = st.checkbox("**Clarity** (e.g., Make texts formal, concise, readable, and understandable)")
                style = st.checkbox("**Style Change** (e.g., Convey your own preferences, such as voice, tone, emotions, etc.)")
                meaning = st.checkbox("**Meaning Change** (e.g., Update or add new information)")
                # domain = st.checkbox("**Domain-specific Knowledge** (e.g., Include more knowledge of your domain background)")
                other = st.checkbox("**Others** (If you click this, please give a detailed explanation to the above textbox.)")
                na = st.checkbox("**N/A** (Check only if you did not edit any span of the sentence.)")

                label_annotations['fluency'] = fluency
                label_annotations['coherency'] = coherency
                label_annotations['clarity'] = clarity 
                label_annotations['style'] = style 
                label_annotations['meaning'] = meaning
                # label_annotations['domain'] = domain
                label_annotations['other'] = other
                label_annotations['na'] = na

                st.markdown("<br><p> Please only click Next if you confirm your responses. There is no way to revise your edits after.</p>", unsafe_allow_html=True)

            save_btn_submit = form.form_submit_button("Next")

            if save_btn_submit:
                if edit_intention == "":
                    st.error("Fill out the Reasons Behind Those Edits in the above text box.")
                    return 
        
                annotated_intent = list(dict(filter(lambda e:e[1]==True, label_annotations.items())).keys())
                if len(annotated_intent) < 1:
                    st.error("Any of the checkboxes is not selected. Please choose all checkboxes that apply.")
                    return

                annot_data = {
                    "revision_info": st.session_state.sent_annotation, 
                    "sent_idx": self.cur_query_id,
                    "edit_sentence": self.annotation_targets, 
                    "edit_intent": edit_intention,
                    "label": annotated_intent
                }

                with open('../data/{}.jsonl'.format(st.session_state.participant), 'a') as out_file:
                    l = json.dumps(annot_data, ensure_ascii=False)
                    out_file.write(f"{l}\n")

                self.cur_query_id += 1
                self._select_annotation_targets()
                st.experimental_rerun()

        else:
            st.success("Congratulation. You have finished your tasks. ", icon="👍") 


def main():

    st.set_page_config(page_title="Annotate Your Edits", layout="wide")

    if 'visual_edit' not in st.session_state:
        st.markdown("<p> No edits have been made yet. Please navigate to Revise GPT-4 Texts page. </p>", unsafe_allow_html=True)
    else:
        st.markdown("<h2> Annotate Your Edits </h2>", unsafe_allow_html=True)
        st.markdown("""
                <br> Now, it's time to give your opinions and reasons about the edits that you have made on the original GPT-4 text.
                We would like to take a deeper look at your intention behind those edits. 
                <br>
                Here are the detailed instructions:
                <ol>
                    <li> First, you will see each sentence with your revision. At the below text box, give your reason or rationale behind the edits you made. </li>
                    <li> Then, select every checkboxes that apply to your intentions of making the edits to that sentence. </li>
                    <li> After clicking all checkboxes in a sentence, then go to the next button to see the next sentence. </li>
                </ol>
                <br>
                <p> <span style="color:red"> WARNING: </span> There is <b>no 'back' button</b> to change your response. Please make sure to review your responses and then go to the next sentence. </p>
                <hr>
                """, unsafe_allow_html=True)

        # Create two columns
        col1, col2 = st.columns(2)

        # In the left column, show st.session_state.visual_edit
        with col1:
            st.markdown("<h2>Entire Passage</h2>", unsafe_allow_html=True)
            st.markdown(st.session_state.visual_edit, unsafe_allow_html=True)

        # In the right column, show the rest of the interface
        with col2:
            demo = RevisionAnnotation()

if __name__ == '__main__':
    main()




