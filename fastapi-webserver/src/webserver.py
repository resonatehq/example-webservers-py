from resonate import Resonate, Context
from resonate.stores import LocalStore
from fastapi import FastAPI
import uvicorn

app = FastAPI()
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


@app.get("/")
def read_root():
    handle = foo.run("fastapi_webserver_foo_promise_id")
    return {"value": handle.result()}


def main() -> None:
    uvicorn.run(app)
