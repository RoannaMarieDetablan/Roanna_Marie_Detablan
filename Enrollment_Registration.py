from tkinter import *
import sqlite3

# Function called when Edit button is pressed
def edit():
    # Create a new window for editing
    editor = Tk()
    editor.title('Edit Enrollment Record')
    editor.geometry("500x500")
    editor.config(bg="sky blue")
    
    conn = sqlite3.connect('D:/Final_Python/Enrollment.db')
    c = conn.cursor()

    record_id = delete_box.get()

    if not record_id.isdigit():
        error_label = Label(editor, text="Please enter a valid ID number.", bg="sky blue", font=("Arial Black", 12, "bold"))
        error_label.grid(row=0, column=0, columnspan=2)
        return

    c.execute("SELECT * FROM enrollment_database WHERE oid=?", (record_id,))
    record = c.fetchone()

    if not record:
        error_label = Label(editor, text="Record not found!", bg="sky blue", font=("Arial Black", 12, "bold"))
        error_label.grid(row=0, column=0, columnspan=2)
        return

    # Entry and Label for Edit when pressed    
    name_editor = Entry(editor, width=30)
    name_editor.grid(row=0, column=1, pady=(10, 0))
    name_editor.insert(0, record[0])  

    name_label = Label(editor, text="Name", bg="sky blue", font=("Arial Black", 12, "bold"))
    name_label.grid(row=0, column=0, padx=10, pady=(10, 0))

    address_editor = Entry(editor, width=30)
    address_editor.grid(row=1, column=1, pady=(10, 0))
    address_editor.insert(0, record[1]) 

    address_label = Label(editor, text="Address", bg="sky blue", font=("Arial Black", 12, "bold"))
    address_label.grid(row=1, column=0, padx=10, pady=(10, 0))

    year_level_editor = Entry(editor, width=30)
    year_level_editor.grid(row=2, column=1, pady=(10, 0))
    year_level_editor.insert(0, record[2])  

    year_level_label = Label(editor, text="Year Level", bg="sky blue", font=("Arial Black", 12, "bold"))
    year_level_label.grid(row=2, column=0, padx=10, pady=(10, 0))

    date_of_birth_editor = Entry(editor, width=30)
    date_of_birth_editor.grid(row=3, column=1, pady=(10, 0))
    date_of_birth_editor.insert(0, record[3]) 

    date_of_birth_label = Label(editor, text="Date Of Birth", bg="sky blue", font=("Arial Black", 12, "bold"))
    date_of_birth_label.grid(row=3, column=0, padx=10, pady=(10, 0))

    age_editor = Entry(editor, width=30)
    age_editor.grid(row=4, column=1, pady=(10, 0))
    age_editor.insert(0, record[4])  

    age_label = Label(editor, text="Age", bg="sky blue", font=("Arial Black", 12, "bold"))
    age_label.grid(row=4, column=0, padx=10, pady=(10, 0))

    email_editor = Entry(editor, width=30)
    email_editor.grid(row=5, column=1, pady=(10, 0))
    email_editor.insert(0, record[5])  

    email_label = Label(editor, text="Email", bg="sky blue", font=("Arial Black", 12, "bold"))
    email_label.grid(row=5, column=0, padx=10, pady=(10, 0))

    course_editor = Entry(editor, width=30)
    course_editor.grid(row=6, column=1, pady=(10, 0))
    course_editor.insert(0, record[6])  

    course_label = Label(editor, text="Course", bg="sky blue", font=("Arial Black", 12, "bold"))
    course_label.grid(row=6, column=0, padx=10, pady=(10, 0))


    # Function Called when Save Changes is pressed
    def save_update():
        updated_name = name_editor.get()
        updated_address = address_editor.get()
        updated_year_level = year_level_editor.get()
        updated_date_of_birth = date_of_birth_editor.get()
        updated_age = age_editor.get()
        updated_email = email_editor.get()
        updated_course = course_editor.get()

        c.execute('''UPDATE enrollment_database SET
                        name = ?, address = ?, year_level = ?, date_of_birth = ?, age = ?, email = ?, course = ? WHERE oid = ?''', 
                  (updated_name, updated_address, updated_year_level, updated_date_of_birth, updated_age, updated_email, updated_course, record_id))

        conn.commit()
        conn.close()

        editor.destroy()

        query()

    # Button for Save Changes
    save_btn = Button(editor, text="Save Changes", command=save_update, bg="lightgray", font=("Arial Black", 12, "bold"))
    save_btn.grid(row=7, column=0, columnspan=2, pady=20, padx=10, ipadx=104)

    editor.mainloop()

