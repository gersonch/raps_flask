from flask import Blueprint, render_template, request

bp = Blueprint("pages", __name__)

USUARIOS = {
    "juan": {"password": "admin", "rol": "administrador"},
    "pepe": {"password": "user", "rol": "usuario"},
}

PRECIO_TARRO = 9000


def _calcular_descuento(edad: int) -> int:
    if 18 <= edad <= 30:
        return 15
    if edad > 30:
        return 25
    return 0


@bp.route("/")
def home():
    return render_template("pages/home.html")


@bp.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    resultado = None
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        try:
            edad = int(request.form.get("edad", ""))
            cantidad = int(request.form.get("cantidad", ""))
        except ValueError:
            return render_template(
                "pages/ejercicio1.html",
                error="Edad y cantidad deben ser números enteros.",
            )

        if edad < 0 or cantidad < 0:
            return render_template(
                "pages/ejercicio1.html",
                error="Edad y cantidad deben ser valores positivos.",
            )

        total_sin_descuento = PRECIO_TARRO * cantidad
        descuento_pct = _calcular_descuento(edad)
        total_con_descuento = total_sin_descuento * (1 - descuento_pct / 100)

        resultado = {
            "nombre": nombre,
            "edad": edad,
            "cantidad": cantidad,
            "total_sin_descuento": total_sin_descuento,
            "descuento_pct": descuento_pct,
            "total_con_descuento": total_con_descuento,
        }

    return render_template("pages/ejercicio1.html", resultado=resultado)


@bp.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    mensaje = None
    exito = False
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip().lower()
        password = request.form.get("password", "")

        datos = USUARIOS.get(usuario)
        if datos and datos["password"] == password:
            mensaje = f"Bienvenido {datos['rol']} {usuario}"
            exito = True
        else:
            mensaje = "Usuario o contraseña incorrectos."

    return render_template(
        "pages/ejercicio2.html", mensaje=mensaje, exito=exito
    )
