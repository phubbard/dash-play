#!/usr/bin/env python
# paul hubbard
# 9/26/15
# Pythonic wrappers for the itunes API and my local configuration

import logging
from datetime import datetime
from ConfigParser import SafeConfigParser

from flask import Flask, make_response, request

import requests

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

app = Flask(__name__)

config = SafeConfigParser()
config.read('config.ini')

# Where the iTunes API is running
ITUNES = config.get('itunes', 'api_url')

# Button MAC addresses
buttons = {config.get('buttons', 'glad'): 'glad',
           config.get('buttons', 'bounty') : 'bounty',
           config.get('buttons', 'ziploc') : 'ziploc',
           config.get('buttons', 'tide'): 'tide',
           config.get('buttons', 'iot'): 'iot'}

# AirPort speaker names
KITCHEN = 'Kitchen'
KIDROOM = 'Upstairs kid room'
LIVINGROOM = 'Living room'
GARAGE = 'Garage'


def is_playing():
    """
    Is iTunes playing anything?
    """
    rv = requests.get(ITUNES + '/now_playing')
    jdata = rv.json()
    if jdata['player_state'] == 'playing':
        return True

    return False


def stop():
    log.info('Stopping playback')
    requests.put(ITUNES + '/stop')


def find_speaker_id(speaker_name):
    rv = requests.get(ITUNES + '/airplay_devices')
    jlist = rv.json()['airplay_devices']
    for device in jlist:
        if device['name'] == speaker_name:
            return device['id']

    log.error('Unable to find speaker ' + speaker_name)


def single_speaker_on(speaker_name): 
    rv = requests.get(ITUNES + '/airplay_devices')
    jlist = rv.json()['airplay_devices']

    # Make sure device is on before turn others off, otherwise itunes enables the computer speaker
    for device in jlist:
        if device['name'] == speaker_name:
            speaker_control(device['id'], turn_on=True)

    # Turn off everything else
    for device in jlist:
        if device['name'] != speaker_name:
            speaker_control(device['id'], turn_on=False)

    log.debug('Done with single-speaker to ' + speaker_name)


def speaker_control(speaker_id, turn_on=True):
    if turn_on:
        cmd_str = '/on'
    else:
        cmd_str = '/off'
    rv = requests.put(ITUNES + '/airplay_devices/' + speaker_id + cmd_str)


def find_playlist_id(playlist_name):
    rv = requests.get(ITUNES + '/playlists')
    playlists = rv.json()['playlists']
    for list in playlists:
        if list['name'] == playlist_name:
            return list['id']

    log.error('Unable to find playlist named ' + playlist_name)


def start_playlist(playlist_name):
    log.info('Starting playlist ' + playlist_name)
    rv = requests.put(ITUNES + '/playlists/' + find_playlist_id(playlist_name) + '/play')


##########################################################################################
# Top-level button logic    
def glad_button():
    single_speaker_on(KITCHEN)

    d = datetime.now()
    if d.hour < 12: # Switch modes at noon
        log.info('Glad pressed, before noon, starting morning playlist')
        start_playlist('Calm classical')
    elif d.hour < 18:
        log.info('Glad pressed, after noon, starting afternoon news')
        start_playlist('APM')
    else:
        log.info('Glad pressed, later, starting evening playlist')
        start_playlist('Dishes')
    
# The IoT button, calling from Lambda, also can do short/long/double clicks. Cool.
def iot_button(type):

    log.info('iot type ' + type)
    single_speaker_on(KITCHEN)

    if type == 'SINGLE':
        start_playlist('Dishes')
    if type == 'DOUBLE':
        start_playlist('Singalong')
    if type == 'LONG':
        start_playlist('Calm classical')
        
def bounty_button():
    single_speaker_on(KIDROOM)
    d = datetime.now()
    if d.hour < 19:
        start_playlist('Anna dance')
    else:
        start_playlist('Bed')


def tide_button():
    single_speaker_on(GARAGE)
    start_playlist('Basic rock')


def ziploc_button():
    single_speaker_on(KIDROOM)
    d = datetime.now()
    if d.hour < 19:
        start_playlist('Margaret dance')
    else:
        start_playlist('Bed')


def lookup_button(hw_addr):
    if buttons.has_key(hw_addr):
        return buttons[hw_addr]
    return None


############################################################################################
# Web logic - gets called by the root-running daemon, just gets button events
@app.route('/button/<hw_addr>', methods=['PUT'])
def button_event(hw_addr):

    name = lookup_button(hw_addr)
    if not name:
        log.warn('Ignoring unknown address '+ hw_addr)
        return make_response('Ignored')

    type = request.args.get('type') 
    if type == None:
        type = 'none'

    log.info('Got button event for ' + hw_addr + ' -> ' + name)

    if is_playing():
        stop()
        return make_response('Stopping')

    # TODO roll into a dictionary
    if name is 'glad':
        glad_button()
    if name is 'tide':
        tide_button()
    if name is 'bounty':
        bounty_button()
    if name is 'ziploc':
        ziploc_button()
    if name is 'iot':
        iot_button(type)

    return make_response('OK')

###
if __name__ == '__main__':
    app.run(port=4321, host='0.0.0.0', debug=True, threaded=True)

