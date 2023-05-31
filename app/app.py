from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId



app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/flaskmongodb'

mongo = PyMongo(app)



@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.json['title']
    description = request.json['description']

    task = {
        'title': title,
        'description': description
    }

    result = mongo.db.tasks.insert_one(task)
    new_task = mongo.db.tasks.find_one({'_id': result.inserted_id})

    # Convertir el ObjectId a una cadena antes de serializar en JSON
    new_task['_id'] = str(new_task['_id'])

    return jsonify(new_task)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = mongo.db.tasks.find()
    result = []
    for task in all_tasks:
        result.append({
            'id': str(task['_id']),
            'title': task['title'],
            'description': task['description']
        })
    return jsonify(result)

@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = mongo.db.tasks.find_one({'_id': id})
    return jsonify(task)

@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    title = request.json['title']
    description = request.json['description']

    # Convertir la cadena 'id' en un objeto ObjectId
    task_id = ObjectId(id)

    mongo.db.tasks.update_one({'_id': task_id}, {'$set': {'title': title, 'description': description}})
    updated_task = mongo.db.tasks.find_one({'_id': task_id})

    # Convertir el ObjectId en una cadena antes de devolver la respuesta JSON
    updated_task['_id'] = str(updated_task['_id'])

    return jsonify(updated_task)

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    # Convertir la cadena 'id' en un objeto ObjectId
    task_id = ObjectId(id)

    deleted_task = mongo.db.tasks.find_one_and_delete({'_id': task_id})

    # Verificar si se encontró y eliminó la tarea
    if deleted_task:
        # Convertir el ObjectId en una cadena antes de devolver la respuesta JSON
        deleted_task['_id'] = str(deleted_task['_id'])
        return jsonify(deleted_task)
    else:
        return jsonify({'message': 'Task not found'})


if __name__ == '__main__':
    app.run(debug=True)


#without autentication in thiss case i use this
#docker run --name mymongo -p 27017:27017 -d mongo:latest

#with autentication
#docker run --name mymongo -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=mypassword -p 27017:27017 -d mongo:latest

#docker exec -it mymongo bash
#mongosh
#or if you want to connect to mongodb autentication
#mongosh --host localhost --port 27017 -u root -p mypassword --authenticationDatabase admin
#show dbs;
#use flaskmongodb;
#show collections;
#db.tasks.find().pretty();