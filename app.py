import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

load_dotenv()

groq_api = os.getenv('GROQ_API_KEY')

st.set_page_config('Time Table Creator')

st.title('__Create Your Time Table__',)

# loading the images by converting them from pdf

from pdf2image import pdf2image

images = pdf2image.convert_from_path('TimeTable Project.pdf')

# creating prompt for the LLM model

template = '''
You are an expert in google sheets. Extract all the information even the small one from the uploaded google sheet images and analyse it properly.
You may get three images.

1.{image_1} : This have sheet with four columns with one column as Subject,and other are three different classes Jr. KG,Sr. KG and I.
    Subject has values english,science,maths etc. and the classes have values like 2,3,4 etc. which represent the number of periods of the particular subject
    in particular class in a week.

2. {image_2} : Second one is a sheet representing information about various classes and their home room teachers.This also has four columns :
   Class : The name of the class (e.g., "Nursery", "Jr.KG A").
   Home_room_Teachers : The names of the teachers assigned to the home room for the class (e.g., "Riya", "Swarali", or "Kim", "Rukhsaar").
   Subjects : The subjects taught in that class (e.g., "All" if it's a general home room with all subjects).
   Class_alloted : The role or allocation of the class, which in this case seems to be "Home Room", indicating the class is managed by a home room teacher.

3. {image_3} : Third one is also a sheet contains information about the teachers assigned to different subjects and their respective class sections. 
    Here's a breakdown of the structure:
    The 'Subject' column represents the name of the subject (e.g., 'Eng' for English, 'Jr. KG A' for Junior Kindergarten A, etc.).
    The other columns, such as 'Jr. KG A', 'Jr. KG B', etc., represent the class sections (e.g., Junior Kindergarten A, B, C, etc.), and the values are the 
    names of the teachers assigned to those class sections for that particular subject. For example : For the subject 'Eng', 'Jr. KG A' has teachers 
    'Nupur FT' and 'Pooja R' and 'Jr. KG B' has 'Maria' and 'Banu' as teachers, and so on.

Your task is to create the Time Table for all the classes using the three images and also consider the user_input to create the time table.
<user_input>
{user_input}
</user_input>

Don't provide any additional instruction and infomation other than the Time Tables

'''

prompt = PromptTemplate(
    template=template,
    input_variables=['image_1','image_2','image_3','user_input']
)


# using llama3 vision model with groq api 

llm = ChatGroq(model='llama-3.2-90b-vision-preview',api_key=groq_api)


# creating the chain 

chain = prompt|llm|StrOutputParser()


user_input = st.text_input(label='***Give Details***',placeholder='Provide detail regarding time interval,lunch break,assembly etc.')


timetable_format = '''
The Days must be in vertical axis and time-period in the horizontal axis
'''

if user_input:
    result = chain.invoke({'image_1':images[0],'image_2':images[2],'image_3':images[1],'user_input':user_input+timetable_format})

    st.write(result)
    st.error('The result is AI generated make sure to make changes according to you need')

else:
    st.warning('provide the details')