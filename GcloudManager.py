"""
Operations over configurations of gcloud utility
"""
from dataclasses import dataclass
from json import loads
from subprocess import check_output
from typing import Optional, List, Any, Dict

from singleton_decorator import singleton

from gubert.utils import VersionTuple


@dataclass
class GcloudConfiguration(object):
    """
    Basic information about gcloud configuration
    """
    name: str
    is_active: bool
    account: str
    project: Optional[str]
    properties: Dict[str, Any]


@singleton
class GcloudManager(object):
    """
    Operations over configurations of gcloud utility
    """

    def __init__(self, verbose: bool = False,
                 timeout: int = 10) -> None:
        super().__init__()
        self.timeout = timeout
        self.version = self._get_gcloud_version()
        if verbose:
            print(f"Gcloud version discovered: {self.version}")
        self._check_gcloud_version()

    def _check_gcloud_version(self) -> None:
        if self.version < (200, 0, 0):
            raise RuntimeError(
                "Your gcloud version is older than required! "
                "Minimal supported version: 200.0.0")

    def configurations_list(self) -> List[GcloudConfiguration]:
        """
        Returns list of discovered gcloud configurations
        """
        out = check_output(["gcloud", "config", "configurations",
                            "list", "--format=json"],
                           timeout=self.timeout)
        parsed = loads(out)
        return [GcloudConfiguration(
            name=conf["name"],
            is_active=conf["is_active"],
            account=conf["properties"]["core"]["account"],
            project=conf["properties"]["core"]["project"],
            properties=conf["properties"],
        ) for conf in parsed]

    def activate_configuration(self, name: str) -> str:
        parsed = check_output(["gcloud", "config", "configurations",
                               "activate", name, "--format=json"],
                              timeout=self.timeout)
        return loads(parsed)

    def _get_gcloud_version(self) -> VersionTuple:
        out = check_output(["gcloud", "version", "--format=json"],
                           timeout=self.timeout)
        parsed = loads(out)
        return VersionTuple(parsed["Google Cloud SDK"])
