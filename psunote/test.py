import flask
import models
import forms

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "This is secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://coe:CoEpasswd@localhost:5432/coedb"

models.init_app(app)

@app.route("/")
def index():
    db = models.db
    notes = db.session.execute(
        db.select(models.Note).order_by(models.Note.title)
    ).scalars()
    return flask.render_template(
        "index.html",
        notes=notes,
    )

@app.route("/notes/create", methods=["GET", "POST"])
def notes_create():
    form = forms.NoteForm()
    if form.validate_on_submit():
        note = models.Note()
        form.populate_obj(note)
        note.tags = []

        db = models.db
        for tag_name in form.tags.data:
            tag = (
                db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
                .scalars()
                .first()
            )

            if not tag:
                tag = models.Tag(name=tag_name)
                db.session.add(tag)

            note.tags.append(tag)

        db.session.add(note)
        db.session.commit()
        flask.flash("สร้างโน้ตเรียบร้อยแล้ว!", "success")
        return flask.redirect(flask.url_for("index"))

    return flask.render_template(
        "notes-create.html",
        form=form,
    )

@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
def notes_edit(note_id):
    db = models.db
    note = db.session.execute(db.select(models.Note).where(models.Note.id == note_id)).scalars().first()

    if not note:
        flask.flash("ไม่พบโน้ต", "error")
        return flask.redirect(flask.url_for("index"))

    form = forms.NoteForm(obj=note)

    if form.validate_on_submit():
        form.populate_obj(note)
        note.tags = []

        for tag_name in form.tags.data:
            tag = db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name)).scalars().first()
            if not tag:
                tag = models.Tag(name=tag_name)
                db.session.add(tag)
            note.tags.append(tag)

        db.session.commit()
        flask.flash("แก้ไขโน้ตเรียบร้อยแล้ว!", "success")
        return flask.redirect(flask.url_for("index"))

    return flask.render_template("notes-edit.html", form=form, note=note)

@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def notes_delete(note_id):
    db = models.db
    note = db.session.execute(db.select(models.Note).where(models.Note.id == note_id)).scalars().first()

    if not note:
        flask.flash("ไม่พบโน้ต", "error")
    else:
        db.session.delete(note)
        db.session.commit()
        flask.flash("ลบโน้ตเรียบร้อยแล้ว!", "success")

    return flask.redirect(flask.url_for("index"))

@app.route("/tags/<tag_name>")
def tags_view(tag_name):
    db = models.db
    tag = (
        db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
        .scalars()
        .first()
    )
    if not tag:
        flask.flash("ไม่พบแท็ก", "error")
        return flask.redirect(flask.url_for("index"))

    notes = db.session.execute(
        db.select(models.Note).where(models.Note.tags.any(id=tag.id))
    ).scalars()

    return flask.render_template(
        "tags-view.html",
        tag_name=tag_name,
        notes=notes,
        tag=tag,
    )

@app.route("/tags/<int:tag_id>/edit", methods=["GET", "POST"])
def tag_edit(tag_id):
    db = models.db
    tag = db.session.execute(db.select(models.Tag).where(models.Tag.id == tag_id)).scalars().first()

    if not tag:
        flask.flash("ไม่พบแท็ก", "error")
        return flask.redirect(flask.url_for("index"))

    if flask.request.method == "POST":
        new_name = flask.request.form.get('name')
        if new_name:
            tag.name = new_name
            db.session.commit()
            flask.flash("แก้ไขแท็กเรียบร้อยแล้ว!", "success")
            return flask.redirect(flask.url_for("tags_view", tag_name=new_name))

    return flask.render_template("tag-edit.html", tag=tag)

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def tag_delete(tag_id):
    db = models.db
    tag = db.session.execute(db.select(models.Tag).where(models.Tag.id == tag_id)).scalars().first()

    if not tag:
        flask.flash("ไม่พบแท็ก", "error")
    else:
        db.session.delete(tag)
        db.session.commit()
        flask.flash("ลบแท็กเรียบร้อยแล้ว!", "success")

    return flask.redirect(flask.url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
