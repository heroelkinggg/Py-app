import flet as ft
import sqlite3

# Database setup for students and marks
def setup_database():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    # Create students table with National ID
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            national_id TEXT NOT NULL
        )
    ''')

    # Create marks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject TEXT,
            mark INTEGER,
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')

    conn.commit()
    conn.close()

# Function to add a student
def add_student_to_db(name, email, phone, address, national_id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, email, phone, address, national_id) VALUES (?, ?, ?, ?, ?)", 
                   (name, email, phone, address, national_id))
    conn.commit()
    conn.close()

# Function to get a student's ID by name and phone
def get_student_id(name, phone):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM students WHERE name = ? AND phone = ?", (name, phone))
    student_id = cursor.fetchone()
    conn.close()
    return student_id[0] if student_id else None

# Function to get all students
def get_all_students():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Function to get the count of registered students
def get_registered_students_count():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Function to add marks to the database
def add_marks_to_db(student_id, subject, mark):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO marks (student_id, subject, mark) VALUES (?, ?, ?)", 
                   (student_id, subject, mark))
    conn.commit()
    conn.close()

# Login function
def login_action(username, password, page):
    if username == "hero" and password == "123456":
        page.snack_bar = ft.SnackBar(ft.Text("Welcome admin!"), open=True)
        # After successful login, show the student-teacher management system
        load_student_management_system(page)
    else:
        page.snack_bar = ft.SnackBar(ft.Text("Error: Incorrect username or password!"), open=True)

# Student view function to handle after the student login
def student_view(page: ft.Page):
    page.scroll = ft.ScrollMode.ALWAYS  # Enable scrolling for student view
    page.controls.clear()  # Clear the login page elements
    page.title = "Student View"

    # Header section for the student page
    header_image = ft.Image(src="home.gif", fit=ft.ImageFit.COVER, width=300, height=150)
    header_text = ft.Text("Student Portal", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_700)
    instructions = ft.Text("Please enter your information to view your marks.", size=16)

    # Input fields for student details
    input_width = 300
    name_field = ft.Row([
        ft.Icon(ft.icons.PERSON, size=24, color=ft.colors.BLUE_500),
        ft.TextField(label="Student Name", width=input_width)
    ])
    
    phone_field = ft.Row([
        ft.Icon(ft.icons.PHONE, size=24, color=ft.colors.BLUE_500),
        ft.TextField(label="Phone Number", width=input_width)
    ])

    email_field = ft.Row([
        ft.Icon(ft.icons.EMAIL, size=24, color=ft.colors.BLUE_500),
        ft.TextField(label="Student Email", width=input_width)
    ])

    address_field = ft.Row([
        ft.Icon(ft.icons.LOCATION_ON, size=24, color=ft.colors.BLUE_500),
        ft.TextField(label="Address", width=input_width)
    ])

    national_id_field = ft.Row([
        ft.Icon(ft.icons.CREDIT_CARD, size=24, color=ft.colors.BLUE_500),
        ft.TextField(label="National ID", width=input_width)
    ])

    # Function to display student marks
    def view_marks(e):
        student_name = name_field.controls[1].value
        student_phone = phone_field.controls[1].value
        student_email = email_field.controls[1].value
        student_address = address_field.controls[1].value
        student_national_id = national_id_field.controls[1].value

        # Get the student ID using name and phone number
        student_id = get_student_id(student_name, student_phone)

        if student_id is not None:
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            cursor.execute("SELECT subject, mark FROM marks WHERE student_id = ?", (student_id,))
            marks = cursor.fetchall()
            conn.close()

            total_marks = sum(mark[1] for mark in marks)
            result = "Success" if total_marks >= 30 else "Failed"
            display_text = f"Marks for {student_name}:\n"
            if marks:
                for mark in marks:
                    display_text += f"  {mark[0]}: {mark[1]}\n"
                display_text += f"Total Marks: {total_marks}\nResult: {result}\n"
            else:
                display_text += "No marks available.\nResult: Failed\n"
        else:
            display_text = "Student not found or no marks available."

        marks_display.value = display_text
        page.update()

    # Marks display section
    marks_display = ft.Text("", size=14, color=ft.colors.BLUE_500)

    # View marks button
    view_button = ft.ElevatedButton("View Marks", on_click=view_marks, bgcolor=ft.colors.BLUE_500, color=ft.colors.WHITE)

    # Back to Login button
    back_to_login_button = ft.ElevatedButton("Back to Login", on_click=lambda e: return_to_login(page), bgcolor=ft.colors.RED_500, color=ft.colors.WHITE)

    # Layout for student view
    page.add(
        ft.Column(
            controls=[
                header_image,    # Adding the GIF
                header_text,     # Adding title for the student portal
                instructions,
                name_field,
                phone_field,
                email_field,
                address_field,
                national_id_field,
                view_button,
                marks_display,
                back_to_login_button  # Add the back to login button here
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
    )
    page.update()

# Function to return to login page
def return_to_login(page: ft.Page):
    page.controls.clear()  # Clear everything on the current page
    page.update()  # Ensure the page is cleared before reloading the login system
    login_system(page)  # Reload the login system on a fresh page

# Modified login system function with "Enter as a student" button
def login_system(page: ft.Page):
    page.scroll = ft.ScrollMode.ALWAYS  # Enable scrolling

    # AppBar for login page
    page.appbar = ft.AppBar(
        title=ft.Text("Login System"),
        leading=ft.Icon(ft.icons.PERSON),
    )

    # TextFields for login
    username_field = ft.TextField(label="Email", hint_text="Enter your email")
    password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, hint_text="Enter your password")

    # Login button
    login_button = ft.ElevatedButton(
        text="Log in my Account Now !!",
        on_click=lambda e: login_action(username_field.value, password_field.value, page)
    )

    # New "Enter as a student" button
    student_login_button = ft.ElevatedButton(
        text="Enter as a student",
        on_click=lambda e: student_view(page)  # Direct the user to the student view
    )

    # Error/Success message area
    message_text = ft.Text("")

    # Add everything to the page
    page.add(
        ft.Column(
            [
                ft.Container(
                    ft.Image(src="path_to_profile_image.png", width=100, height=100),
                    alignment=ft.alignment.center,
                    padding=20
                ),
                ft.Text("Login System", size=24, weight="bold"),
                username_field,
                password_field,
                login_button,
                student_login_button,  # Added the new student button here
                message_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
    )

# Function to load student management system after login
def load_student_management_system(page: ft.Page):
    page.scroll = ft.ScrollMode.ALWAYS  # Enable scrolling for student management system
    page.controls.clear()  # Clear the login page elements
    page.title = "Student Management System"

    # Header section with centered GIF, title, and number of students
    header_image = ft.Image(src="home.gif", fit=ft.ImageFit.COVER, width=300, height=150)
    header_text = ft.Text("Teacher And Student Application", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_700)
    registered_students = ft.Text(f"Number Of Students : {get_registered_students_count()}", size=16, color=ft.colors.BLUE_500)

    header = ft.Column(
        controls=[header_image, header_text, registered_students],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Input Fields
    input_width = 300
    name_field = ft.Row([
        ft.Icon(ft.icons.PERSON, size=24, color=ft.colors.BLUE_500),
        ft.TextField(label="Student Name", width=input_width)
    ])

    email_field = ft.Row([
        ft.Icon(ft.icons.EMAIL, size=24, color=ft.colors.BLUE_500),
        ft.TextField(label="Student Email", width=input_width)
    ])

    phone_field = ft.Row([
        ft.Icon(ft.icons.PHONE, size=24, color=ft.colors.BLUE_500),
        ft.TextField(label="Phone Number", width=input_width)
    ])

    address_field = ft.Row([
        ft.Icon(ft.icons.LOCATION_ON, size=24, color=ft.colors.BLUE_500),
        ft.TextField(label="Address", width=input_width)
    ])

    national_id_field = ft.Row([
        ft.Icon(ft.icons.CREDIT_CARD, size=24, color=ft.colors.BLUE_500),
        ft.TextField(label="National ID", width=input_width)
    ])

    # Marks section title
    marks_title = ft.Text("Marks : ", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_500)

    # Marks input section
    subjects = ["French", "Math", "Arabic", "Chemistry", "English", "Art"]
    marks_input = ft.Column(spacing=10)
    for subject in subjects:
        marks_input.controls.append(ft.Row([
            ft.TextField(label=f"{subject} Mark", width=input_width),
            ft.TextButton("Save", on_click=lambda e, subj=subject: add_marks(e, subj, name_field, phone_field, page))
        ]))

    # Function to add marks for a student
    def add_marks(e, subject, name_field, phone_field, page):
        mark_value = e.control.parent.controls[0].value
        student_name = name_field.controls[1].value
        student_phone = phone_field.controls[1].value
        student_id = get_student_id(student_name, student_phone)

        if mark_value.isdigit() and student_id is not None:
            add_marks_to_db(student_id, subject, int(mark_value))
            e.control.parent.controls[0].value = ""
            page.update()
        else:
            print("Please provide valid marks and ensure the student exists.")

    # Function to add a student
    def add_student(e):
        name_value = name_field.controls[1].value
        email_value = email_field.controls[1].value
        phone_value = phone_field.controls[1].value
        address_value = address_field.controls[1].value
        national_id_value = national_id_field.controls[1].value

        if name_value and email_value and phone_value and address_value and national_id_value:
            add_student_to_db(name_value, email_value, phone_value, address_value, national_id_value)
            name_field.controls[1].value = ""
            email_field.controls[1].value = ""
            phone_field.controls[1].value = ""
            address_field.controls[1].value = ""
            national_id_field.controls[1].value = ""
            registered_students.value = f"Number Of Students : {get_registered_students_count()}"
            page.update()
        else:
            print("Please fill in all fields!")

    # Function to show students
    def show_students(e):
        students = get_all_students()
        page.controls.clear()

        student_grid = ft.GridView(expand=1, max_extent=400, padding=10, spacing=10)
        for student in students:
            student_id = student[0]
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            cursor.execute("SELECT subject, mark FROM marks WHERE student_id = ?", (student_id,))
            marks = cursor.fetchall()
            conn.close()

            total_marks = sum(mark[1] for mark in marks)
            result = "Success" if total_marks >= 30 else "Failed"
            display_text = f"Name: {student[1]}\nEmail: {student[2]}\nPhone: {student[3]}\nAddress: {student[4]}\nNational ID: {student[5]}\n"
            if marks:
                display_text += "Marks:\n"
                for mark in marks:
                    display_text += f"  {mark[0]}: {mark[1]}\n"
                display_text += f"Total Marks: {total_marks}\nResult: {result}\n"
            else:
                display_text += "No marks available.\nResult: Failed\n"

            student_display_card = ft.Card(
                content=ft.Container(
                    content=ft.Text(display_text, size=14, color=ft.colors.BLUE_500),
                    border_radius=10,
                    padding=10,
                    expand=True
                ),
                elevation=5,
                color=ft.colors.BLACK12,
                margin=10
            )
            student_grid.controls.append(student_display_card)

        page.add(student_grid)
        return_button = ft.ElevatedButton("Return to Main Menu", on_click=lambda e: load_student_management_system(page), bgcolor=ft.colors.RED_500, color=ft.colors.WHITE)
        page.add(return_button)
        page.update()

    # Back to Login button
    back_to_login_button = ft.ElevatedButton("Back to Login", on_click=lambda e: return_to_login(page), bgcolor=ft.colors.RED_500, color=ft.colors.WHITE)

    # Add and Show buttons
    add_button = ft.ElevatedButton("Add Student", on_click=add_student, bgcolor=ft.colors.BLUE_500, color=ft.colors.WHITE)
    show_button = ft.ElevatedButton("Show Students", on_click=show_students, bgcolor=ft.colors.BLUE_500, color=ft.colors.WHITE)

    # Main Layout
    page.add(
        ft.Column(
            controls=[
                header,
                name_field,
                email_field,
                phone_field,
                address_field,
                national_id_field,
                ft.Divider(),
                marks_title,
                marks_input,
                ft.Row([add_button, show_button], alignment=ft.MainAxisAlignment.CENTER),
                back_to_login_button  # Added Back to Login button here for the teacher's system
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    page.update()

# Main entry point
def main(page: ft.Page):
    page.title = "Login and Student Management App"
    page.scroll = ft.ScrollMode.ALWAYS  # Enable scrolling on the main page
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 10
    login_system(page)

# Set up the database and run the app
setup_database()
ft.app(target=main)
