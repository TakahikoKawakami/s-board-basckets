import uvicorn

from app.config import AppConfig
from app.application_responder import api

"""Webサーバを立ち上げる際に実行するファイル"""
if __name__ == "__main__":
    if AppConfig.ENV_DIVISION == AppConfig.ENV_DIVISION_PRODUCTION:
        api.run(port=1000, debug=False)
    elif AppConfig.ENV_DIVISION == AppConfig.ENV_DIVISION_STAGING:
        api.run(port=6500, debug=True)
    elif AppConfig.ENV_DIVISION == 'HEROKU':
        api.run()
    else:
        # uvicorn.run("run:api", host='0.0.0.0', log_config="logging_config.json", port=5500, debug=True, reload=True)
        uvicorn.run(
            "app.application_responder:api",
            host='0.0.0.0',
            port=5500,
            debug=True,
            reload=True,
            reload_dirs=['app']
        )
