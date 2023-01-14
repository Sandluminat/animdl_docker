import subprocess
import streamlit as st
import re
import pathlib

download_path = "/download/"
call = "python runner.py "

st.set_page_config(page_title="animdl")
st.title("animdl")

tab1, tab2, tab3, tab4 = st.tabs(["download", "search", "List", "options"])

storage = []

def refresh():
    for x in pathlib.Path(download_path).glob("**/*"):
        outputting = []
        string = str(x)
        if string == "/download" or "DS_Store" in string:
            pass

        else:
            string = string[10:]
            if "/" in string:
                divider = string.find("/")
                beginning = string[:divider]
                number = str(x.stem)
                if number[1] == "0":
                    number = number[2:]
                else:
                    number = number[1:]

                if len(storage) == 0:
                    string = "python runner.py search "
                    string += f"'{beginning}'"
                    output = subprocess.run(string, shell=True, capture_output=True)
                    listings = re.findall(r'(https?://[^\s]+)', str(output))

                    for string in listings:
                        end = string.find("[")
                        outputting.append(string[0:(end-2)])

                    if "pip.pypa" in outputting[0]:
                        outputting.pop(0)
                    storage.append([beginning, [number], outputting[0]])

                else:
                    for i, title in enumerate(storage):
                        if title[0] == beginning:
                            i = title.index(beginning)
                            storage[i][1].append(number)

                        else:
                            string = "python runner.py search "
                            string += f"'{beginning}'"
                            output = subprocess.run(string, shell=True, capture_output=True)
                            listings = re.findall(r'(https?://[^\s]+)', str(output))

                            for string in listings:
                                end = string.find("[")
                                outputting.append(string[0:(end-2)])

                            if "pip.pypa" in outputting[0]:
                                outputting.pop(0)
                            storage.append([beginning, [number], outputting[0]])

def check_if_downloaded(link):
    if any(link in sublist for sublist in storage):
        for i, title in enumerate(storage):
            if title[2] == link:
                episodes = storage[i][1]
                downloading_episodes = ""
                if episodes[0] != str(1):
                    downloading_episodes += f"1-{episodes[0]},"
                for count, i in enumerate(episodes):
                    try:
                        if str(int(i)+1) == episodes[count+1]:
                            pass
                        elif str(int(i)+2) == episodes[count+1]:
                            downloading_episodes += f"{count+1},"
                        else:
                            downloading_episodes += f"{i}-{episodes[count+1]},"
                    except:
                        downloading_episodes += f"{str(int(i)+1)}-"
                st.write(f"downloading episodes: {downloading_episodes}")
                string = "python runner.py download "
                string += f"'{link}' -r {downloading_episodes} -d {download_path}"
                subprocess.run(string, shell=True)
                break
    else:
        string = "python runner.py download "
        string += f"{link} -d {download_path}"
        subprocess.run(string, shell=True, capture_output=True)


with tab1:
    txt = st.text_area("link of anime", height=300, max_chars=None)

    if txt == "":
        pass
    else:
        refresh()
        txt = txt.split(";")
        for line in txt:
            st.write("Starting...")
            check_if_downloaded(line.strip())
            st.write("...Done")

with tab2:
    txt = st.text_input("Name of anime", max_chars=None)
    if txt == "":
        pass
    else:
        refresh()
        outputting = [False]
        q = (call + "search '" + txt.strip() + "';")
        output = subprocess.run(q, shell=True, capture_output=True)
        beginning = re.findall(r'(https?://[^\s]+)', str(output))
        for string in beginning:
            end = string.find("[")
            outputting.append(string[0:(end-2)])
        if "pip.pypa" in outputting[1]:
            outputting.pop(1)
        download = st.selectbox("Do you want to download?", outputting)
        if not download:
            pass
        else:
            st.write("Starting...")
            check_if_downloaded(download.strip())
            st.write("...Done")

            
with tab3:
    st.write("The links might be wrong. No guarantee!!!")
    show_new_list = st.button("refresh downloaded series/episodes")
    if show_new_list:
        refresh()
    
    col1, col2, col3 = st.columns(3)
    col1.header("Title")
    col2.header("Link")
    col3.header("Episodes")
    for i in storage:
        col1.write(i[0])
        col2.write(i[2])
        string = ""
        for y in i[1]:
            string += f"{y}, "
        col3.write(string)

  
with tab4:
    passings = st.button("Change files from .txt to .mp4")
    if passings:
        for x in pathlib.Path(download_path).glob("**/*"):
            if x.suffix == ".txt":
                x.rename(x.with_suffix(".mp4"))
    txt = st.text_input("Download path (default = /download/)", max_chars=None)
    if txt == "":
        pass
    else:
        download_path = txt.strip()
