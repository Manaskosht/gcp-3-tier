from flask import Flask, render_template, request, redirect, session, url_for
from database.mongo import employees
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "admin123"


# ==========================
# Employee Registration Page
# ==========================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# Save Employee
# ==========================
@app.route("/add", methods=["POST"])
def add_employee():

    employees.insert_one({
        "name": request.form["name"],
        "father_name": request.form["father_name"],
        "mobile": request.form["mobile"],
        "email": request.form["email"],
        "qualification": request.form["qualification"],
        "address": request.form["address"]
    })

    return redirect("/")


# ==========================
# Admin Login Page
# ==========================
@app.route("/admin")
def admin():

    return render_template("admin_login.html")


# ==========================
# Login
# ==========================
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    if username == "admin" and password == "admin123":
        session["admin"] = True
        return redirect("/dashboard")

    return "Invalid Username or Password"


# ==========================
# Dashboard
# ==========================
@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/admin")

    data = employees.find()

    return render_template(
        "dashboard.html",
        employees=data,
        total=employees.count_documents({})
    )


# ==========================
# Delete Employee
# ==========================
@app.route("/delete/<id>")
def delete(id):

    if "admin" not in session:
        return redirect("/admin")

    employees.delete_one({"_id": ObjectId(id)})

    return redirect("/dashboard")


# ==========================
# Edit Employee
# ==========================
@app.route("/edit/<id>")
def edit(id):

    if "admin" not in session:
        return redirect("/admin")

    employee = employees.find_one({"_id": ObjectId(id)})

    return render_template("edit.html", employee=employee)


# ==========================
# Update Employee
# ==========================
@app.route("/update/<id>", methods=["POST"])
def update(id):

    if "admin" not in session:
        return redirect("/admin")

    employees.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "name": request.form["name"],
                "father_name": request.form["father_name"],
                "mobile": request.form["mobile"],
                "email": request.form["email"],
                "qualification": request.form["qualification"],
                "address": request.form["address"]
            }
        }
    )

    return redirect("/dashboard")


# ==========================
# Logout
# ==========================
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)