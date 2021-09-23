import click
from redfishtool.api import info as InfoApi
from .formatter import pretty_json


def model_to_dict(__list):
    return [_.to_dict() for _ in __list]


@click.group(name='info', help='Hardware Information')
@click.pass_context
def cli(ctx):
    pass


@cli.command(help='Show system information')
@click.pass_context
def system(ctx):
    conn = ctx.obj
    info = InfoApi.get_system_info(conn)

    print(pretty_json(info.to_dict()))


@cli.command(help='Show CPU information')
@click.pass_context
def cpu(ctx):
    conn = ctx.obj
    info = InfoApi.get_cpu_info(conn)

    print(pretty_json(model_to_dict(info)))


@cli.command(help='Show memory information')
@click.pass_context
def memory(ctx):
    conn = ctx.obj
    info, absent = InfoApi.get_memory_info(conn)

    print(pretty_json(model_to_dict(info)))
    print(pretty_json(absent))


@cli.command(help='Show storage information')
@click.pass_context
def storage(ctx):
    conn = ctx.obj
    info = InfoApi.get_storage_info(conn)

    print(pretty_json(model_to_dict(info)))


@cli.command(help='Show PCI information')
@click.pass_context
def pci(ctx):
    conn = ctx.obj
    info = InfoApi.get_pci_device_info(conn)

    print(pretty_json(model_to_dict(info)))