# Function Called when Add Record is pressed    
def submit():
    conn = sqlite3.connect('D:/Final_Python/Enrollment.db')
    c = conn.cursor()

    c.execute("INSERT INTO enrollment_database VALUES (:name, :address, :year_level, :date_of_birth, :age, :email, :course)",
              {
                'name': name.get(),
                'address': address.get(),
                'year_level': year_level.get(),
                'date_of_birth': date_of_birth.get(),
                'age': age.get(),
                'email': email.get(),
                'course': course.get(),
              })
    
    conn.commit()
    conn.close()

    name.delete(0, END)
    address.delete(0, END)
    year_level.delete(0, END)
    date_of_birth.delete(0, END)
    age.delete(0, END)
    email.delete(0, END)
    course.delete(0, END)

# Function Called when Show Record is Pressed
def query():
    conn = sqlite3.connect('D:/Final_Python/Enrollment.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM enrollment_database")
    records = c.fetchall()
    conn.close()

    # Remove previous query display (if any)
    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) >= 12:
            widget.grid_forget()

    # Create a Text widget to display the records
    query_text = Text(root, height=20, width=40, wrap=WORD, bg="lightgrey", font=("Arial", 9), state=DISABLED)
    query_text.grid(row=12, column=0, columnspan=2, padx=20, pady=10)

    # Insert records into the Text widget
    query_text.config(state=NORMAL)  # Enable editing temporarily to insert text
    print_records = ""
    for record in records:
        print_records += f"☘︎\n\tName: {record[0]}\n\tAddress: {record[1]}\n\tYear level: {record[2]}\n\tDate of birth: {record[3]}\n\tAge: {record[4]}\n\tEmail: {record[5]} \n\tCourse: {record[6]} \n\tEnrollment ID: {record[7]}\n________________________________________\n"
    query_text.insert(END, print_records)
    query_text.config(state=DISABLED)  # Disable editing to make it read-only


# Function Called when Button Delete is Pressed    
def delete():
    conn = sqlite3.connect('D:/Final_Python/Enrollment.db')
    c = conn.cursor()
    c.execute("DELETE FROM enrollment_database WHERE oid=?", (delete_box.get(),))
    conn.commit()

    delete_box.delete(0, END)

    conn.close()

    query()

root = Tk() 
root.title('Enrollment Registration Database')
root.geometry("500x1000")
root.config(bg="sky blue")

# Entry
name = Entry(root, width=30)
name.grid(row=0, column=1, padx=20)

address = Entry(root, width=30)
address.grid(row=1, column=1, padx=20)

year_level = Entry(root, width=30)
year_level.grid(row=2, column=1, padx=20)

date_of_birth = Entry(root, width=30)
date_of_birth.grid(row=3, column=1, padx=20)

age = Entry(root, width=30)
age.grid(row=4, column=1, padx=20)

email = Entry(root, width=30)
email.grid(row=5, column=1, padx=20)

course = Entry(root, width=30)
course.grid(row=6, column=1, padx=20)

# Label
name_label = Label(root, text=" Name", bg="sky blue", font=("Arial Black", 12, "bold"))
name_label.grid(row=0, column=0)

address_label = Label(root, text="Address", bg="sky blue", font=("Arial Black", 12, "bold"))
address_label.grid(row=1, column=0)

year_level_label = Label(root, text="Year Level", bg="sky blue", font=("Arial Black", 12, "bold"))
year_level_label.grid(row=2, column=0)   

date_of_birth_label = Label(root, text="Date Of Birth", bg="sky blue", font=("Arial Black", 12, "bold"))
date_of_birth_label.grid(row=3, column=0)

age_label = Label(root, text="Age", bg="sky blue", font=("Arial Black", 12, "bold"))
age_label.grid(row=4, column=0)

email_label = Label(root, text="Email", bg="sky blue", font=("Arial Black", 12, "bold"))
email_label.grid(row=5, column=0)

course_label = Label(root, text="Course", bg="sky blue", font=("Arial Black", 12, "bold"))
course_label.grid(row=6, column=0)

# Delete Entry & Label
delete_box = Entry(root, width=30)
delete_box.grid(row=10, column=1, padx=30)

delete_box_label = Label(root, text="Select Registration No.", bg="sky blue", font=("Arial Black", 12, "bold"))
delete_box_label.grid(row=10, column=0)

# Submit, Show Record, Delete, Edit Button
submit_btn = Button(root, text="Add Registration for Enrollment", command=submit, bg="lightgray", font=("Arial Black", 12, "bold"))
submit_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=30)

query_btn = Button(root, text="Show Enrollment Registered", command=query, bg="lightgray", font=("Arial Black", 12, "bold"))
query_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=30)

delete_btn = Button(root, text="Delete Enrollment Registered", command=delete, bg="lightgray", font=("Arial Black", 12, "bold"))
delete_btn.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=30)

update_btn = Button(root, text="Edit Existing Enrollment Record", command=edit, bg="lightgray", font=("Arial Black", 12, "bold"))
update_btn.grid(row=13, column=0, columnspan=2, pady=10, padx=10, ipadx=30)

# Text widget to show records
query_text = Text(root, width=50, height=20, bg="light gray", font=("Arial", 10))
query_text.grid(row=30, column=0, columnspan=2, padx=20, pady=10)

root.mainloop()
