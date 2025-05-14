from flask import Flask, jsonify
from resonate import Resonate


app = Flask("flask-webserver")
resonate = Resonate.local()


def baz(_):
    print("running baz")
    return "hello world!"


def bar(ctx):
    print("running bar")
    result = yield ctx.lfc(baz)
    return result


@resonate.register
def foo(ctx):
    print("running foo")
    result = yield ctx.lfc(bar)
    return result


@app.route("/")
def read_root():
    handle = foo.run("flask_webserver_foo_promise_id")
    return jsonify({"value": handle.result()})


def main() -> None:
    app.run(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
