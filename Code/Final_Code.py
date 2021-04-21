import os,time,datetime,_thread
import pandas as pd
import SensorData.csv_data
import ServerActivity.post_data, ServerActivity.get_response


def csv_write(data_dict):
    """
    Write data in csv file in Log folder out of Code folder
    """
    df = pd.DataFrame(data_dict)
    try:
        fileptr = open("../Log/sensor_data.csv","r+")
        if not fileptr:  
            df.to_csv('../Log/sensor_data.csv',mode='a', index=False, na_rep='Unknown')
        else:
            df.to_csv('../Log/sensor_data.csv',mode='a', header=False,index=False, na_rep='Unknown')
    except FileNotFoundError:
        df.to_csv('../Log/sensor_data.csv',mode='a', index=False, na_rep='Unknown')

def get_status():
    """
    This will check backup_file data is null or not. In case of not null data, read
    all data from text file and try to send to server using "POST" method. If server
    response is ok then clear all old data from backup_file.
    """
    backup_data = ""
    
    try:
        # Try to open backup text file and read data
        backup_file = open("../Log/backup_data.txt","r+")
    except Exception:
        # create backup text file and write null string
        backup_file = open("../Log/backup_data.txt","w+")
        backup_file.write("")
        backup_file.close()

    # Open backup text file and read data
    backup_file = open("../Log/backup_data.txt","r+")
    if backup_file:
        backup_data = backup_file.read()
    backup_file.close()

    # Check data is null or not
    if backup_data == "":
        print("\nNo data in backup_file...")
    if str(backup_data) != "":
        # Post data to HTTP server url
        post_resp = ""
        post_resp = ServerActivity.post_data.post_value(backup_data)
        # Check upload response
        if str(post_resp) == "unavailable":
            print("\nERROR: Server is not running...")
        elif post_resp.status_code != 200:
            print("\nWARNING: Server is not responding...")
        else:
            # reset backup_file data
            backup_file = open("../Log/backup_data.txt","w+")
            if backup_file:
                backup_file.write("")
            backup_file.close()
            print("\nSUCCESS: Posted Backup data to server...")
    else:
        pass
    
    return

def post_sensor_data():
    """
    This will first collect data from sensor. Then write new data to csv file. Next try
    to send data to server. If fails to upload data then write data in backup_file in 
    append mode. 
    """
    # Get sensor data and save to csv file
    data = SensorData.csv_data.run_sensor()
    # Write data to csv file
    csv_write(data)
    # Get status of post response to HTTP server url
    post_resp = ""
    post_resp = ServerActivity.post_data.post_value(data)
    if str(post_resp) == "unavailable":
        # write data to text file
        backup_file = open("../Log/backup_data.txt","a+")
        if backup_file:
            backup_file.write(str(data['Value'])+"\n")
        backup_file.close()
        print("\nERROR: Server is not running...")
    elif post_resp.status_code != 200:
        # write data to text file
        backup_file = open("../Log/backup_data.txt","a+")
        if backup_file:
            backup_file.write(str(data['Value'])+"\n")
        backup_file.close()
        print("\nWARNING: Server is not responding...")
    else:
        print("\nSUCCESS: Posted data to server...")
    
    return

# Define a function for the thread
def print_time( threadName, delay):
    """
    Create a function to call another function as parameter within a time interval.
    """
    while 1:
        time.sleep(delay)
        threadName()
        print ("%s" % (time.ctime(time.time()) ))

def run_main():
    """
    Create thread of two program. get_status function will be called in 5 seconds
    interval and post_sensor_data in 60 seconds interval.
    """
    # Create two threads as follows
    try:
        _thread.start_new_thread(print_time,(get_status, 5,))
        _thread.start_new_thread(print_time,(post_sensor_data, 60,))
    except:
        print ("Error: unable to start thread")

    while 1:
        pass


if __name__ == "__main__":
    run_main()