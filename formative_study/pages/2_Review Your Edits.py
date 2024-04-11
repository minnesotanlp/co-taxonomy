import streamlit as st
import json


# def visualize_edits(string_json_data):

#     json_data = json.loads(string_json_data)
#     added_tokens = json_data['added']
#     removed_tokens = json_data['removed']
#     unchanged_tokens = json_data['unchanged']
    
#     all_tokens = []
#     for token in unchanged_tokens:
#         all_tokens.append((token['token'], token['position'], 'unchanged'))
    
#     for token in removed_tokens:
#         all_tokens.append((token['token'], token['position'], 'removed'))
        
#     for token in added_tokens:
#         all_tokens.append((token['token'], token['position'], 'added'))
        
#     all_tokens.sort(key=lambda x: x[1])
    
#     html_text = ""
#     for token in all_tokens:
#         if token[0] == '\n\n':
#             html_text += "<br><br>"
#         elif token[2] == 'removed':
#             html_text += f'<s>{token[0]}</s> '
#         elif token[2] == 'added':
#             html_text += f'<span style="color:red;">{token[0]}</span> '
#         else:
#             html_text += f'{token[0]} '            
#     return html_text


def visualize_edits(string_json_data):
    json_data = json.loads(string_json_data)
    diffs = json_data['diffs'][-1]['iteration'] # Visualizing the last edited revision

    html_text = ""
    for diff in diffs:
        if diff == '\n\n':
            html_text += "<br><br>"
        elif diff.startswith("- "):
            html_text += f'<s>{diff[2:]}</s> '
        elif diff.startswith("+ "):
            html_text += f'<span style="color:red;">{diff[2:]}</span> '
        elif diff.startswith("  "):
            html_text += f'{diff[2:]} '

    return html_text

def main():

    st.set_page_config(page_title="Review Your Edits")
    # st.sidebar.header("Visualizing your edits with the original text")

    if 'differences_json' not in st.session_state:
        # st.session_state.differences_json = None
        st.markdown("<p> No edits have been made yet. Please navigate to Revise GPT-4 Texts page. </p>", unsafe_allow_html=True)
    else:
        visual_edit = visualize_edits(st.session_state.differences_json)
        st.markdown("""
                    <h2> Review Your Edits! </h2> 
                    """, unsafe_allow_html=True)
        st.markdown(""" 
                    <p> Here, you can track your revision as a comparison to the original template. </p><hr>""", unsafe_allow_html=True)
        st.markdown(visual_edit, unsafe_allow_html=True)
        st.markdown("""
                    <hr>
                    <br>
                    <p> If you do not see some parts of your revision, then please go back to Revise GPT-4 Texts page and re-click 'Finish Revision' button at the bottom. </p>
                    <br><br>
                    """, unsafe_allow_html=True)
        if 'visual_edit' not in st.session_state:
            st.session_state.visual_edit = None 

        st.session_state.visual_edit = visual_edit

if __name__ == '__main__':
    main()


























