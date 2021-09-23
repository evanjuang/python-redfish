import click
from .formatter import pretty_json


@click.group(name='redfish', help='Redfish resource')
@click.pass_context
def cli(ctx):
    pass


@cli.command('invoke', help='Invoke Redfish API')
@click.argument('path')
@click.option('-m', 'method', default='get', type=click.Choice(['get', 'post', 'patch']), help='HTTP method')
@click.option('-d', 'body', help='Request body')
@click.pass_context
def invoke(ctx, path, method, body):
    conn = ctx.obj

    data = {}
    if method == 'get':
        data = conn.get(path)
    elif method == 'post':
        data = conn.patch(path, body)
    elif method == 'patch':
        data = conn.patch(path, body)

    print(pretty_json(data))


@cli.group(invoke_without_command=True, help='Show system resource')
@click.pass_context
def system(ctx):
    conn = ctx.obj
    root = conn.service_root
    sys = root.get_system()

    ctx.obj = sys

    print(pretty_json(sys.data))


@system.command('proc', help='Show processor resource')
@click.pass_context
def processor(ctx):
    sys = ctx.obj
    res_col = sys.get_processor_collection()

    data = []
    for res in res_col.member_resources():
        data.append(res.data)

    print(pretty_json(data))


@system.command('mem', help='Show memory resource')
@click.pass_context
def memory(ctx):
    sys = ctx.obj
    res_col = sys.get_memory_collection()

    data = []
    for res in res_col.member_resources():
        data.append(res.data)

    print(pretty_json(data))


@system.command('storage', help='Show storage resource')
@click.pass_context
def storage(ctx):
    sys = ctx.obj
    stor_col = sys.get_storage_collection()

    data = []
    for stor in stor_col.get_storage():
        stor_data = {}
        stor_data['Storage'] = stor.data
        stor_data['Drives'] = [d.data for d in stor.get_drive()]

        data.append(stor_data)

    print(pretty_json(data))


@cli.command('chassis', help='Show chassis resource')
@click.pass_context
def chassis(ctx):
    conn = ctx.obj
    root = conn.service_root

    print(root.get_chassis().json)


@cli.command('manager', help='Show manager resource')
@click.pass_context
def manager(ctx):
    conn = ctx.obj
    root = conn.service_root

    print(root.get_manager().json)
