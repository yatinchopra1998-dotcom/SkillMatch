import streamlit as st 
from pdfextractor import text_extractor
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# First lets configure the model 

gemini_api_key = os.getenv('test-project-1')
model = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash-lite',
    api_key = gemini_api_key,
    temperature=0.75,
)


# Lets create a side bar to upload the resume 
st.sidebar.title(':red[UPLOAD YOUR RESUME]')
file = st.sidebar.file_uploader('  Resume',type=['pdf'])
if file:
    file_text = text_extractor(file)
    st.sidebar.success('Resume Uploaded Successfully')



# Lets create the main page of the application 

st.title(":yellow[SKILL MATCH:-] AI Assisted Skill Matcher 🤖",width='content')
st.subheader("This application will help you match and analyse your resume with job descriptions using AI.",width='content')
tips = '''
:grey[Follow these steps:]
\n
:grey[1. Upload your resume (PDF Only) in the sidebar.]
\n
:grey[2. Copy and paste the job description in the text area below.]
\n
:grey[3. Click on the "Match Skills" button to see the analysis.]

'''
st.write(tips)

job_desc = st.text_area("Paste the Job Description here:",height=250,key='job_description',max_chars=50000)

if st.button("Match Skills"):
    with st.spinner('Analyzing your resume with the job description...'):
        prompt = f'''
        <role> You are an expert career coach and resume analyzer.
        <goal> Your task is to compare a applicant's resume with a job description provided by the applicant.
        <context> The following content is the applicant's resume:
        * Resume : {file_text}
        * Job Description : {job_desc}
        <format> The report should follow these steps
        * Give a brief description of applicant in 3 to 5 lines. 
        * Describe in percentage what are the chances of this resume getting selected for the job role(give approximate).
        * Need not to be exact percentage  you can give interval of percentage like.
        * Give the expected ATS score along with matching and non-matching keywords.
        * Perform SWOT analysis and explain each parameter that is strength,weakness,opportunity and threat in detail.
        * Give what all current resume that are required to be added or removed to match the job description.
        * Show both and current version of resume and modified or improved version of resume after analyzing with job description. 
        * Create two sample resume which can maximize the ATS score and selection percentage for the given job description.
        * Use bullet points wherever necessary for better readability.
        * Keep the entire response within 500 words and consise and to the point.

        <Instruction>
        * Create tables for description where ever required.
        * Strictly do not add any new skill in the sample resumes which is not present in the original resume.
        * The format of the sample resume should be in such a way that it can be copy pasted directly to word document or google docs without any formatting issues.

        '''


        response = model.invoke(prompt)
        st.write(response.content)
