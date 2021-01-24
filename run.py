import uvicorn

"""Webサーバを立ち上げる際に実行するファイル"""
if __name__ == "__main__":
    # api.run(address="0.0.0.0", port=5500, debug=True)
    # uvicorn.run("run:api", host='0.0.0.0', log_config="logging_config.json", port=5500, debug=True, reload=True)
    uvicorn.run(
        "app.application_responder:api", 
        host='0.0.0.0', 
        port=5500, 
        debug=True, 
        reload=True,
        reload_dirs=['app']
    )
