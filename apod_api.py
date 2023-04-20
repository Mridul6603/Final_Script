import requests 
import datetime
import sys
from datetime import date
import pprint
import image_lib
'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''


api_get_url = 'https://api.nasa.gov/planetary/apod'
api_key = '0g2uwthxHKQpaXSUUW6eWfAS1vvWDw2oAfoTSAFo'

def main():
    # TODO: Add code to test the functions in this module

    if len(sys.argv) == 2:
        date = sys.argv[1]
    else:
        date = datetime.date.today()
        print (datetime.date.today())

    info = get_apod_info(date)
    get_apod_image_url(info)

def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    apod_info = str(apod_date).strip().lower()


    url = api_get_url + f'?api_key={api_key}&date={apod_date}'
    print (url)
    print ('\n',f'Searching for the apod with the date {apod_info}..', '\n', end='')
    resp_msg = requests.get(url)

    if resp_msg.status_code == requests.codes.ok:
        print('\n',f'APOD date: {apod_info}' , '\n')
        return resp_msg.json()
    else:
        print('\n','Failure, No such data is available', '\n')
        print('\n',f'Error Code : {resp_msg.status_code}, Reason For Error : {resp_msg.reason}', '\n')
    return None

def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info from API

    Returns:
        str: APOD image URL
    """

    url_exp = apod_info_dict["url"]
    
    return url_exp

if __name__ == '__main__':
    main()