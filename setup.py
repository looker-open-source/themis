from loguru import logger
from looker_sdk.rtl import api_settings
from looker_sdk.rtl import auth_session
from looker_sdk.rtl import requests_transport
from looker_sdk.rtl import serialize
from looker_sdk.sdk.api40 import methods


def configure_sdk():

  try:
    settings = api_settings.ApiSettings()
    user_agent_tag = f"Themis v1.0"
    settings.headers = {
      "Content-Type": "application/json",
      "User-Agent": user_agent_tag,
    }
    settings.timeout = 480
    transport = requests_transport.RequestsTransport.configure(settings)
  except Exception as e:
    logger.error('Issues generating SDK configuration: {}'.format(e))

  return methods.Looker40SDK(
    auth_session.AuthSession(settings, transport, serialize.deserialize40, "4.0"),
    serialize.deserialize40,
    serialize.serialize,
    transport,
    "4.0"
  )
