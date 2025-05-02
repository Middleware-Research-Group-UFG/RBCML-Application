from app import create_app, socketio


app = create_app()

socketio.run(app, host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
