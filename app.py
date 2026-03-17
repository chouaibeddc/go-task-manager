# Imports

from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#import sass : For Dev
import os

# APP
app = Flask(__name__)

# Compiling SCSS To CSS
# Use absolute paths for file operations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

"""
#  This code snippet are not for production

scss_path = os.path.join(BASE_DIR, "static/scss/styles.scss")
css_path = os.path.join(BASE_DIR, "static/css/styles.css")

if os.path.exists(scss_path):
    with open(scss_path, "r") as file_in:
        css = sass.compile(string=file_in.read(), output_style='compressed')
        with open(css_path, "w") as file_out:
            file_out.write(css)
            
"""

db_path = os.path.join(BASE_DIR, 'instance/database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Data Class
class MyTask(db.Model):
    id = db.Column(db.Integer ,primary_key=True )
    content = db.Column(db.String(100) , nullable=False)
    complete = db.Column(db.Integer , default=0)
    created = db.Column(db.DateTime  , default=datetime.utcnow)

    def __repr__(self):
        return f"Task {self.id}"

with app.app_context():
    db.create_all()
#Routes to webpages
# Home page
@app.route("/" , methods=['GET', 'POST'])
def index():
    # Ass a Task
    if request.method == 'POST':
        current_task = request.form['content']
        if not current_task:
            return redirect('/')
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f'ERROR: {e}')
            return f'ERROR: {e}'

    # See all current tasks
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()

        return render_template("index.html" , tasks=tasks)


# Delete an Item
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(f'ERROR: {e}')
        return f'ERROR: {e}'

# Edit an item
@app.route("/edit/<int:id>" , methods=['GET', 'POST'])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == 'POST':
        current_task = request.form['content']
        if not current_task:
            return redirect('/')
        task.content = current_task
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f'ERROR: {e}')
            return f'ERROR: {e}'
    else:
        return render_template('edit.html' , task=task)

if __name__ == "__main__":
    app.run(debug=True)