from flask import Flask
from Api.Train import train
from Api.Railway import railway
from Api.Emergency import emergency
from Simulator import Simulator

app = Flask(__name__)

app.register_blueprint(train, url_prefix='/train')
app.register_blueprint(railway, url_prefix='/railway')
app.register_blueprint(emergency, url_prefix='/emergency')

if __name__ == '__main__':
    simulator = Simulator()
    simulator.start_thread()
    app.run(debug=True)