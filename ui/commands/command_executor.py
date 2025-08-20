import subprocess
import logging

logger = logging.getLogger(__name__)


class CommandExecutor:
    """Handles execution of terminal commands"""

    @staticmethod
    def execute(command: str) -> None:
        """Execute a terminal command"""
        try:
            subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True,
            )
        except subprocess.SubprocessError as e:
            logger.error(f"Error executing command '{command}': {e}")
            raise
