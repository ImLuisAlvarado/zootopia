import os
import pymysql
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)


def get_connection():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        cursorclass=pymysql.cursors.DictCursor,
    )


def validar(form):
    """Limpia los datos del formulario y devuelve (datos, errores)."""
    datos = {
        "nombre": form.get("nombre", "").strip(),
        "especie": form.get("especie", "").strip(),
        "color": form.get("color", "").strip(),
        "edad": form.get("edad", "").strip(),
    }
    errores = []
    if not datos["nombre"]:
        errores.append("El nombre es obligatorio.")
    if not datos["especie"]:
        errores.append("La especie es obligatoria.")
    try:
        if int(datos["edad"]) < 0:
            raise ValueError
    except ValueError:
        errores.append("La edad debe ser un número entero mayor o igual a 0.")
    return datos, errores


def obtener_animal(animal_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre, especie, edad, color FROM animales WHERE id = %s",
                (animal_id,),
            )
            return cursor.fetchone()
    finally:
        conn.close()


@app.route('/')
@app.route('/animales')
def index():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre, especie, edad, color FROM animales ORDER BY id"
            )
            animales = cursor.fetchall()
    finally:
        conn.close()
    return render_template('index.html', animales=animales)


@app.route('/animales/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        datos, errores = validar(request.form)
        if errores:
            return render_template('form.html', titulo="Nuevo animal",
                                   animal=datos, errores=errores)
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO animales (nombre, especie, color, edad) "
                    "VALUES (%s, %s, %s, %s)",
                    (datos["nombre"], datos["especie"], datos["color"], int(datos["edad"])),
                )
            conn.commit()
        finally:
            conn.close()
        return redirect(url_for('index'))
    return render_template('form.html', titulo="Nuevo animal", animal={}, errores=[])



@app.route('/animales/<int:animal_id>/editar', methods=['GET', 'POST'])
def editar(animal_id):
    animal = obtener_animal(animal_id)
    if animal is None:
        abort(404)

    if request.method == 'POST':
        datos, errores = validar(request.form)
        if errores:
            return render_template('form.html', titulo="Editar animal",
                                   animal=datos, errores=errores)
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE animales SET nombre=%s, especie=%s, color=%s, edad=%s "
                    "WHERE id=%s",
                    (datos["nombre"], datos["especie"], datos["color"],
                     int(datos["edad"]), animal_id),
                )
            conn.commit()
        finally:
            conn.close()
        return redirect(url_for('index'))
    return render_template('form.html', titulo="Editar animal", animal=animal, errores=[])


# DELETE
@app.route('/animales/<int:animal_id>/eliminar', methods=['POST'])
def eliminar(animal_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM animales WHERE id = %s", (animal_id,))
        conn.commit()
    finally:
        conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)