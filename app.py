from flask import Flask, render_template, request, jsonify
from parser import analizar
from curp_utils import generar_curp, formatear_curp

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    curp_generada = None
    curp_formateada = None
    errores = []
    datos_validos = None

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido1 = request.form.get("apellido1", "").strip()
        apellido2 = request.form.get("apellido2", "").strip()
        fecha = request.form.get("fecha", "").strip()
        sexo = request.form.get("sexo", "").strip()
        estado = request.form.get("estado", "").strip()

        if not all([nombre, apellido1, apellido2, fecha, sexo, estado]):
            errores.append("Todos los campos son obligatorios")
        else:
            entrada = f"{nombre} {apellido1} {apellido2} {fecha} {sexo} {estado}"
            
            resultado, errores_parser = analizar(entrada)
            
            if errores_parser:
                errores = errores_parser
            elif resultado:
                try:
                    curp_generada = generar_curp(
                        resultado["nombre"],
                        resultado["apellido1"],
                        resultado["apellido2"],
                        resultado["fecha"],
                        resultado["sexo"],
                        resultado["estado"]
                    )
                    curp_formateada = formatear_curp(curp_generada)
                    datos_validos = resultado
                except Exception as e:
                    errores.append(f"Error al generar CURP: {str(e)}")

    return render_template(
        "index.html",
        curp=curp_generada,
        curp_formateada=curp_formateada,
        errores=errores,
        datos=datos_validos
    )

@app.route("/api/validar", methods=["POST"])
def api_validar():
    data = request.get_json()
    
    entrada = f"{data.get('nombre', '')} {data.get('apellido1', '')} {data.get('apellido2', '')} {data.get('fecha', '')} {data.get('sexo', '')} {data.get('estado', '')}"
    
    resultado, errores = analizar(entrada)
    
    return jsonify({
        "valido": len(errores) == 0,
        "errores": errores,
        "datos": resultado
    })

@app.route("/api/generar", methods=["POST"])
def api_generar():
    data = request.get_json()
    
    entrada = f"{data.get('nombre', '')} {data.get('apellido1', '')} {data.get('apellido2', '')} {data.get('fecha', '')} {data.get('sexo', '')} {data.get('estado', '')}"
    
    resultado, errores = analizar(entrada)
    
    if errores:
        return jsonify({
            "exito": False,
            "errores": errores
        }), 400
    
    try:
        curp = generar_curp(
            resultado["nombre"],
            resultado["apellido1"],
            resultado["apellido2"],
            resultado["fecha"],
            resultado["sexo"],
            resultado["estado"]
        )
        
        return jsonify({
            "exito": True,
            "curp": curp,
            "curp_formateada": formatear_curp(curp),
            "datos": resultado
        })
    except Exception as e:
        return jsonify({
            "exito": False,
            "errores": [f"Error al generar CURP: {str(e)}"]
        }), 500

if __name__ == "__main__":
    app.run(debug=False)