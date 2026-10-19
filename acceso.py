def token_required(f):

  def decorator(*args, **kwargs):
    token = request.headers.get("Authorization")
    if not token:
      return jsonify({"error": "Token de autenticación requerido"}), 401
    try:
      data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
      current_user = data["username"]
    except:
      return jsonify({"error": "Token inválido o expirado"}), 401
    return f(current_user, *args, **kwargs)

  return decorator


@app.route("/protected-hub", methods=["GET"])
@token_required
def protected_hub(current_user):
  return jsonify(
      {"message": f"Bienvenido al área segura del Hub, {current_user}!"}
  )