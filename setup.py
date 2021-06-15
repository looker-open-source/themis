from loguru import logger
import looker_sdk
from looker_sdk import error
from looker_sdk.rtl import api_settings, auth_session, requests_transport, serialize
from looker_sdk.sdk.api40 import methods, models


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
    logger.error('Issues generating SDK configuration.')

  return methods.Looker40SDK(
    auth_session.AuthSession(settings, transport, serialize.deserialize40, "4.0"),
    serialize.deserialize40,
    serialize.serialize,
    transport,
    "4.0"
  )
