import click
import json
from redfishtool.api import bios as BiosApi
from .formatter import pretty_json


@click.group(name='bios', help='Bios configuration')
@click.pass_context
def cli(ctx):
    pass


@cli.command(help='List current bios setting')
@click.option('-f', '--filepath', help='Write to JSON file')
@click.option('-k', '--keyword', help='Filter by keyword')
@click.option('-v', '--verbose', is_flag=True, help='Show detail')
@click.pass_context
def list(ctx, filepath, keyword, verbose):
    conn = ctx.obj

    s = BiosApi.get_bios_setting(conn, hii=True, filter_args=keyword, verbose=verbose)

    if filepath:
        with open(filepath, 'w') as fp:
            fp.write(pretty_json(s))
    else:
        print(pretty_json(s))


@cli.command(help='Dump bios setting')
@click.option('-f', '--filepath', help='Write to JSON file')
@click.pass_context
def dump(ctx, filepath):
    conn = ctx.obj

    s = BiosApi.get_bios_setting(conn)

    if filepath:
        with open(filepath, 'w') as fp:
            fp.write(pretty_json(s))
    else:
        print(pretty_json(s))


@cli.command(help='Update bios setting')
@click.option('-f', '--filepath', required=True, type=click.Path(exists=True), help='Bios setting in JSON format')
@click.pass_context
def update(ctx, filepath):
    with open(filepath, 'r') as f:
        new_settings = json.load(f)

    conn = ctx.obj
    BiosApi.update_bios_setting(conn, new_settings)


@cli.command(help='Show bios pending setting')
@click.pass_context
def pending(ctx):
    conn = ctx.obj
    s = BiosApi.get_bios_pending_setting(conn)
    print(pretty_json(s))


@cli.command(help='Undo bios pending setting')
@click.pass_context
def undo(ctx):
    conn = ctx.obj
    BiosApi.undo_bios_pending_setting(conn)
