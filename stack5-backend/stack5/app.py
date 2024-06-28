#!/usr/bin/env python
# coding : utf-8
import os 

from flask import Flask, render_template, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/task'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tache = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, tache, date=None):
        self.tache = tache
        if date is None:
            date = datetime.utcnow()
        self.date = date

@app.route('/tasks', methods = ['GET'])
def get_tasks():
    task = Task.query.all()
    return jsonify([{'id': task.id, 'tache': task.tache, 'date': task.date} for task in task])


@app.route('/tasks', methods = ['POST'])
def add_task():
    data = request.json

    my_data = Task(tache=data['tache'])
    db.session.add(my_data)
    db.session.commit()

    return jsonify({'message': 'Task added successfully'})


@app.route('/update/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.json
    task = Task.query.get(id)
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    if 'tache' not in data:
        return jsonify({'message': 'No task data provided'}), 400

    task.tache = data['tache']
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, host='0.0.0.0', port=5000)