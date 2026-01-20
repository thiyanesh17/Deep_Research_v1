import streamlit as st
import pandas as pd
import re
import numpy as np
import os

# Page Configuration
st.set_page_config(page_title="Deep Research Engine", layout="wide")

# Title and Tagline
# Custom CSS for Center Alignment
st.markdown(
    """
    <style>
    .title {
        text-align: center;  /* Center alignment */
        color: black;        /* Black text */
        font-size: 40px;      /* Large title font */
        font-weight: bold;   /* Bold text for emphasis */
    }
    .tagline {
        text-align: center;  /* Center alignment for tagline */
        color: grey;         /* Grey text for better contrast */
        font-size: 14px;      /* Small, readable font size */
    }
    </style>
    """, unsafe_allow_html=True
)

# Title and Tagline
st.markdown('<h1 class="title">Deep Research Engine</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="tagline">Developed for Logitech Internal Sustainability Team</h3>', unsafe_allow_html=True)
st.write("")
st.write("")
st.write("")

if st.sidebar.button("Clear State"):
    st.session_state.clear()


# Initialize or load the DataFrame to store user inputs

   
# Convert Data to DataFrame
df = pd.read_csv(r"combined_csv.csv")


def truncate_to_words(text, max_words=150):
    words = text.split()
    if len(words) > max_words:
        return ' '.join(words[:max_words]) + '...[read more]'
    return text


# Sidebar with Topic List (Including 'All')
st.sidebar.header("Topics")
unique_topics = ["All"] + list(df["Topic_Name"].unique())
selected_topic = st.sidebar.radio("Select a Topic:", unique_topics)
filtered_df1 = pd.DataFrame()
# Filter Data
if selected_topic != "All":
    filtered_df1 = df[df["Topic_Name"] == selected_topic]
    topic_names = filtered_df1["Topic_Name"].unique() # Display all topics
    num_topics = len(topic_names)  # Total unique topics
    # Divide topics into rows of 3
    rows = [topic_names[i:i+3] for i in range(0, num_topics, 3)]  # Group topics into sets of 3
    st.header(f"Research Report: {selected_topic}")
    intro_content = filtered_df1[filtered_df1["Section_Topic"] == "1. Introduction"]["Section_content"].values
    intro_content = [re.sub(r'.*Introduction\s*', '', content) for content in intro_content]
    if intro_content:
        #st.subheader("Introduction")
        st.write(intro_content[0])
    
    # Render Section Data
    filtered_content = filtered_df1[~filtered_df1["Section_Topic"].isin(["1. Introduction", "9. Conclusion"])]
    for _, row in filtered_content.iterrows():
        with st.expander(row["Section_Topic"]):  # Display collapsible sections (e.g., Methodology, Results)
            st.write(row['Section_description'])
            st.write(row['Section_content'])
            st.subheader("Below is the research paper summary")
            st.write(row['Arxiv'])
            st.write(f"You can View Research Paper here:({row['URL']})")
            raw_content_filename = f"{row['Section_Topic'].replace(' ', '_')}_raw_content.txt"
            raw_content_data = row["Raw_content"]
            st.download_button(
            label="Download Raw Content",
            data=raw_content_data,
            file_name=raw_content_filename,
            mime="text/plain"
            )
    conclusion_df = filtered_df1[filtered_df1["Section_Topic"].isin(["9. Conclusion"])]
    for _, row in conclusion_df.iterrows():
        with st.expander(row["Section_Topic"]):
            st.write(row['Section_description'])
            st.write(row['Section_content'])
        
