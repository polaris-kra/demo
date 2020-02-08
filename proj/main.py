from flask import jsonify, render_template, request
from core.server import DemoServer


server = DemoServer()
app = server.create()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/classify", methods=["GET"])
def classify():
    if request.method == "GET":
        return render_template("classify.html")


@app.route("/classify_ajax", methods=["POST"])
def classify_ajax():
    if "img" not in request.files:
        raise Exception('ERROR: no image')

    image = request.files["img"]
    result = server.classify(image)

    return jsonify(result=result)


if __name__ == "__main__":
    server.run()
