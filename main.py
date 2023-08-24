from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

#cadena de conexion
mysqlConnection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="project_db"
)
cursor = mysqlConnection.cursor(dictionary=True)

@app.route('/', methods=['GET'])
def helloWorld():
    response={
        "message": "Hello World"
    }
    return jsonify(response)

@app.route('/natalia', methods=['GET'])
def helloNatalia():
    response={
        "message": "Hello Natalia"
    }
    return jsonify(response)

@app.route('/users', methods=['GET'])
def getUsers():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify(users)

@app.route('/users', methods=['POST'])
def createUser():
    data = request.get_json()
    name = data['name']
    password = data['password']
    email = data['email']
    nickname = data['nickname']
    cursor.execute("INSERT INTO users (name, password, email, nickname) VALUES (%s, %s, %s, %s)",
                   (name, password, email, nickname))
    mysqlConnection.commit()
    return jsonify({"message": "User created successfully"})

@app.route('/users/<int:userId>', methods=['GET'])
def getUser(userId):
    #seleccione todos los usuarios donde el id sea userId
    cursor.execute("SELECT * FROM users WHERE id = %s", (userId,))
    user = cursor.fetchone()
    return jsonify(user)

@app.route('/users/<int:userId>', methods=['PUT'])
#necesito el identificador para saber que actualizo y tambien necesito el body con la informacion que voy a actualizar
def updateUser(userId):
    #leeo el body
    data = request.get_json()
    name = data['name']
    password = data['password']
    email = data['email']
    nickname = data['nickname']
    #actualice en  la tabla usuarios y haga un seteo de name y cambielo por .. donde el id sea tal
    cursor.execute("UPDATE users SET name = %s, password = %s, email =%s, nickname = %s WHERE id = %s",
    #se cambia por lo que llega aca
    (name, password, email, nickname, userId))
    #se manda la conexion
    mysqlConnection.commit()
    return jsonify({"message": "User updated successfully"})

#Eliminar usuario por ID
#siempre se manipula por id
@app.route('/users/<int:userId>', methods=['DELETE'])
def deleteUser(userId):
    #borreme de las tabla usuarios en la que el id es
    cursor.execute("DELETE FROM users WHERE id = %s", (userId,))
    mysqlConnection.commit()
    return jsonify({"message": "User deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)
