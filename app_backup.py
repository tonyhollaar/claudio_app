"""
 _____ _                 _ _       
/  __ \ |               | (_)      
| /  \/ | __ _ _   _  __| |_  ___  
| |   | |/ _` | | | |/ _` | |/ _ \ 
| \__/\ | (_| | |_| | (_| | | (_) |
 \____/_|\__,_|\__,_|\__,_|_|\___/ 

@author: tonyhollaar
https://www.tonyhollaar.com/

Description: Audio To Text Transcript Application hosted by Streamlit using AssemblyAI API
Additional Functionalities:
    - Text Summary
    - Question and Answer Text Corpus
    - Sentiment Analysis
    - Emotion Analysis
"""
# =============================================================================
# Dependencies
# =============================================================================
import assemblyai as aai
import streamlit as st
from streamlit_option_menu import option_menu
from fire_state import create_store, form_update, get_state, set_state, get_store, set_store
from my_functions import show_lottie_animation, vertical_spacer, seconds_to_hhmmss, get_sentiment, save_audio_data, get_audio_data, create_flipcard, download_icon, balloon_heart_icon
from my_fonts import font_style, my_text_header, my_text_paragraph, color_text_by_sentiment
from transformers import pipeline
import requests

import networkx as nx # TEST  Knowledge Graphs
import spacy

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd

# =============================================================================
# INITIATE VARIABLES
# =============================================================================
# Initiate variable to store api_key for AssemblyAI -> needed to create transcript of audio to text!
api_key = None

try:
    # Get the API key from Streamlit secrets
    api_key_secrets = st.secrets["api_key"]
except KeyError:
    api_key_secrets = None

# Initiate Session State Variable(s)
key1, key2, key3, key4, key5, key6, key7, key8, key9, key10, key11 = create_store("CLAUDIO", [("whole_text", ""),         #key1
                                                                                        ("audio_url", ""),         #key2
                                                                                        ("audio_data", None),      #key3
                                                                                        ("treemap", None),         #key4
                                                                                        ("legend_html", None),     #key5
                                                                                        ("knowledge_graph", None), #key6
                                                                                        ("speaker_sentiments", None), #key7
                                                                                        ("transcript", ""),        #key8
                                                                                        ("whole_text", ""),        #key9
                                                                                        ("file_name", ""),         #key10
                                                                                        ("run", 0)])               #key11

# Set Boolean to check if new file is uploaded in Streamlit Widget
new_file_loaded = False

# =============================================================================
# FUNCTIONS
# =============================================================================
def initiate_global_variables():
    # Initiate Session State Variable(s)
    key1, key2, key3, key4, key5, key6, key7, key8, key9, key10, key11 = create_store("CLAUDIO", [("whole_text", ""),         #key1
                                                                                            ("audio_url", ""),         #key2
                                                                                            ("audio_data", None),      #key3
                                                                                            ("treemap", None),         #key4
                                                                                            ("legend_html", None),     #key5
                                                                                            ("knowledge_graph", None), #key6
                                                                                            ("speaker_sentiments", None), #key7
                                                                                            ("transcript", ""),        #key8
                                                                                            ("whole_text", ""),        #key9
                                                                                            ("file_name", ""),         #key10
                                                                                            ("run", 0)])               #key11

    return key1, key2, key3, key4, key5, key6, key7, key8, key9

def reset_session_states():
    for key in st.session_state.keys():
        #if key == '__CLAUDIO-transcript__' or key == "__CLAUDIO-whole_text__" or key == "__CLAUDIO-audio_url__":
        del st.session_state[key]
        
    key1, key2, key3, key4 = initiate_global_variables()



def read_file(filename):
    CHUNK_SIZE = 5242880
    with open(filename, 'rb') as _file:
        while True:
            
            data = _file.read(CHUNK_SIZE)
            if not data:
                break
            yield data
            
