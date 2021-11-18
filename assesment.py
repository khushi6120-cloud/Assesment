import os
import time
import shutil
from os import listdir
from os.path import join, isfile

import mysql.connector

pre_path = 'processing'
tlee_path = 'queue'
ckm_path = 'processed'
pmc = mysql.connector.connect(
    host="localhost",
    user="khushi",
    password="yyyy",
    database="anm"
)
drawer = pmc.cursor()
for i in range(1, 31):
    f = str(i)
    filename = f + ".txt"
    with open(os.path.join(pre_path, filename), 'w') as fp:
        pass

    sql = "INSERT INTO Sayrun (Fname, Status) VALUES (%s, %s)"
    val = (filename, "0")
    drawer.execute(sql, val)
    pmc.commit()
    time.sleep(1)

    if i % 5 == 0 and not(any(isfile(join(tlee_path, i)))):
        all_files = os.listdir(pre_path)
        for file in all_files:
            shutil.move(pre_path + '/' + file, tlee_path + '/' + file)

        all_files1 = os.listdir(tlee_path)
        for file in all_files1:
            sql1 = "UPDATE Sayrun SET Status = %s Where Fname =%s"
            val1 = ("1",file)
            drawer.execute(sql1, val1)
            pmc.commit()

    if any(isfile(join(tlee_path, i)) for i in listdir(tlee_path)):  # checking if any file exists in queue folder.
        file_to_move = os.listdir(tlee_path)[0]  # transferring the very first file to processed folder.
        shutil.move(tlee_path + '/' + file_to_move, ckm_path + '/' + file_to_move)

