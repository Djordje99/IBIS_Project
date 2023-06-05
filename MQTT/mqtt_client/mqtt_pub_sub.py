from time import sleep
from paho.mqtt import client as mqtt_client
import requests
import mqtt_client.mqtt_config as config
import mqtt_client.states as states

endpoint = 'http://localhost:5000'
pull_url = endpoint + '/pull'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(config.client_id)
    client.on_connect = on_connect
    client.connect(config.broker, config.port)
    return client


def _publish(client, topic, message):
    status_message = client.publish(topic, message)
    if status_message == 0:
        print(f"Failed to send message to topic {topic}")
    else:
        print(f"Successfully sent message {message}")


def create_connection():
    client = connect_mqtt()
    client.loop_start()
    return client


def _subscribe(client, topic):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def get_message(topic):
    client = connect_mqtt()
    _subscribe(client, topic)
    client.loop_forever()


def pull_data(client):

    while True:
        sleep(2)
        response = requests.get(pull_url, '')
        
        #parse response

        if states.train_A['direction'] != response['direction']:
            states.train_A['direction'] = response['direction']

        if states.train_A['position'] != response['position']:
            states.train_A['position'] = response['position']
            if states.train_A['direction'] == 'A':
                _publish(client, config.topics['train_aa'], states.train_A['position'])
            else:
                _publish(client, config.topics['train_ab'], states.train_A['position'])
        
        if states.train_A['speed'] != response['speed']:
            states.train_A['speed'] = response['speed']
            _publish(client, config.topics['speed_a'], states.train_A['speed'])

        if states.train_A['doors'] != response['doors']:
            states.train_A['doors'] = response['doors']
            _publish(client, config.topics['doors_a'], states.train_A['doors'])

        if states.train_A['passing_ab'] != response['passing_ab']:
            states.train_A['passing_ab'] = response['passing_ab']
            _publish(client, config.topics['passing_ab'], states.train_A['passing_ab'])

        if states.train_A['passing_ac'] != response['passing_ac']:
            states.train_A['passing_ac'] = response['passing_ac']
            _publish(client, config.topics['passing_ac'], states.train_A['passing_ac'])