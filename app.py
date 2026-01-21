import streamlit as st
import google.generativeai as genai
from PIL import Image
import os 
import datetime as dt

# Configure the model

gemini_api_key = os.getenv('GOOGLE_API_KEY2')
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

#Lets Create sidebar for Image Upload 

st.sidebar.title(':red[Upload the Images of Defect Here]')
uploaded_image = st.sidebar.file_uploader('Image',type=['jpeg','jpg','png','jfif'],accept_multiple_files=True)
uploaded_image = [Image.open(img)for img in uploaded_image]
if uploaded_image:
    st.sidebar.success('Image has been uploaded Sucessfully')
    st.sidebar.subheader(':blue[Uploaded Images]')
    st.sidebar.image(uploaded_image)


# Lets create the main page
st.title(':orange[STRUCTURAL DEFECT:-->] :blue[AI Assisted Structural Defect Indetifier]')
st.markdown('#### This Application take the Images of the Structural Defects from the construction and prepare the AI Assisted Report')
title = st.text_input('Enter the Title of the Report')
name = st.text_input('Enter the name of the person who has prepared the Report ')
orgz = st.text_input('Enter the name of the Organisation')
desig = st.text_input('Enter the Designation of a Person who prepared Report')


if st.button('SUBMIT'):
    with st.spinner('Processing....'):
        prompt = f'''
                <Role>
                    You are a senior Structural & Civil Engineer with over 20 years of professional experience in
                    building design, construction supervision, site execution, and defect assessment.

                    <Objective>
                    Prepare a comprehensive, technically accurate, and professional **Structural Defect Assessment Report**
                    based on the construction defects observed in the images provided by the user.

                    <Context>
                    • The user has uploaded site photographs showing one or more visible structural or construction defects.
                    • The report must be suitable for submission to clients, consultants, contractors, or for official documentation.
                    * Images by user are attached
                
                    <Report Metadata>
                    Include the following details clearly at the beginning of the report:
                    • **Report Title**: {title} (this is provided by the user use this title as Report Title)
                    • **Prepared By**:

                    - new line 
                    Name: {name}

                    -new line 
                    Designation: {desig}

                    - new line
                    Organization: {orgz}

                    • new line 
                    **Date of Inspection Report**: {dt.datetime.now().date()} (Keep Format of Date DD-MM-YYYY)

                    <Defect Identification & Classification>
                    From the images, identify and classify **each defect separately**, such as (but not limited to):
                    • Structural cracks (flexural, shear, settlement, thermal, shrinkage)
                    • Non-structural cracks (plaster cracks, hairline cracks)
                    • Honeycombing in concrete
                    • Spalling of concrete
                    • Exposed or corroded reinforcement
                    • Construction joint defects
                    • Poor compaction or segregation of concrete
                    • Water seepage or dampness
                    • Efflorescence
                    • Improper concrete cover
                    • Surface scaling or delamination
                    • Formwork defects or misalignment
                    • Poor finishing or workmanship-related defects

                    <Defect Analysis (For Each Identified Defect)>
                    For **each defect**, provide the following in a structured manner:

                    1. **Defect Name**
                    2. **Location in Structure** (beam, column, slab, wall, foundation, etc.)
                    3. **Visual Description**
                    - Observable characteristics from the image
                    4. **Probable Causes**
                    - Design-related
                    - Material-related
                    - Workmanship-related
                    - Environmental or exposure-related
                    5. **Potential Impact on Structure**
                    - Effect on strength, durability, serviceability, and safety
                    6. **Severity Assessment**
                    - Severity Level: Low / Medium / High
                    - Nature of Defect: Avoidable / Inevitable
                    7. **Risk Evaluation**
                    - Immediate risk (if any)
                    - Long-term consequences if left unaddressed

                    <Repair & Rectification Recommendations>
                    For each defect, provide:

                    • **Short-Term Remedial Measures**
                    - Immediate actions to control or arrest the defect
                    • **Long-Term Repair or Rectification Solutions**
                    - Recommended repair techniques based on standard engineering practice

                    <Cost & Time Estimates>
                    Provide **approximate**:
                    • Repair Cost Range (₹ INR)
                    • Estimated Repair Duration (days/weeks)

                    (Assume typical Indian market conditions and clearly state that costs are indicative.)

                    <Preventive & Quality Control Measures>
                    List practical preventive measures, including:
                    • Design-stage considerations
                    • Material selection and quality checks
                    • On-site execution controls
                    • Concreting and curing best practices
                    • Inspection and quality assurance procedures
                    • Maintenance and periodic monitoring recommendations

                    <Formatting & Output Instructions>
                    • Generate the report in a **Word-document style format**
                    • Use:
                    - Clear section headings
                    - Bullet points
                    - Numbered lists
                    - Use Tables As much as possible (especially for defect summary, severity, cost, and time)
                    • Maintain a professional engineering tone
                    • Ensure the total content does **not exceed 3 pages** in a standard Word document
                    • Avoid unnecessary verbosity; prioritize clarity and technical accuracy

                    <Final Instruction>
                    Keep whole Report professional as well make sure it is precise and meaningful
                    Do Not Include HTML Formats like <br> and others
                    Do not mention AI, prompts, or image limitations.
                    Present the report as if prepared by a qualified structural engineering professional.

            '''
        response = model.generate_content([prompt,*uploaded_image],
                                          generation_config={'temperature':0.9})
        st.write(response.text)

    if st.download_button(
    label='Click To Download',
    data=response.text,
    file_name='Structural_defect_report.txt',
    mime='text/plain'
    ):
        st.success('The File is Downloaded Successfully')