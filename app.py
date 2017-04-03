from flask import *
app = Flask(__name__)
import mlab
from models.FoodItem import FoodItem
from models.user import User
import os
from werkzeug.utils import *
from flask_login import *
from sessionuser import SessionUser
mlab.connect()
app.config["UPLOAD_PATH"] = os.path.join(app.root_path, "upload")
if not os.path.exists(app.config["UPLOAD_PATH"]):
    os.makedirs(app.config["UPLOAD_PATH"])

app.secret_key = "himitsu"

login_manager = LoginManager()
login_manager.init_app(app)

# admin_user = User()
# admin_user.username = "admin"
# admin_user.password = "admin"
# admin_user.save()


# new_food = FoodItem()
# new_food.src = "http://cdn.dogbreedsdb.com/img/2016-11-20/corgi-11-1_1479648681136.jpg"
# new_food.title = "Item 5"
# new_food.discription = "Discription for Item 5"
# new_food.save()

# image_file = [
#     {
#         "src": "https://2982-presscdn-29-70-pagely.netdna-ssl.com/wp-content/uploads/2015/12/dog-sleeping-on-notebook.jpg"
#     },
#     {
#         "src": "https://2982-presscdn-29-70-pagely.netdna-ssl.com/wp-content/uploads/2015/12/dog-sleeping-on-notebook.jpg"
#     },
#     {
#         "src": "https://2982-presscdn-29-70-pagely.netdna-ssl.com/wp-content/uploads/2015/12/dog-sleeping-on-notebook.jpg"
#     }
# ]


@login_manager.user_loader
def user_loader(user_token):
    found_user = User.objects(token = user_token).first()
    if found_user:
        session_user = SessionUser(found_user)
        return session_user

@app.route('/')
def hello_world():
    return redirect(url_for("foodblog"))
number_visitor = 0

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        user = User.objects(username=request.form["username"]).first()
        if user and user.password == request.form["password"]:
            session_user = SessionUser(user.id)
            user.update(set__token = str(user.id))
            login_user(session_user)

            return redirect(url_for("add_food"))
        else:
            return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/addfood', methods = ["GET", "POST"])
@login_required
def add_food():
    if request.method == "GET":
        return render_template("addfood.html")
    if request.method == "POST":
        file = request.files["source"]
        if file:
            filename = secure_filename(file.filename)
            if os.path.exists(os.path.join(app.config["UPLOAD_PATH"], filename)):
                name_index = 0
                original_name = filename.rsplit(".", 1)[0]
                original_extension = filename.rsplit(".", 1)[1]
                while os.path.exists(os.path.join(app.config["UPLOAD_PATH"], filename)):
                    name_index +=1
                    filename = "{0} ({1}).{2}".format(original_name, name_index, original_extension)
            file.save(os.path.join(app.config["UPLOAD_PATH"], filename))


            new_food = FoodItem()

            new_food.title = request.form["title"]
            new_food.src = url_for("uploaded_file", filename = filename)
            # new_food.image = request.files["image"]
            new_food.discription = request.form["discription"]
            new_food.save()
            return render_template("addfood.html")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_PATH"], filename)

@app.route('/deletefood', methods = ["GET", "POST"])
def delete_food():
    if request.method == "GET":
        return render_template("deletefood.html")
    if request.method == "POST":
        new_food = FoodItem.objects(title=request.form["title"]).first()
        if new_food is not None:
            new_food.delete()
        return render_template("deletefood.html")

@app.route("/foodblog")
def foodblog():
    return render_template("foodblog.html", food_list = FoodItem.objects())



if __name__ == '__main__':
    app.run()
