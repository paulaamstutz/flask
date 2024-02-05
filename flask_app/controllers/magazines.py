from flask import flash, redirect, render_template, request, session

from flask_app import app
from flask_app.models.magazines import Magazine


@app.route("/magazines")
def magazines():
    if "user_id" in session:
        return render_template("magazines.html")
    return redirect("/")


@app.route("/magazines/new")
def addMagazine():
    if "user_id" in session:
        return render_template("addMagazine.html")

    return redirect("/")


@app.route("/magazine", methods=["POST"])
def createMagazine():
    if "user_id" not in session:
        return redirect("/")
    if not Magazine.validate_magazine(request.form):
        return redirect(request.referrer)
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "user_id": session["user_id"],  # id e personit te loguar
    }
    Magazine.create(data)
    return redirect("/")


@app.route("/magazine/<int:id>")
def viewMagazine(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"id": id, "magazine_id": id}
    magazine = Magazine.get_magazine_by_id(data)
    if magazine:
        usersWhoLikes = Magazine.get_users_who_liked_by_magazine_id(data)
        return render_template(
            "magazine.html", magazine=magazine, usersWhoLikes=usersWhoLikes
        )
    return redirect("/")


@app.route("/magazine/edit/<int:id>")
def editMagazine(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"id": id}
    magazine = Magazine.get_magazine_by_id(data)
    if magazine and magazine["user_id"] == session["user_id"]:
        return render_template("editmagazine.html", magazine=magazine)
    return redirect("/")


@app.route("/magazine/update/<int:id>", methods=["POST"])
def updateMagazine(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"id": id}
    magazine = Magazine.get_magazine_by_id(data)
    if magazine and magazine["user_id"] == session["user_id"]:
        if not Magazine.validate_magazineUpdate(request.form):
            return redirect(request.referrer)
        data = {
            "description": request.form["description"],
            "nrOfPages": request.form["nrOfPages"],
            "price": request.form["price"],
            "id": id,
        }
        Magazine.update(data)
        return redirect("/magazine/" + str(id))
    return redirect("/")


@app.route("/magazine/delete/<int:id>")
def deleteMagazine(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id,
    }
    magazine = Magazine.get_magazine_by_id(data)
    if magazine["user_id"] == session["user_id"]:
        Magazine.delete_all_magazine_comments(data)
        Magazine.delete(data)
    return redirect("/")


@app.route("/add/comment/<int:id>", methods=["POST"])
def addComment(id):
    if "user_id" not in session:
        return redirect("/")
    if len(request.form["comment"]) < 2:
        flash("The comment should be at least 2 characters", "comment")
    data = {
        "comment": request.form["comment"],
        "user_id": session["user_id"],
        "magazine_id": id,
    }
    Magazine.addComment(data)
    return redirect(request.referrer)


@app.route("/update/comment/<int:id>", methods=["POST"])
def updateComment(id):
    if "user_id" not in session:
        return redirect("/")
    if len(request.form["comment"]) < 2:
        flash("The comment should be at least 2 characters", "comment")
    data = {"comment": request.form["comment"], "id": id}
    comment = Magazine.get_comment_by_id(data)
    if comment["user_id"] == session["user_id"]:
        Magazine.update_comment(data)
    return redirect("/magazine/" + str(comment["magazine_id"]))


@app.route("/delete/comment/<int:id>")
def deleteComment(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"id": id}
    komenti = Magazine.get_comment_by_id(data)
    if komenti["user_id"] == session["user_id"]:
        Magazine.delete_comment(data)
    return redirect(request.referrer)


@app.route("/edit/comment/<int:id>")
def editComment(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"id": id}
    comment = Magazine.get_comment_by_id(data)
    if comment["user_id"] == session["user_id"]:
        return render_template("editComment.html", comment=comment)
    return redirect("/")


@app.route("/add/like/<int:id>")
def addLike(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"magazine_id": id, "user_id": session["user_id"]}
    usersWhoLikes = Magazine.get_users_who_liked_by_magazine_id(data)
    print(usersWhoLikes)
    if session["user_id"] not in usersWhoLikes:
        Magazine.addLike(data)
    return redirect(request.referrer)


@app.route("/remove/like/<int:id>")
def removeLike(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"magazine_id": id, "user_id": session["user_id"]}
    Magazine.removeLike(data)
    return redirect(request.referrer)