else:
    select_topic = None
    filtered_df = df  # Display all topics    
    
    # Display Topics Horizontally
    topic_names = filtered_df["Topic_Name"].unique()  # Get unique topics
    num_topics = len(topic_names)  # Total unique topics
    
    # Divide topics into rows of 3
    rows = [topic_names[i:i+3] for i in range(0, num_topics, 3)]  # Group topics into sets of 3
    
    
    
    
    
    # Loop through rows and create columns for each
    for row_topics in rows:
        columns = st.columns(len(row_topics))  # Create columns for the current row
        for i, topic in enumerate(row_topics):
            with columns[i]:  # Access the column for the topic
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(
                    f"""
                    <h2 style="text-align: center; font-size: 24px; margin-bottom: 20px;">
                        {topic}
                    </h2>
                    """,
                    unsafe_allow_html=True)  # Display the topic
                with col2:
                    if st.button(f"View", key=f"btn_{topic}"):  # Use key to make uniqueness
                        st.session_state.select_topic = topic
                        st.rerun()    
                intro_data = filtered_df[filtered_df["Topic_Name"] == topic]
                intro_content = intro_data[intro_data["Section_Topic"] == "1. Introduction"]["Section_content"].values
                intro_content = [re.sub(r'.*Introduction\s*', '', content) for content in intro_content]
                truncated_content = [truncate_to_words(content, max_words=150) for content in intro_content]
                #filtered_df["Section_content"] = filtered_df["Section_content"].str.replace(r'^Introduction\s*', '', regex=True)
                if len(intro_content) > 0:
                    st.markdown(f"""
        			<div style="text-align: center; font-size: 16px; margin-top: 10px;">
        			{truncate_to_words(intro_content[0], max_words=75)}
        			</div>
        			""",
        			unsafe_allow_html=True
        			) # Display the introduction content!
                else:
                    st.write("No Introduction content available.")
                st.write("")
                st.write("")
            st.write("")
    
    if "select_topic" in st.session_state:
        select_topic = st.session_state.select_topic
        st.write("")  # Add some space
        st.markdown(
            f"<h1 style='text-align: center;'>Research Report for {select_topic}</h1>",
            unsafe_allow_html=True
        )
        st.write("")  # Add some space
        
        # Filter DataFrame for the selected topic
        filtered_df_top = df[df["Topic_Name"] == select_topic]

        #st.header(f"Research Report: {select_topic}")
        intro_content = filtered_df_top[filtered_df_top["Section_Topic"] == "1. Introduction"]["Section_content"].values
        intro_content = [re.sub(r'.*Introduction\s*', '', content) for content in intro_content]
        if intro_content:
            #st.subheader("Introduction")
            st.write(intro_content[0])
        
        # Render Section Data
        filtered_content = filtered_df_top[~filtered_df_top["Section_Topic"].isin(["1. Introduction", "9. Conclusion"])]
        for _, row in filtered_content.iterrows():
            with st.expander(row["Section_Topic"]):  # Display collapsible sections (e.g., Methodology, Results)
                st.write(row['Section_description'])
                st.write(row['Section_content'])
                st.subheader("Below is the research paper summary")
                st.write(row['Arxiv'])
                st.write(f"You can View Research Paper here:({row['URL']})")
                raw_content_filename = f"{row['Section_Topic'].replace(' ', '_')}_raw_content.txt"
                raw_content_data = row["Raw_content"]
                st.download_button(
                label="Download Raw Content",
                data=raw_content_data,
                file_name=raw_content_filename,
                mime="text/plain"
                )
        conclusion_df = filtered_df_top[filtered_df_top["Section_Topic"].isin(["9. Conclusion"])]
        for _, row in conclusion_df.iterrows():
            with st.expander(row["Section_Topic"]):
                st.write(row['Section_description'])
                st.write(row['Section_content'])



# Ensure the output directory exists
output_dir = "data/output/"
os.makedirs(output_dir, exist_ok=True)

# File path for saving the DataFrame
file_path = os.path.join(output_dir, "user_inputs_df.csv")


# Function to save or append data
def save_user_inputs(df, file_path):
    if os.path.exists(file_path):
        # If the file exists, append without overwriting
        existing_df = pd.read_csv(file_path)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.drop_duplicates(inplace=True)
        updated_df.to_csv(file_path, index=False)
    else:
        # If the file doesn't exist, create a new file
        df.to_csv(file_path, index=False)
    return file_path



if "user_inputs_df" not in st.session_state:
    st.session_state.user_inputs_df = pd.DataFrame(columns=["Topic", "Prompt", "Num_Sections", "Num_Research_Papers"])

if "topic" not in st.session_state:
    st.session_state.topic = ""
if "prompt" not in st.session_state:
    st.session_state.prompt = ""

# Streamlit Sidebar Inputs
with st.sidebar:
    #st.header("Deep Research Input")
    topic = st.text_input("Enter the Topic to perform the Deep research:")
    prompt = st.text_input("Enter the Prompt [optional]:")
    num_sections = st.slider("Mention the Number of Sections:", min_value=1, max_value=10, value=3)
    num_research_papers = st.slider("Mention the Number of Research Papers/Section:", min_value=1, max_value=20, value=5)

    # Submit button to capture the information
    if st.button("Submit"):
        # Append the input to the DataFrame stored in session state
        new_row = pd.DataFrame([{
            "Topic": topic,
            "Prompt": prompt,
            "Num_Sections": num_sections,
            "Num_Research_Papers": num_research_papers,
        }])  # IMPORTANT: Wrap the dictionary in a list to create a DataFrame
        
        # Append the new row to the stored DataFrame using pd.concat
        st.session_state.user_inputs_df = pd.concat([st.session_state.user_inputs_df, new_row], ignore_index=True)
        st.session_state.topic = ""
        st.session_state.prompt = ""


        # Display Thank You Message
        st.success("Thanks for submitting, Research engine is running .. It will be added to the Topics list once it's processed")

        if "user_inputs_df" in st.session_state and not st.session_state.user_inputs_df.empty:
            save_user_inputs(st.session_state.user_inputs_df, file_path)
            st.success(f"DataFrame has been updated successfully! [Download here](data/output/user_inputs_df.csv)")
            
        # Reset the fields (Streamlit automatically resets UI inputs after user action)
        #st.rerun()  # Force re-run to clear the form fields

    

    
                


        

