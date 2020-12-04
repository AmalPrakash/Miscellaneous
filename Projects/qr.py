import os
import time
import cv2
import imutils
from pyzbar import pyzbar
import pickle

###################################
####### Initialise Settings #######
###################################
cap = cv2.VideoCapture(0)
BASE = os.getcwd()
secret_key_metadata = None
wifi_metadata = None
remote_metadata = None

# reading secret file object
try:
    with open(BASE + '/secret_metadata.pkl', 'rb') as f:
        secret_metadata = pickle.load(f)
except IOError as e:
    with open(BASE + '/secret_metadata.pkl', 'wb') as f:
        pickle.dump({'secret_key': 'admin'}, f)

# reading wifi file object
try:
    with open(BASE + '/wifi_metadata.pkl', 'rb') as f:
        wifi_metadata = pickle.load(f)
except IOError as e:
    with open(BASE + '/wifi_metadata.pkl', 'wb') as f:
        pickle.dump({'uuid': 'admin', 'password': 'password'}, f)

# reading remote file object
try:
    with open(BASE + '/remote_metadata.pkl', 'rb') as f:
        remote_metadata = pickle.load(f)
except IOError as e:
    with open(BASE + '/remote_metadata.pkl', 'wb') as f:
        pickle.dump({'host': 'localhost', 'master_slug':'/qrcode'}, f)



initial_time = time.time()
time_limit = initial_time + 5

def detect_qr_code():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 90)
    frame = imutils.resize(frame, width=600)

    
    # finding qrcode
    barcodes = pyzbar.decode(frame)

    output = []

    for barcode in barcodes[0:1]:
        barcodeData = barcode.data.decode("utf-8")
        timestamp = time.ctime(time.time())
        barcodeType = barcode.type
        output = [barcodeData, barcodeType]
       
    return output 


def format_data(data):
    output_dict = {}
    tokens = data.split('\n')
    for pair in tokens:
        key, value = str(pair.split(':')[0]), str(pair.split(':')[1])
        output_dict[key] = value
    return output_dict

def compare_keys(present_key):
    if secret_metadata['secret_key'] == present_key:
        return True
    else:
        return False

def change_secret_key(data):
    if compare_keys(data['present_key']):
        # updating secret key
        with open(BASE + '/secret_metadata.pkl', 'wb') as f:
            pickle.dump({'secret_key': data['secret_key']}, f)
    else:
        return "Unauthorised Access! Fuck yourself :)"

# User must be informed the reset state's period
def reset():
    flag = True
    output = result = None
    print("You can show QR Code in five seconds...")
    while time.time() <= time_limit and flag:
        result = detect_qr_code()
        if result != []:
            flag = False
            print(result[0])
            output = format_data(result[0])
            change_secret_key(output)
    return output


if __name__ == "__main__":
    print(reset())
#reset.txt
#Displaying reset.txt.