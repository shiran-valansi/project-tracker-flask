"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/")
def display_homepage():
	"""Display list of students and projects"""

	students = hackbright.return_students()
	projects = hackbright.return_projects()

	return render_template("homepage.html", students=students, projects=projects)

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    grades = hackbright.get_grades_by_github(github)

    # return "{} is the GitHub account for {} {}".format(github, first, last)
    return render_template("student_info.html", first=first,
    											last=last,
    											github=github,
    											grades=grades)

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/add-a-student")
def get_student_info():
	"""Show form to add a student name."""

	return render_template("student_add.html")


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""

    first_name = request.form.get('fname')
    last_name = request.form.get('lname')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("student_added.html", first=first_name,
    											 last=last_name,
    											 git=github)

@app.route("/project")
def show_project_info():
	""""""

	title = request.args.get('title')
	
	title, description, max_grade  = hackbright.get_project_by_title(title)
	grades = hackbright.get_grades_by_title(title)

	return render_template("project_info.html",
							title=title,
							description=description,
							max_grade=max_grade,
							grades=grades)



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
