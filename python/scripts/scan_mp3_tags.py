from os.path import join, isdir
from os import listdir
from mutagen.easyid3 import EasyID3

log_file = "error.log"

def check_tag(f_name):
    """ Test f_name to seee if it has a valid mp3 tag. """    
    try:
        mp3info = EasyID3(f_name)
        mp3info.items()
        print("validated " + f_name)
    except Exception as e:
        print("Error processing: " + f_name)
        with open(log_file, "a") as f:
            f.write(f_name + '\r\n')

def scan_folder(source):
    """
    Synchronizes the contents of the sources and destination folder.
    """
    # Note: We use listdir i.s.o. walk to we need tighter control over
    # iteration to maintain the mapping the the destination
    files = listdir(source)
    for item in files:
        f_source = join(source, item)
        if isdir(f_source):
            scan_folder(f_source)
        elif f_source.lower().find(".mp3") > -1:
            check_tag(f_source)
            
            
if __name__ == "__main__":
    # Initialize
    scan_folder('/home/fruitbat/Music/')