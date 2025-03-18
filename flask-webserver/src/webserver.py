from flask import Flask, jsonify
from resonate import Resonate, Context
from resonate.stores import LocalStore

app = Flask(__name__)
resonate = Resonate(store=LocalStore())


def baz(_: Context):
    return 1


def bar(ctx: Context):
    v = yield ctx.lfc(baz)
    return v + 1


@resonate.register
def foo(ctx: Context):
    v = yield ctx.lfc(bar)
    return v + 1


@app.route("/")
def read_root():
    handle = foo.run("flask_webserver_foo_promise_id")
    return jsonify({"value": handle.result()})


def main() -> None:
    app.run(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
