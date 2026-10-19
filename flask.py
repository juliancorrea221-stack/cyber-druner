import datetime
import jwt
from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

SECRET_KEY = "cyber_drunners_secret_key"


users_db = {}


@app.route("/register", methods=["POST"])
def register():
  data = request.get_json()
  username = data.get("username")
  password = data.get("password")

  if username in users_db:
    return jsonify({"error": "El usuario ya existe"}), 400

  # Hashing seguro de la contraseña
  pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
  users_db[username] = pw_hash

  return jsonify({"message": "Usuario registrado exitosamente"}), 201


@app.route("/login", methods=["POST"])
def login():
  data = request.get_json()
  username = data.get("username")
  password = data.get("password")

  user_pw_hash = users_db.get(username)

  # Verificar existencia del usuario y contraseña
  if not user_pw_hash or not bcrypt.check_password_hash(
      user_pw_hash, password
  ):
    return jsonify({"error": "Credenciales inválidas"}), 401

  # Generar Token de acceso seguro (JWT) válido por 1 hora
  token = jwt.encode(
      {
          "username": username,
          "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
      },
      SECRET_KEY,
      algorithm="HS256",
  )

  return jsonify({"message": "Inicio de sesión exitoso", "token": token}), 200


if __name__ == "__main__":
  app.run(debug=True, port=5000)