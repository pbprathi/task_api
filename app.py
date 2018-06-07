from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql://{username}:{password}@{hostname}/{databasename}".format(
    username="root",
    password="XXXX",
    hostname="localhost",
    databasename="todo",
)

app.config['SQLALCHEMY_DATABASE_URI']=SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)


class Tasks(db.Model):
    __tablename__ = 'tasks'
    task_id=db.Column(db.Integer,primary_key=True)
    taskname=db.Column(db.String(150))
    status=db.Column(db.Boolean)


#curl -i http://127.0.0.1:5000/createdb

@app.route('/createdb',methods=['GET'])
def create_db():
    db.create_all()
    return jsonify({'message':'Welcome'})


#curl -i http://127.0.0.1:5000/tasks


@app.route('/tasks',methods=['GET'])
def get_all_tasks():
    tasks=Tasks.query.all()
    output=[]
    for task in tasks:
        task_data={}
        task_data['task_id']=task.task_id
        task_data['taskname']=task.taskname
        task_data['status']=task.status
        output.append(task_data)
    return jsonify({'Tasks' : output})

#curl -i http://127.0.0.1:5000/task/1

@app.route('/task/<int:task_id>',methods=['GET'])
def get_task(task_id):
    task=Tasks.query.filter_by(task_id=task_id).first()
    if not task:
        return Jsonify({'Message' : 'Record Not Found.'})
    task_data={}
    task_data['task_id']=task.task_id
    task_data['taskname']=task.taskname
    task_data['status']=task.status
    return jsonify({'Task':task_data})

#curl -i -H "Content-Type: application/json" -X POST -d '{"taskname":"Read a book"}' http://127.0.0.1:5000/task

@app.route('/task',methods=['POST'])
def post_task():
    task_data=request.get_json()
    new_task=Tasks(taskname=task_data['taskname'],status=False)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'Message':'New task created.'})

#curl -i -X DELETE http://127.0.0.1:5000/task/2

@app.route('/task/<int:task_id>',methods=['DELETE'])
def delete_task(task_id):
    task=Tasks.query.filter_by(task_id=task_id).first()
    if not task:
        return jsonify({'Message':'Record not found.'})
    db.session.delete(task)
    db.session.commit()
    return jsonify({'Message':'Task Deleted.'})

#curl -i -H "Content-Type: application/json" -X PUT -d '{"id":"1","taskname":"Read a story book","status":"false"}' http://127.0.0.1:5000/task

@app.route('/task/<int:task_id>',methods=['PUT'])
def put_task(task_id):
    task_data=request.get_json()
    task=Tasks.query.filter_by(task_id=task_id).first()
    if not task:
        return jsonify({'Message':'Record not found.'})
    task.taskname=task_data['taskname']
    task.status=task_data['status']
    db.session.commit()
    return jsonify({'Message':'Task Updated'})


if __name__=='__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')
