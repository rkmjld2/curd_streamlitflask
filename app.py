import streamlit as st
from db import get_connection


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Student CRUD",
    page_icon="🎓",
    layout="centered"
)


# ==========================================
# TITLE
# ==========================================

st.title("🎓 Student Management System")

st.subheader(
    "Python + Streamlit + Render + TiDB Cloud"
)


# ==========================================
# DATABASE READ
# ==========================================

def get_students():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, course
        FROM students
        ORDER BY id DESC
        """
    )

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    return records


# ==========================================
# CREATE
# ==========================================

def add_student(name, course):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO students
        (name, course)
        VALUES (%s, %s)
        """,
        (name, course)
    )

    connection.commit()

    cursor.close()
    connection.close()


# ==========================================
# UPDATE
# ==========================================

def update_student(student_id, name, course):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE students
        SET name = %s,
            course = %s
        WHERE id = %s
        """,
        (name, course, student_id)
    )

    connection.commit()

    cursor.close()
    connection.close()


# ==========================================
# DELETE
# ==========================================

def delete_student(student_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM students
        WHERE id = %s
        """,
        (student_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()


# ==========================================
# MENU
# ==========================================

menu = st.radio(
    "Select Operation",
    [
        "View Students",
        "Add Student",
        "Edit Student",
        "Delete Student"
    ],
    horizontal=True
)


# ==========================================
# VIEW
# ==========================================

if menu == "View Students":

    st.header("Student Records")

    try:

        students = get_students()

        if students:

            for student in students:

                st.write(
                    f"**ID:** {student[0]}  |  "
                    f"**Name:** {student[1]}  |  "
                    f"**Course:** {student[2]}"
                )

                st.divider()

        else:

            st.info(
                "No student records found."
            )

    except Exception as e:

        st.error(
            f"Database Error: {e}"
        )


# ==========================================
# ADD
# ==========================================

elif menu == "Add Student":

    st.header("Add Student")

    name = st.text_input(
        "Student Name"
    )

    course = st.text_input(
        "Course"
    )

    if st.button(
        "Save Student",
        type="primary"
    ):

        if not name.strip():

            st.warning(
                "Please enter student name."
            )

        elif not course.strip():

            st.warning(
                "Please enter course."
            )

        else:

            try:

                add_student(
                    name,
                    course
                )

                st.success(
                    "Student added successfully!"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Database Error: {e}"
                )


# ==========================================
# EDIT
# ==========================================

elif menu == "Edit Student":

    st.header("Edit Student")

    try:

        students = get_students()

        if not students:

            st.info(
                "No students available."
            )

        else:

            student_options = {
                f"{student[0]} - {student[1]}":
                student
                for student in students
            }

            selected = st.selectbox(
                "Select Student",
                list(student_options.keys())
            )

            student = student_options[
                selected
            ]

            student_id = student[0]

            name = st.text_input(
                "Student Name",
                value=student[1]
            )

            course = st.text_input(
                "Course",
                value=student[2]
            )

            if st.button(
                "Update Student",
                type="primary"
            ):

                if not name.strip():

                    st.warning(
                        "Please enter student name."
                    )

                elif not course.strip():

                    st.warning(
                        "Please enter course."
                    )

                else:

                    update_student(
                        student_id,
                        name,
                        course
                    )

                    st.success(
                        "Student updated successfully!"
                    )

                    st.rerun()

    except Exception as e:

        st.error(
            f"Database Error: {e}"
        )


# ==========================================
# DELETE
# ==========================================

elif menu == "Delete Student":

    st.header("Delete Student")

    try:

        students = get_students()

        if not students:

            st.info(
                "No students available."
            )

        else:

            student_options = {
                f"{student[0]} - {student[1]}":
                student[0]
                for student in students
            }

            selected = st.selectbox(
                "Select Student",
                list(student_options.keys())
            )

            student_id = student_options[
                selected
            ]

            if st.button(
                "Delete Student",
                type="primary"
            ):

                delete_student(
                    student_id
                )

                st.success(
                    "Student deleted successfully!"
                )

                st.rerun()

    except Exception as e:

        st.error(
            f"Database Error: {e}"
        )