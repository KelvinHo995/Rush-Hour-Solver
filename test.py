import customtkinter as ctk

app = ctk.CTk()
text = ctk.StringVar(value="what's up")
button = ctk.CTkButton(app, textvariable=text)
button.pack()
button.setvar('text', '2')
print(text)
app.mainloop()