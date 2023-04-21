""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py [apod_date]

Parameters:
  apod_date = APOD date (format: YYYY-MM-DD)
"""
from datetime import date
import os
import image_lib
import inspect
import sys
import datetime 
import sqlite3
import hashlib
import apod_api


# Global variables
image_cache_dir = None  # Full path of image cache directory
image_cache_db = None   # Full path of image cache database

def main():
    ## DO NOT CHANGE THIS FUNCTION ##
    # Get the APOD date from the command line
    apod_date = get_apod_date()    

    # Get the path of the directory in which this script resides
    script_dir = get_script_dir()

    # Initialize the image cache
    init_apod_cache(script_dir)

    # Add the APOD for the specified date to the cache
    apod_id = add_apod_to_cache(apod_date)

    # Get the information for the APOD from the DB
    apod_info = get_apod_info(apod_id)

    # Set the APOD as the desktop background image
    if apod_id != 0:
        image_lib.set_desktop_background_image(apod_info['file_path'])

def get_apod_date():
    """Gets the APOD date
     
    The APOD date is taken from the first command line parameter.
    Validates that the command line parameter specifies a valid APOD date.
    Prints an error message and exits script if the date is invalid.
    Uses today's date if no date is provided on the command line.

    Returns:
        date: APOD date
    """
    # TODO: Complete function body
    if len(sys.argv) == 2:
        date = sys.argv[1]
    else:
        date = datetime.date.today()
        print (datetime.date.today())
    apod_date = datetime.date.fromisoformat(str(date))
    return apod_date

def get_script_dir():
    """Determines the path of the directory in which this script resides

    Returns:
        str: Full path of the directory in which this script resides
    """
    ## DO NOT CHANGE THIS FUNCTION ##
    script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
    return os.path.dirname(script_path)

def init_apod_cache(parent_dir):
    """Initializes the image cache by:
    - Determining the paths of the image cache directory and database,
    - Creating the image cache directory if it does not already exist,
    - Creating the image cache database if it does not already exist.
    
    The image cache directory is a subdirectory of the specified parent directory.
    The image cache database is a sqlite database located in the image cache directory.

    Args:
        parent_dir (str): Full path of parent directory    
    """

    global image_cache_dir
    global image_cache_db

    # TODO: Determine the path of the image cache directory
    # TODO: Determine the path of image cache DB

    image_cache_dir = parent_dir + '\images\\'
    image_cache_db = parent_dir + '\\nasa_apod.db'
    print (image_cache_db, image_cache_dir)


    # TODO: Create the image cache directory if it does not already exist
    
    if not os.path.exists(image_cache_dir):
        os.mkdir(image_cache_dir)    
        print("directory created")

    # TODO: Create the DB if it does not already exist
    if not os.path.exists(image_cache_db):
        con = sqlite3.connect(image_cache_db)
        
        cur = con.cursor()

        create_tbl_query = """
        CREATE TABLE IF NOT EXISTS nasa_apod
        (
        ID INTEGER PRIMARY KEY,
        Title TEXT NOT NULL,
        Explanation TEXT NOT NULL,
        Path TEXT NOT NULL,
        SHA_256 TEXT NOT NULL
        );
        """
        cur.execute(create_tbl_query)

        con.commit()
        print("database created")

def add_apod_to_cache(apod_date):
    """Adds the APOD image from a specified date to the image cache.
     
    The APOD information and image file is downloaded from the NASA API.
    If the APOD is not already in the DB, the image file is saved to the 
    image cache and the APOD information is added to the image cache DB.

    Args:
        apod_date (date): Date of the APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if a new APOD is added to the
        cache successfully or if the APOD already exists in the cache. Zero, if unsuccessful.
    """
    print("APOD date:", apod_date.isoformat())
    # TODO: Download the APOD information from the NASA API

    apod_info = apod_api.get_apod_info(apod_date)  
    url = apod_api.get_apod_image_url(apod_info)
    
    # TODO: Download the APOD image

    image = image_lib.download_image(url)
   
    # TODO: Check whether the APOD already exists in the image cache
    # TODO: Save the APOD file to the image cache directory

    if not os.path.exists(image_cache_dir + str(apod_date)):
        save_image = image_lib.save_image_file(image, image_cache_dir + str(apod_date))
        add_tbl_query = """
            INSERT INTO nasa_apod
            (
            Title,
            Explanation,
            Path,
            SHA_256 
            )
            VALUES (?, ?, ?, ?);
            """
        con = sqlite3.connect(image_cache_db)

        cur = con.cursor()
        
        with open(image_cache_dir + str(apod_date),"rb") as f:
            bytes = f.read() # read entire file as bytes
        image_sha256 = hashlib.sha256(bytes).hexdigest()
        print(image_sha256)

        cur.execute(add_tbl_query, [apod_info["title"], apod_info["explanation"], image_cache_dir + str(apod_date), image_sha256 ])
        
        con.commit()

        return get_apod_id_from_db(image_sha256)

    # TODO: Add the APOD information to the DB

    return 0
# do this first
def add_apod_to_db(title, explanation, file_path, sha256):
    """Adds specified APOD information to the image cache DB.
     
    Args:
        title (str): Title of the APOD image
        explanation (str): Explanation of the APOD image
        file_path (str): Full path of the APOD image file
        sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: The ID of the newly inserted APOD record, if successful.  Zero, if unsuccessful       
    """
    # TODO: Complete function body
    return 0
# do this first

def get_apod_id_from_db(image_sha256):
    """Gets the record ID of the APOD in the cache having a specified SHA-256 hash value
    
    This function can be used to determine whether a specific image exists in the cache.

    Args:
        image_sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if it exists. Zero, if it does not.
    """
    db = f"SELECT ID from nasa_apod WHERE SHA_256='{image_sha256}';"

    con = sqlite3.connect(image_cache_db)
        
    cur = con.cursor()
    
    cur.execute(db)

    save = cur.fetchone()[0]
    
    # TODO: Complete function body
    return cur.fetchone()[0]

# do this first

def determine_apod_file_path(image_title, image_url):
    """Determines the path at which a newly downloaded APOD image must be 
    saved in the image cache. 
    
    The image file name is constructed as follows:
    - The file extension is taken from the image URL
    - The file name is taken from the image title, where:
        - Leading and trailing spaces are removed
        - Inner spaces are replaced with underscores
        - Characters other than letters, numbers, and underscores are removed

    For example, suppose:
    - The image cache directory path is 'C:\\temp\\APOD'
    - The image URL is 'https://apod.nasa.gov/apod/image/2205/NGC3521LRGBHaAPOD-20.jpg'
    - The image title is ' NGC #3521: Galaxy in a Bubble '

    The image path will be 'C:\\temp\\APOD\\NGC_3521_Galaxy_in_a_Bubble.jpg'

    Args:
        image_title (str): APOD title
        image_url (str): APOD image URL
    
    Returns:
        str: Full path at which the APOD image file must be saved in the image cache directory
    """
    # TODO: Complete function body
    return
# do this first

def get_apod_info(image_id):
    """Gets the title, explanation, and full path of the APOD having a specified
    ID from the DB.

    Args:
        image_id (int): ID of APOD in the DB

    Returns:
        dict: Dictionary of APOD information
    """
    # TODO: Query DB for image info
    # TODO: Put information into a dictionary
    apod_info = {
        #'title': , 
        #'explanation': ,
        'file_path': 'TBD',
    }
    return apod_info

def get_all_apod_titles():
    """Gets a list of the titles of all APODs in the image cache

    Returns:
        list: Titles of all images in the cache
    """
    # TODO: Complete function body
    # NOTE: This function is only needed to support the APOD viewer GUI
    return

if __name__ == '__main__':
    main()