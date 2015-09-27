#!/usr/bin/env python
# paul hubbard
# 9/26/15
# Pythonic wrappers for the itunes API and my local configuration

import logging
from datetime import datetime

import requests

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

# Where the iTunes API is running
ITUNES = 'http://thor.phfactor.net:8181'

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



def glad_button():
    if is_playing():
        log.info('Stopping playback via Glad')
        stop()
        return

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
    
def bounty_button():
    if is_playing():
        log.info('Stopping playback via Bounty')
        stop()
        return

    single_speaker_on(KIDROOM)
    start_playlist('Bed')
