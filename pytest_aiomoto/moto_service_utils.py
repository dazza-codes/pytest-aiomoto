import os

import moto.backends
import moto.server

_PYCHARM_HOSTED = os.environ.get("PYCHARM_HOSTED") == "1"
CONNECT_TIMEOUT = 90 if _PYCHARM_HOSTED else 10


def moto_service_reset(service_name: str):
    """
    Reset a moto service backend, for all regions.
    Each service can have multiple regional backends.
    """
    service_backends = moto.backends.get_backend(service_name)
    for region_name, backend in service_backends.items():
        backend.reset()


def moto_service_app(service_name: str):
    app = moto.server.DomainDispatcherApplication(
        moto.server.create_backend_app, service=service_name
    )
    app.debug = True
    return app
