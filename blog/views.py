from flask import render_template, request, redirect, url_for

from . import app
from .database import session, Entry

PAGINATE_BY = 10

@app.route('/')
@app.route('/page/<int:page>')
def entries(page=1):

    page_index = page - 1

    count = session.query(Entry).count()

    start = page_index * PAGINATE_BY
    end  = start + PAGINATE_BY

    total_pages = (count - 1) / PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    entries = session.query(Entry).order_by(Entry.datetime.desc())
    entries = entries[start:end]

    return render_template("entries.html",
        entries=entries,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )

@app.route("/entry/add", methods=["GET"]) #just get the template
def add_entry_get():
    return render_template("add_entry.html")

@app.route("/entry/add", methods=["POST"])
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))

@app.route("/entry/<int:id>", methods=["GET"])
def show_entry(id):
    entry = session.query(Entry).get(id)
    return render_template("show_entry.html", entry=entry)

@app.route("/entry/<int:id>/edit", methods=["GET"])
def edit_entry(id):
    entry = session.query(Entry).get(id)
    return render_template("edit_entry.html",
                            entry=entry)

@app.route("/entry/<int:id>/edit", methods=["POST"])
def edit_entry_post(id):
    entry = session.query(Entry).get(id)
    entry.title = request.form["title"]
    entry.content = request.form["content"]
    session.commit()
    return redirect(url_for('show_entry', id=entry.id))

@app.route("/entry/<int:id>/delete", methods=["GET", "POST"])
def delete_confirm(id):
    entry = session.query(Entry).get(id)
    if request.method == 'GET':
        return render_template("delete_confirm.html", id=entry.id)
    else:
        session.delete(entry)
        session.commit()
        return redirect(url_for('entries'))