def upload_audio_to_assemblyai(api_key, audio_file):
    transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
    upload_endpoint = 'https://api.assemblyai.com/v2/upload'
    headers = {
        "authorization": api_key
    }

    # Upload audio file to AssemblyAI
    try:
        #upload_response = requests.post(upload_endpoint, headers=headers, data = uploaded_file[0].read())
        upload_response = requests.post(upload_endpoint, headers=headers, data = audio_data)
        
        audio_url = upload_response.json()['upload_url']
            
        return audio_url
    except:
        pass
    
# =============================================================================
# Main Page Setup
# =============================================================================
# PAGE SETTINGS ("centered" or "wide" | "auto" or "expanded" or "collapsed")
st.set_page_config(page_title = "claudio", layout = "centered", page_icon = "🎙️", initial_sidebar_state = "expanded") 

# FONTS
st.markdown(font_style, unsafe_allow_html=True) 

# =============================================================================
# Menu
# =============================================================================
menu_item = option_menu(menu_title = None, 
                         options = ["Home", "Settings", "About"], 
                         icons = ["house", "gear", "info-circle"],
                         menu_icon = "cast", 
                         default_index = 0, 
                         orientation = "horizontal", 
                         styles = {
                                     "container": {
                                         "padding": "0.5px",
                                         "background-color": "transparent",
                                         "border-radius": "10px",
                                         "border": "0px solid black",
                                         "margin": "0px 0px 0px 0px",
                                     },
                                     "icon": {
                                         "color": "#333333",
                                         "font-size": "20px",
                                     },
                                     "nav-link": {
                                         "font-size": "12px",
                                         "font-family": 'Ysabeau SC',
                                         "color": "F5F5F5",
                                         "text-align": "center",
                                         "margin": "0px",
                                         "padding": "8px",
                                         "background-color": "transparent",
                                         "opacity": "1",
                                         "transition": "background-color 0.3s ease-in-out",
                                     },
                                     "nav-link:hover": {
                                         "background-color": "#4715ef",
                                     },
                                     "nav-link-selected": {
                                         "background-color": "transparent",
                                         "color": "black",
                                         "opacity": "0.1",
                                         "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.0)",
                                         "border-radius": "0px",
                                     },
                                 }
                         )
        
