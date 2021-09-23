import logging
import redfishtool
import redfishtool.cli as CLI
from redfishtool.settings import APP_SETTINGS as app
from redfishtool.utils import log

LOG = logging.getLogger(__name__)


class RedfishTool:
    @staticmethod
    def run():
        try:
            log.setup_logger(app.log_config)
            LOG.info('Start redfishtool')
            CLI.cli(prog_name=redfishtool.__title__)

        except Exception as e:
            LOG.exception(str(e))

        finally:
            pass
