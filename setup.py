import looker_sdk
from looker_sdk import error
from looker_sdk.rtl import api_settings, auth_session, requests_transport, serialize
from looker_sdk.sdk.api40 import methods, models


def configure_sdk(config_file):
    settings = api_settings.ApiSettings(config_file, "Looker")
    user_agent_tag = f"Themis v1.0"
    settings.headers = {
        "Content-Type": "application/json",
        "User-Agent": user_agent_tag,
    }
    settings.timeout = 480
    transport = requests_transport.RequestsTransport.configure(settings)

    return methods.Looker40SDK(
            auth_session.AuthSession(settings, transport, serialize.deserialize40, "4.0"),
            serialize.deserialize40,
            serialize.serialize,
            transport,
            "4.0"
        )