if menu_item == 'Home':
    # TITLE
    my_text_header('Claudio', my_font_size = '48px', my_font_family = 'Rock Salt')
    
    # CASETTE ANIMATION
    show_lottie_animation(url="./images/casette.json", key="casette", height=200, width=200, speed = 1, loop=True, quality='high', col_sizes = [4,4,4]) 
    
    # =============================================================================
    # Sidebar Setup
    # =============================================================================
    with st.sidebar:
        with st.form('API'):
            col1, col2, col3 = st.columns([8,8,1])
            with col1:
                my_text_header('Step 1:', my_font_size = '24px', my_font_family = 'Rock Salt') # Title 1
                my_text_header('Step 2:', my_font_size = '24px', my_font_family = 'Rock Salt') # Title 2
                vertical_spacer(4)
                my_text_header('Step 3:', my_font_size = '24px', my_font_family = 'Rock Salt') # Title 3
            
            with col2:
                if api_key_secrets is None:
                    api_key_input = st.text_input("Enter :blue[**AssemblyAI**] API Key", value = '', help = '''to obtain an api key, register at https://www.assemblyai.com/''', label_visibility = 'visible')                                     
                else:
                    api_key_input = ''
                    
                    vertical_spacer(2)
                    
                    st.markdown("""
                    <div style="background-color: #f5f5f5; border: 0px solid #cfcfcf; border-radius: 8px; padding: 6px; text-align: left;">
                        &nbsp;&nbsp;&nbsp;<span style="color: #626262; font-size: 13px; font-family: 'Arial', sans-serif;">AssemblyAI API Key Found</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                uploaded_file = st.file_uploader(label = 'Upload Audio File', 
                                                 label_visibility='hidden', 
                                                 type = ["mp3"], 
                                                 accept_multiple_files = True,
                                                 )
                
                # Custom CSS Styling for st.file_uploader / hide standard text to make widget smaller
                hide_label = """
                <style>
                    .css-9ycgxx {
                        display: none;
                    }
                </style>
                """
                st.markdown(hide_label, unsafe_allow_html=True)
                
                # FORM BUTTON
                submit_button = st.form_submit_button(label="Start Transcript", 
                                                      use_container_width = True, 
                                                      type="primary")
    

    
    # =============================================================================
    # Knowledge Graph    
    # =============================================================================
    # Initialize spaCy for named entity recognition (NER)
    nlp = spacy.load('en_core_web_sm')
    
    # Create an empty knowledge graph using NetworkX
    knowledge_graph = nx.Graph()
    
    # Define a function to extract entities and relationships from text
    def extract_entities_and_relationships(text):
        doc = nlp(text)
        entities = [ent.text for ent in doc.ents]
        
        # Extract relationships (you may need to define custom logic for this)
        relationships = []
        
        return entities, relationships
    
    def visualize_graph(graph):
        # Create a Plotly figure
        fig = go.Figure()
    
        # Extract node positions
        pos = nx.spring_layout(graph)
    
        # Create nodes
        for node in graph.nodes():
            x, y = pos[node]
            fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", marker=dict(size=20), text=node, textposition="bottom center"))
    
        # Create edges
        for edge in graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines"))
    
        # Set layout options
        fig.update_layout(
            showlegend=False,
            hovermode="closest",
            margin=dict(l=0, r=0, b=0, t=0),
        )
    
        # Display the graph using Streamlit's `st.plotly_chart()` function
        st.plotly_chart(fig, use_container_width=True)
        
    #******************************************************************************
    # AssemblyAI Package
    #******************************************************************************
    # Process the form submission
    if submit_button:
        
        if uploaded_file is None or len(uploaded_file) == 0:
            # show error image
            st.image('https://github.com/tonyhollaar/claudio/blob/main/images/assemblyai_file_error.png?raw=true')
        
        elif uploaded_file is not None and len(uploaded_file) > 0:
            if uploaded_file[0].name != get_state("CLAUDIO", "file_name"):
                reset_session_states()
                new_file_loaded = True
                
            # =============================================================================
            # AUDIO PLAYBACK CODE
            # =============================================================================
            # Read and save the uploaded audio data
            audio_data = uploaded_file[0].read() # uploaded_file[0].read()
            save_audio_data(audio_data)
    
            # Display the audio data if available
            audio_data = get_audio_data()
            set_state("CLAUDIO", ("audio_data", audio_data)) # SAVE TO SESSION STATE
            
            if audio_data is not None:
                st.audio(audio_data, format="audio/mp3")

                # =============================================================================
                # API KEY -> Check if the user has provided an API key through the form
                # =============================================================================
                if api_key_input:
                    api_key = api_key_input
                    st.toast('Your API Key was used from the input!', icon='😍')
                elif api_key_secrets:
                    api_key = api_key_secrets
                    st.toast('Your API Key was found in secrets.toml file!', icon='😍')
                else:
                    st.warning('No API Key was provided. Please visit www.assemblyai.com to get one.')
                
                # Initialize AssemblyAI settings
                if api_key:
                    aai.settings.api_key = api_key
                else:
                    st.stop()    

                # =============================================================================
                # AUDIO_URL
                # =============================================================================
                # if audio_url is not created yet -> upload audio to AssemblyAI via API
                if new_file_loaded == True or get_state("CLAUDIO", "audio_url") == "":
                    audio_url = upload_audio_to_assemblyai(api_key, audio_data)
                else:
                    # If not found, upload the audio and store it in session state
                    audio_url = upload_audio_to_assemblyai(api_key, audio_data)
                    set_state("CLAUDIO", ("audio_url", audio_url)) # Store the audio URL in session state

                FILE_URL = audio_url
                #FILE_URL = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3" # TEST AUDIO MP3
                
                # Quick message on bottom-right of screen
                st.toast("Transcription in progress... please wait!")
                       
                # SET CONFIGURATION OF AssemblyAI - source: https://www.assemblyai.com/docs/Models/speech_recognition
                config = aai.TranscriptionConfig(speaker_labels=True, )
                
                # [OPTIONAL] Add custom spelling of words
                config.set_custom_spelling({"Kubernetes": ["k8s"], "SQL": ["Sequel"],})
            
                # Define AssemblyAI Transcriber
                transcriber = aai.Transcriber()
                
                # =============================================================================
                # START TRANSCRIPTION IF NOT IN SESSION STATE ! ELSE SKIP THIS PART OF CODE                
                # =============================================================================
                if new_file_loaded == True or get_state("CLAUDIO", "transcript") == "":                    
                    transcript = transcriber.transcribe(FILE_URL, config=config)
                    set_state("CLAUDIO", ("transcript", transcript)) # Store the transcript in session state

                    # =============================================================================
                    # Emotion analysis                 
                    # =============================================================================
                    # Setup Pipeline with the Model for Emotion Analysis
                    classifier = pipeline("text-classification", model="michellejieli/emotion_text_classifier")
                    
                    # Map the emotion label to the corresponding emoticon
                    emoticons = {
                        "anger": "🤬",
                        "disgust": "🤢",
                        "fear": "😨",
                        "joy": "😀",
                        "neutral": "😐",
                        "sadness": "😭",
                        "surprise": "😲" }
                    # =============================================================================

                    # Convert transcript to a list of dictionaries
                    transcript_data = []
                    
                    for utterance in transcript.utterances:
                        speaker_name = f"Speaker {utterance.speaker}"
                        start_time_ms = utterance.start
                        start_time_seconds = start_time_ms / 1000.0  # Convert milliseconds to seconds
                        time_in_hhmmss = seconds_to_hhmmss(start_time_seconds)
                        text = utterance.text
                        sentiment_score = get_sentiment(text)
            
                        # =============================================================================
                        # Emotion analysis - source: https://huggingface.co/michellejieli/emotion_text_classifier
                        # =============================================================================
                        emotion = classifier(text)
                        predicted_label = emotion[0]['label']
                        predicted_emoticon = emoticons.get(predicted_label, "Unknown")
                        # =============================================================================
                        
                        # =============================================================================
                        # STORE DATA RELATED TO TRANSCRIPT IN LIST                        
                        # =============================================================================
                        # Append data to the transcript_data list
                        transcript_data.append({
                            "time": time_in_hhmmss,
                            "speaker_name": speaker_name,
                            "text": text,
                            "sentiment_score": sentiment_score,
                            "predicted_emoticon": predicted_emoticon
                        })
                        
                    # Store the transcript data in session state
                    set_state("CLAUDIO", ("transcript", transcript_data)) # STORE TRANSCRIPT DATA IN SESSION STATE
                
                # =============================================================================
                # IF ALREADY FOUND IN SESSION STATE LETS GO!                
                # =============================================================================
                else:
                    # If transcript exists in session state, retrieve it
                    transcript_data = get_state("CLAUDIO", "transcript")

                # Display the transcript data outside the loop
                with st.expander('transcript', expanded=True):
                    for utterance_data in transcript_data:
                        # Create two columns
                        col1, col2, col3 = st.columns([2, 8, 2])
                
                        # Display the time in the left time column
                        col1.write(utterance_data["time"])
                
                        # Display the transcript (colored text) in the middle column
                        colored_text = color_text_by_sentiment(utterance_data["text"], utterance_data["sentiment_score"])
                        col2.write(f"<b>{utterance_data['speaker_name']}:</b> {colored_text}", unsafe_allow_html=True)
                
                        # Display Emotion Analysis in right-side column
                        col3.write(f"{utterance_data['predicted_emoticon']}")
                    
                with st.expander('named entity recognition', expanded=True):
                    
                    # Load the English language model - source: https://spacy.io/models/en#en_core_web_sm
                    nlp = spacy.load("en_core_web_sm")
                    
                    # Transcript Text (whole text)
                    transcript_text = "\n".join(utterance_data["text"] for utterance_data in transcript_data)
                    set_state("CLAUDIO", ("whole_text", transcript_text))
                    
                    # Process the text with spaCy
                    doc = nlp(transcript_text) #doc = nlp(whole_text)
                    
                    # Extract entities and their entity types
                    entities = [(ent.text, ent.label_) for ent in doc.ents]
                        
                    # Create a DataFrame to store the entities and their categories
                    df = pd.DataFrame(entities, columns=["Entity", "Entity Type"])
                    
                    # Define group abbreviations and definitions based on entity categories
                    group_definitions = {
                                            "CARDINAL": ("Cardinal Number", "Numerals that indicate quantity (e.g., 'one', 'two')"),
                                            "DATE": ("Date", "Dates or periods in time (e.g., 'January 1, 2023')"),
                                            "EVENT": ("Event", "Named events (e.g., 'Olympics', 'conference')"),
                                            "FAC": ("Facility", "Buildings, airports, highways, bridges, etc."),
                                            "GPE": ("Geopolitical Entity", "Entities related to countries, regions, or places"),
                                            "LANGUAGE": ("Language", "Any named language"),
                                            "LAW": ("Law", "Named documents made into laws"),
                                            "LOC": ("Location", "Non-GPE locations, mountain ranges, bodies of water"),
                                            "MONEY": ("Monetary Value", "Monetary values, including unit (e.g., '10 USD')"),
                                            "NORP": ("Nationalities or Religious or Political Groups", "Nationalities, religious groups, or political groups"),
                                            "ORDINAL": ("Ordinal Number", "Ordinal numbers (e.g., 'first', 'second')"),
                                            "ORG": ("Organization", "Named organizations or groups"),
                                            "PERCENT": ("Percentage", "Percentage, including '%'"),
                                            "PERSON": ("Person", "Individual names or personal entities"),
                                            "PRODUCT": ("Product", "Named products or services"),
                                            "QUANTITY": ("Quantity", "Measurements, as of weight or distance (e.g., '5kg', '10 meters')"),
                                            "TIME": ("Time", "Times smaller than a day (e.g., '10:30 am')"),
                                            "WORK_OF_ART": ("Work of Art", "Titles of books, songs, etc."),
                                        }
                    
                    # Create columns for group abbreviations and definitions
                    df["Group Abbreviation"] = df["Entity Type"].map(lambda x: group_definitions.get(x, ("N/A", "N/A"))[0])
                    df["Group Definition"] = df["Entity Type"].map(lambda x: group_definitions.get(x, ("N/A", "N/A"))[1])
                    
                    # Sort the DataFrame by the "Entity Type" column
                    df_sorted = df.sort_values(by="Entity Type")
                    
                    #st.dataframe(df_sorted) # Display the sorted DataFrame
                    
                    # =============================================================================
                    # Create a Treemap using Plotly Express                     
                    # =============================================================================
                    # Count the occurrences of each entity type and entity name
                    entity_counts = df_sorted.groupby(["Entity Type", "Entity"]).size().reset_index(name="Count")
                    
                    # Merge the entity counts back into df_sorted based on 'Entity Type' and 'Entity'
                    df_sorted = pd.merge(df_sorted, entity_counts, on=["Entity Type", "Entity"])
                    
                    # Get a list of unique entity types
                    unique_entity_types = df_sorted["Entity Type"].unique()
                    
                    # Create a dictionary to map entity types to colors
                    entity_type_colors = {
                                            "CARDINAL": "#1f77b4",      # Blue
                                            "DATE": "#fd5151",          # Orange
                                            "EVENT": "#2ca02c",         # Green
                                            "FAC": "#d62728",           # Red
                                            "GPE": "#2e83d1",           # Purple
                                            "LANGUAGE": "#8c564b",      # Brown
                                            "LAW": "#e377c2",           # Pink
                                            "LOC": "#99d1fd",           # Gray
                                            "MONEY": "#bcbd22",         # Olive
                                            "NORP": "#17becf",          # Teal
                                            "ORDINAL": "#aec7e8",       # Light Blue
                                            "ORG": "#ffbb78",           # Light Orange
                                            "PERCENT": "#98df8a",       # Light Green
                                            "PERSON": "#c5b0d5",        # Light Purple
                                            "PRODUCT": "#c49c94",       # Light Red
                                            "QUANTITY": "#f7b6d2",      # Light Pink
                                            "TIME": "#c7c7c7",          # Light Gray
                                            "WORK_OF_ART": "#dbdb8d"    # Light Olive
                                        }
                    
                    # Create a custom color scale based on the entity_type_colors dictionary
                    #color_scale = [entity_type_colors.get(entity_type, "gray") for entity_type in unique_entity_types]
                    
                    # Create a categorical column for entity types
                    df_sorted['Entity Type'] = pd.Categorical(df_sorted['Entity Type'], categories=unique_entity_types)
                    
                    # Create a treemap using Plotly Express with the categorical color scale
                    fig = px.treemap(
                        df_sorted,
                        path=["Entity Type", "Entity"],
                        values="Count",
                        labels={"Entity Type": "Entity Type"},
                        color="Entity Type",  # Use the categorical column for color
                        color_discrete_map=entity_type_colors,  # Specify colors using the entity_type_colors dictionary
                    )
                    
                    # Adjust the margin to reduce the bottom margin
                    fig.update_layout(margin=dict(t=0, b=10, l=0, r=0))
                    
                    # save figure to session state
                    set_state("CLAUDIO", ("treemap", fig))
                    
                    # Display the treemap using Streamlit's st.plotly_chart() function
                    st.plotly_chart(fig, use_container_width=True)                 

                    # =============================================================================
                    # LEGEND
                    # =============================================================================
                    # Create custom HTML and CSS styling for the legend
                    legend_html = '<div style="display: flex; flex-wrap: wrap;">'
                    for entity_type in unique_entity_types:
                        color = entity_type_colors.get(entity_type, "gray")  # Default to gray if no color defined
                        legend_html += f'<div style="margin-right: 10px; margin-bottom: 5px; padding: 5px; background-color: {color}; color: white; border-radius: 5px;">'
                        legend_html += f'    <span style="font-weight: bold;">{entity_type}</span><br>'
                        legend_html += f'    <span style="font-style: italic;">{group_definitions.get(entity_type, ("N/A", "N/A"))[0]}</span><br>'
                        legend_html += f'    <span>{group_definitions.get(entity_type, ("N/A", "N/A"))[1]}</span>'
                        legend_html += '</div>'
                    legend_html += '</div>'
                    
                    # save legend_html to session statea
                    set_state("CLAUDIO", ("legend_html", legend_html))
                    
                    # Display the legend-like HTML
                    my_text_paragraph("LEGEND", my_font_size="14px", my_text_align="left")
                    st.markdown(legend_html, unsafe_allow_html=True)                    

                with st.expander('knowledge graph', expanded=True): 
                    # =============================================================================
                    #  KNOWLEDGE GRAPH            
                    # =============================================================================
                    # Extract entities and relationships from the text
                    entities, relationships = extract_entities_and_relationships(transcript_text)
                    
                    # Add entities to the knowledge graph
                    knowledge_graph.add_nodes_from(entities)
                    
                    # Add relationships to the knowledge graph
                    knowledge_graph.add_edges_from(relationships)
                     
                    # save to session state
                    set_state("CLAUDIO", ("knowledge_graph", knowledge_graph))
                    
                    visualize_graph(knowledge_graph)
                    
                # =============================================================================
                # Get for each speaker the Average Sentiment Score
                # =============================================================================
                with st.expander('sentiment analysis', expanded=True):
                    # Get for each speaker the Average Sentiment Score
                    # Define thresholds for sentiment scores
                    positive_threshold = 0.5  # Example threshold for positive sentiment
                    negative_threshold = -0.5  # Example threshold for negative sentiment
                    
                    # Define sentiment-to-emoticon mapping
                    sentiment_emoticons = {
                        "positive": "😃",
                        "neutral": "😐",
                        "negative": "😞"}
                    
                    speaker_sentiments = {}  # Dictionary to store sentiment scores for each speaker

                    for utterance_data in transcript_data:
                        speaker = utterance_data["speaker_name"]
                        text = utterance_data["text"]
                        sentiment_score = get_sentiment(text)
                        
                        if speaker not in speaker_sentiments:
                            speaker_sentiments[speaker] = []
                        
                        speaker_sentiments[speaker].append(sentiment_score)
                    
                    # save to session state 
                    set_state("CLAUDIO", ("speaker_sentiments", speaker_sentiments))
                    
                    for speaker, sentiment_scores in speaker_sentiments.items():
                        # Calculate average sentiment score based on chunks of text
                        average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
                        
                        # Determine the sentiment label based on the threshold
                        if average_sentiment >= positive_threshold:
                            sentiment_label = "positive"
                        elif average_sentiment <= negative_threshold:
                            sentiment_label = "negative"
                        else:
                            sentiment_label = "neutral"
                        
                        # Get the emoticon for the sentiment label
                        sentiment_emoticon = sentiment_emoticons[sentiment_label]
                        
                        # Show average sentiment score(s) in Streamlit with emoticon
                        st.write(f"{speaker} Average Sentiment: **{sentiment_label.capitalize()}** {sentiment_emoticon} ({average_sentiment:.2f})")
                        
                with st.expander('summary', expanded=True):
                    # Use whole_text variable with other model
                    # source 1: https://www.youtube.com/watch?v=TsfLm5iiYb4
                    # source 2: https://huggingface.co/docs/transformers/main_classes/pipelines#transformers.SummarizationPipeline
                    # Note: If no framework is specified, will default to the one currently installed. If no framework is specified and both frameworks are installed, will default to the framework of the model, or to PyTorch if no model is provided.
                    summarizer = pipeline('summarization')
                    summary = summarizer(transcript_text, max_length=130, min_length=30, do_sample=False)
                    st.write(summary[0]['summary_text'])
            
    with st.sidebar:
        
        vertical_spacer(1)
    
        # Create a form to wrap the input and button
        with st.form("question_form"):
            my_text_header("Q&A", my_text_align='center')
            col1, col2 = st.columns([18, 2])
            with col1:
                # Create a text input box for user questions
                #my_text_paragraph('Type your question here:')
                user_question = st.text_input("Type your question here:", value="Type your question here...", label_visibility='collapsed')
            with col2:
                # Add a submit button to the form
                submit_button = st.form_submit_button("❓")
        
            # Check if the form is submitted (button is clicked)
            if submit_button:
                # Initialize the question answering pipeline
                oracle = pipeline(model="deepset/roberta-base-squad2")
            
                # Get the answer to the user's question
                answer = oracle(question=user_question, context = get_state("CLAUDIO", "whole_text"))
            
                threshold = 0.01  # Adjust the threshold as needed
                
                if answer["score"] is not None and answer["score"] >= threshold:
                    # If the score is above the threshold, display the answer with the score
                    # Display the answer with the score as a percentage
                    my_text_paragraph(answer["answer"], score=answer["score"], my_text_align='left', my_font_family='Open Sans')
                else:
                    # If the score is below the threshold, display "No answer could be found"
                    my_text_paragraph("No answer could be found")
    
        with st.expander('', expanded=True):    
            my_text_header(f"{download_icon}", my_text_align='center')
            vertical_spacer(1)
            download_btn = st.button(label = 'Download Transcript', type="secondary", use_container_width=True)

        # get the file name 
        try:
            #st.write('test filename', uploaded_file[0].name)
            set_state("CLAUDIO", ("file_name", uploaded_file[0].name))
        except:
            pass


    # =============================================================================
    # With Q&A question by user -> reload the main page again
    # =============================================================================
    if submit_button:
        try:
            # =============================================================================
            # PLAY AUDIO            
            # =============================================================================
            st.audio(get_state("CLAUDIO", "audio_data"), format="audio/mp3")
            
            # =============================================================================
            # TRANSCRIPT            
            # =============================================================================
            # If transcript exists in session state, retrieve it
            transcript_data = get_state("CLAUDIO", "transcript")
         
            # Display the transcript data outside the loop
            with st.expander('transcript', expanded=True):
                 	for utterance_data in transcript_data:
                 		# Create two columns
                 		col1, col2, col3 = st.columns([2, 8, 2])
                 
                 		# Display the time in the left time column
                 		col1.write(utterance_data["time"])
                 
                 		# Display the transcript (colored text) in the middle column
                 		colored_text = color_text_by_sentiment(utterance_data["text"], utterance_data["sentiment_score"])
                 		col2.write(f"<b>{utterance_data['speaker_name']}:</b> {colored_text}", unsafe_allow_html=True)
                 
                 		# Display Emotion Analysis in right-side column
                 		col3.write(f"{utterance_data['predicted_emoticon']}")
                         
            # =============================================================================
            # NER - NAMED ENTITY RECOGNITION
            # =============================================================================
            with st.expander('named entity recognition', expanded=True):
                fig = get_state("CLAUDIO", "treemap")
                st.plotly_chart(fig, use_container_width=True)     
                legend_html = get_state("CLAUDIO", "legend_html")
                my_text_paragraph("LEGEND", my_font_size="14px", my_text_align="left")
                st.markdown(legend_html, unsafe_allow_html=True)    
                
            # =============================================================================
            # Knowledge Graph                
            # =============================================================================
            with st.expander('knowledge graph', expanded=True): 
                knowledge_graph = get_state("CLAUDIO", "knowledge_graph")
                visualize_graph(knowledge_graph)
                
            # =============================================================================
            # Speaker Sentiment                
            # =============================================================================
            with st.expander('sentiment analysis', expanded=True):
                # retrieve sentiments from session state
                speaker_sentiments = get_state("CLAUDIO", "speaker_sentiments")
                
                # Get for each speaker the Average Sentiment Score
                # Define thresholds for sentiment scores
                positive_threshold = 0.5  # Example threshold for positive sentiment
                negative_threshold = -0.5  # Example threshold for negative sentiment
                
                # Define sentiment-to-emoticon mapping
                sentiment_emoticons = {
                    "positive": "😃",
                    "neutral": "😐",
                    "negative": "😞"}

                for speaker, sentiment_scores in speaker_sentiments.items():
                    # Calculate average sentiment score based on chunks of text
                    average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
                    
                    # Determine the sentiment label based on the threshold
                    if average_sentiment >= positive_threshold:
                        sentiment_label = "positive"
                    elif average_sentiment <= negative_threshold:
                        sentiment_label = "negative"
                    else:
                        sentiment_label = "neutral"
                    
                    # Get the emoticon for the sentiment label
                    sentiment_emoticon = sentiment_emoticons[sentiment_label]
                    
                    # Show average sentiment score(s) in Streamlit with emoticon
                    st.write(f"{speaker} Average Sentiment: **{sentiment_label.capitalize()}** {sentiment_emoticon} ({average_sentiment:.2f})")
        except:
            pass

if menu_item == "About":
    # FLIPCARD HTML+CSS IN STREAMLIT
    image_url_front = 'https://raw.githubusercontent.com/tonyhollaar/claudio/main/images/assemblyai_about.png'
    image_url_back = 'https://raw.githubusercontent.com/tonyhollaar/claudio/main/images/assemblyai_about_back.png'
    create_flipcard(image_path_front_card=image_url_front, image_path_back=image_url_back, font_size_back='16px')