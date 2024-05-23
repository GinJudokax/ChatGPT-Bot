from tkinter import *
import customtkinter
import openai
import os
import pickle
import requests
import json

# Initiate App
root = customtkinter.CTk()
root.title("ChatGPt.bot")
root.geometry('600x600')
root.iconbitmap("ai_lt.ico")  # https://tkinter.com/ai_lt.ico

# Set color scheme  
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Submit To ChatGPT
def speak():
    if chat_entry.get():
        # Define Filename
        filename = "api_key"
        try:
            if os.path.isfile(filename):
                # Open the file
                input_file = open(filename, "rb")

                # Load the data from the file into the variable 
                api_key = pickle.load(input_file)

                # Define the URL and headers for the request
                url = "https://api.openai.com/v1/chat/completions"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }

                # Define the data for the request
                data = {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": chat_entry.get()}
                    ]
                }

                # Send the POST request
                response = requests.post(url, headers=headers, data=json.dumps(data))

                # Check if the request was successful
                if response.status_code == 200:
                    response_data = response.json()
                    reply = response_data["choices"][0]["message"]["content"]
                    my_text.insert(END, reply)
                    my_text.insert(END, "\n\n")
                else:
                    my_text.insert(END, f"Error: {response.status_code}\n{response.text}\n\n")

            else:
                # Create the file 
                input_file = open(filename, "wb")
                # Close the file 
                input_file.close()
                # Error message - you need an API key
                my_text.insert(END, "\n\n You need an API key to talk with ChatGPT. Get one here:\n https://beta.openai.com/account/api-keys")

        except Exception as e:
            my_text.insert(END, f"There was an error\n\n{e}\n\n")

    else:
        my_text.insert(END, "\n\nHey! You Forgot To Type Anything!")

# Clear The Screens
def clear():
    # Clear The Main Text Box
    my_text.delete(1.0, END)
    # Clear The Query Entry Widget
    chat_entry.delete(0, END)

# Do API Stuff
def key():
    # Define Filename
    filename = "api_key"

    try:
        if os.path.isfile(filename):
            # Open the file
            input_file = open(filename, "rb")

            # Load the data from the file into the variable 
            stuff = pickle.load(input_file)

            # Output stuff to our entry box
            api_entry.insert(END, stuff)
        else:
            # Create the file 
            input_file = open(filename, "wb")
            # Close the file 
            input_file.close()

    except Exception as e:
        my_text.insert(END, f"There was an error\n\n{e}\n\n")

# Resize App Larger
    root.geometry('600x750')
    # Reshow API frame
    api_frame.pack(pady=30)

# Save The API Key
def save_key():
    # Define our file name
    filename = "api_key"

    try:
        # Open file 
        output_file = open(filename, "wb")

        # Actually add the data to the file 
        pickle.dump(api_entry.get(), output_file)

        # Delete Entry Box
        api_entry.delete(0, END)

        # Hide API Frame
        api_frame.pack_forget()
        # Resize App smaller
        root.geometry('600x600')

    except Exception as e:
        my_text.insert(END, f"There was an error\n\n{e}\n\n")

# Create Text Frame
text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)

# Add Text Widget To Get ChatGPT Responses
my_text = Text(text_frame,
    bg="#343638",
    width=65,
    bd=1,
    fg="#d6d6d6",  # inside text
    relief="flat",
    wrap=WORD,  # word wrap
    selectbackground="#1f538d")  # color of selected text
my_text.grid(row=0, column=0)

# Create Scrollbar for text widget
text_scroll = customtkinter.CTkScrollbar(text_frame,
    command=my_text.yview)
text_scroll.grid(row=0, column=1, sticky="ns")

# Add scrollbar to the textbox
my_text.configure(yscrollcommand=text_scroll.set)

# Entry Widget To Type Stuff to ChatGPT
chat_entry = customtkinter.CTkEntry(root,
    placeholder_text="Type Something To ChatGPT...",
    width=535,
    height=50,
    border_width=2)
chat_entry.pack(pady=10)

# Create Button Frame 
button_frame = customtkinter.CTkFrame(root, fg_color="#242424")
button_frame.pack(pady=10)

# Create Submit Button 
submit_button = customtkinter.CTkButton(button_frame,
    text="Speak To ChatGPT",
    command=speak)
submit_button.grid(row=0, column=0, padx=25)

# Create Clear Button
clear_button = customtkinter.CTkButton(button_frame,
    text="Clear Response",
    command=clear)
clear_button.grid(row=0, column=1, padx=35)

# Create API Button
API_button = customtkinter.CTkButton(button_frame,
    text="Update API Key",
    command=key)
API_button.grid(row=0, column=2, padx=25)

# Add API Key Frame
api_frame = customtkinter.CTkFrame(root, border_width=1)
api_frame.pack(pady=30)

# Add API Entry Widget
api_entry = customtkinter.CTkEntry(api_frame,
    placeholder_text="Enter Your API Key",
    width=350, height=50, border_width=1)
api_entry.grid(row=0, column=0, padx=20, pady=20)

# Add API Button
api_save_button = customtkinter.CTkButton(api_frame,
    text="Save Key",
    command=save_key)
api_save_button.grid(row=0, column=1, padx=10)

root.mainloop()


### Key Changes:
#1. **Importing `requests` and `json`**: Added at the top of the file.
#2. **Loading the API Key**: Correctly loading the API key from a file.
#3. **Defining the API Request**: Using the `v1/chat/completions` endpoint with the correct headers and data structure.
#4. **Handling the API Response**: Parsing and displaying the response correctly.
