import streamlit as st
import os
import json
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import google.generativeai as genai
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()

api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def preprocess_data(data):
    """Replaces null values with 0 in the data dictionary."""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                data[key] = [0 if v is None else v for v in value]
    return data

def plot_data(plots):
    """Plots the graphs based on the provided JSON data."""
    for plot in plots:
        parameter = plot.get("key", "Unknown Parameter")
        plot_type = plot.get("type", "Unknown Plot Type").replace(" ", "_").lower()
        data = preprocess_data(plot.get("data", {}))

        st.subheader(parameter)

        if data:
            x = data.get("x", [])
            y = data.get("y", [])

            if not x or (plot_type not in ["pie"] and not y):
                st.warning(f"Missing 'x' or 'y' data for {parameter}. Skipping plot.")
                continue

            if plot_type not in ["pie"] and len(x) != len(y):
                st.warning(f"Mismatch in lengths of 'x' ({len(x)}) and 'y' ({len(y)}) for {parameter}. Skipping plot.")
                continue

            if plot_type in ["bar", "bar_chart"]:
                plt.figure()
                plt.bar(x, y, color="skyblue")
                plt.xlabel("Categories" if not isinstance(x[0], str) else "Years")
                plt.ylabel("Values")
                plt.title(parameter)
                plt.xticks(rotation=45)
                st.pyplot(plt)

            elif plot_type in ["line", "line_chart"]:
                plt.figure()
                plt.plot(x, y, marker="o", linestyle="-", color="blue")
                plt.xlabel("Categories" if not isinstance(x[0], str) else "Years")
                plt.ylabel("Values")
                plt.title(parameter)
                plt.xticks(rotation=45)
                st.pyplot(plt)

            elif plot_type in ["scatter"]:
                plt.figure()
                plt.scatter(x, y, color="green")
                plt.xlabel("Categories" if not isinstance(x[0], str) else "Years")
                plt.ylabel("Values")
                plt.title(parameter)
                plt.xticks(rotation=45)
                st.pyplot(plt)

            elif plot_type in ["hist", "histogram"]:
                plt.figure()
                plt.hist(y, bins=10, color="purple", alpha=0.7)
                plt.xlabel("Values")
                plt.ylabel("Frequency")
                plt.title(parameter)
                st.pyplot(plt)

            elif plot_type in ["pie"]:
                if len(x) != len(y):
                    st.warning(f"Mismatch in lengths of 'x' ({len(x)}) and 'y' ({len(y)}) for {parameter}. Skipping plot.")
                    continue
                plt.figure()
                plt.pie(y, labels=x, autopct="%1.1f%%", startangle=140, colors=plt.cm.tab20.colors)
                plt.title(parameter)
                st.pyplot(plt)

            elif plot_type in ["box", "boxplot"]:
                plt.figure()
                plt.boxplot(y, vert=True, patch_artist=True, boxprops=dict(facecolor="cyan"))
                plt.title(parameter)
                st.pyplot(plt)

            else:
                st.warning(f"Plot type '{plot_type}' is not supported.")
        else:
            st.warning("No data available to plot.")



def document_analysis_operation(): 
    base_path = 'all_data/data/Engineering' 
    try:
        college_folders = [folder for folder in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, folder))]
    except FileNotFoundError:
        st.error("The specified folder path does not exist.")
        return

    st.title("Document Analysis")
     
    selected_college = st.selectbox("Select a College", college_folders)
    
    if selected_college: 
        college_path = os.path.join(base_path, selected_college)
         
        pdf_files = [file for file in os.listdir(college_path) if file.endswith('.pdf')]
        
        if pdf_files:
            content = ""
            years = ""
            for file in pdf_files:
                file_name = os.path.splitext(file)[0]   
                years += file_name + ", "
            years = years.rstrip(", ")
            st.write(f"Using the Data of NIRF Report for year: {years}")

            for pdf_file in pdf_files:
                pdf_path = os.path.join(college_path, pdf_file)
                try: 
                    reader = PdfReader(pdf_path)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()
                    content += text + "\n"
                except Exception as e:
                    st.error(f"Error reading {pdf_file}: {e}")

            if st.button("Generate Response"):
                prompt = (
                         "This is Text from a report. Give me all the Parameters with unique keys which can be plotted along with the "
                          "appropriate different plot type with the data to be plotted as a JSON like plaintext. Also provide me the "
                          "merit, demerit, and critical information of this college inside this JSON like plaintext and nothing else. "
                          "Output only valid JSON like plaintext without ```json block and without any explanations or extra text. "
                          "\n the response should be as JSON like plaintext without ```json block as:\n "
                          "{\n"
                          "  \"plots\": [\n"
                          "    {\"key\": \"<parameter_name>\", \"type\": \"<plot_type e.g. scatter, line bar, hist, pie, box, etc>\", \"data\": {\"x\": [], \"y\": []}},\n"
                          "    {\"key\": \"<parameter_name>\", \"type\": \"<plot_type e.g. scatter, line bar, hist, pie, box, etc>\", \"data\": {\"key1\": value1, \"key2\": value2}}\n"
                          "  ],\n"
                          "  \"merit\": [\"<merit1>\", \"<merit2>\", ...],\n"
                          "  \"demerit\": [\"<demerit1>\", \"<demerit2>\", ...],\n"
                          "  \"critical_information\": [\"<info1>\", \"<info2>\", ...]\n"
                          "}\n\n"
                          "Do not include explanations or any additional text outside valid JSON like plaintext without ```json block."
                          
                          )
                try:
                    response = model.generate_content(prompt + "\n" + content)
                    # st.write(response.text)
                    if response:
                        st.success("Response received. Parsing...")
                        raw_response = response.text.strip()
                        try: 
                            response_json = json.loads(raw_response)
                             
                            if "plots" in response_json:
                                plot_data(response_json["plots"])
                            else:
                                st.warning("No plot data found in the response.")
                            if "merit" in response_json:
                                st.subheader("Merits")
                                st.write("\n".join(f"- {item}" for item in response_json["merit"]))
                            if "demerit" in response_json:
                                st.subheader("Demerits")
                                st.write("\n".join(f"- {item}" for item in response_json["demerit"]))
                            if "critical_information" in response_json:
                                st.subheader("Critical Information")
                                st.write("\n".join(f"- {item}" for item in response_json["critical_information"]))

                        except json.JSONDecodeError as e:
                            st.error(f"Error decoding the response. Ensure the response is valid JSON. Error: {e}")
                    else:
                        st.error("Empty response from Gemini.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.write(f"No Data found for {selected_college}.")
