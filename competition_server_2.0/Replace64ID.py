import csv
from collections import defaultdict

def Replace_SteamIDs():
    SteamID_To_GameID = {}
    with open('SteamID_GameID.csv', 'r', encoding = 'UTF-8') as SteamID_To_GameID_File:
        Read_ID = csv.reader(SteamID_To_GameID_File)
        for row in Read_ID:
            if len(row) >= 2:
                Game_ID, Steam_ID = row[0], row[1]
                if len(Steam_ID) == 17 and Steam_ID.isdigit():
                    SteamID_To_GameID[Steam_ID] = Game_ID

    with open('Player_Data.csv', 'r', encoding = 'UTF-8') as Input_File, \
         open('Final_Show_Player.csv', 'w', newline = '', encoding = 'UTF-8') as Output_File:
        
        Read_SteamID = csv.reader(Input_File)
        Write_GameID = csv.writer(Output_File)

        Header = next(Read_SteamID)
        if '选手ID' in Header:
            print('原始文件已经存在ID列,将被覆盖')
            Header.remove('选手ID')
        Header.insert(0, '选手ID')
        Write_GameID.writerow(Header)

        for row in Read_SteamID:
            Matched_IDs = ''
            for All_SteamIDs in row:
                if len(All_SteamIDs) == 17 and All_SteamIDs.isdigit() and All_SteamIDs in SteamID_To_GameID:
                    Matched_IDs = SteamID_To_GameID[All_SteamIDs]
                    break
            row.insert(0, Matched_IDs)
            Write_GameID.writerow(row)