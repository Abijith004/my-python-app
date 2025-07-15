from flask import Flask, render_template, request, jsonify
from sympy import symbols, limit, diff, sympify

app = Flask(__name__)

x = symbols('x')

# Web route for HTML UI
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        func = request.form["function"]
        option = request.form["operation"]
        expr = sympify(func)

        if option == "derivative":
            result = diff(expr, x)
        elif option == "limit":
            point = float(request.form["point"])
            result = limit(expr, x, point)

    return render_template("index.html", result=result)


# ✅ API route for JSON input (Postman or other prompts)
@app.route("/api/calculate", methods=["POST"])
def api_calculate():
    data = request.json
    try:
        func = data.get("function")
        operation = data.get("operation")
        expr = sympify(func)

        if operation == "derivative":
            result = str(diff(expr, x))
        elif operation == "limit":
            point = float(data.get("point", 0))
            result = str(limit(expr, x, point))
        else:
            return jsonify({"error": "Invalid operation"}), 400

        return jsonify({
            "function": func,
            "operation": operation,
            "result": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
