import click
import importlib
import logging
import pkgutil
import redfishtool
from redfishtool.redfish.connector import BMCConfig, RedfishConnector


LOG = logging.getLogger(__name__)


@click.version_option(version=redfishtool.__version__, prog_name=redfishtool.__title__)
@click.group()
@click.option('-H', '--host', metavar='<ip>', required=True, help='Remote BMC host ip')
@click.option('-U', '--user', metavar='<username>', required=True, help='Remote BMC username')
@click.option('-P', '--password', metavar='<password>', required=True, help='Remote BMC password')
@click.pass_context
def cli(ctx, host, user, password):
    bmc_config = BMCConfig(host, user, password)
    LOG.debug(bmc_config)
    conn = RedfishConnector(bmc_config)

    root = conn.service_root
    print(f'Refish version: {root.version}')

    ctx.obj = conn


for _, name, _ in pkgutil.walk_packages(__path__, prefix=__name__ + "."):
    try:
        m = importlib.import_module(name)
        c = getattr(m, 'cli', lambda: None)
        cli.add_command(c)
    except AttributeError:
        pass
    except Exception as ex:
        # log warning
        LOG.exception(str(ex))
