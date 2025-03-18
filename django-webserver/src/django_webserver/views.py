from resonate import Resonate, Context
from resonate.stores import LocalStore
from django.http import JsonResponse


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


def read_root(request):
    v = foo.run("django_webserver_foo_promise_id").result()
    return JsonResponse({"value": v})
