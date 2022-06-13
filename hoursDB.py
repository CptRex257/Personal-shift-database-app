#!/usr/bin/python3
import sqlite3

global conn
conn = sqlite3.connect("shifts2022.db")

months = [["Leden", 31], ["Únor", 28], ["Březen", 31], ["Duben", 30],
["Květen", 31], ["Červen", 30], ["Červenec", 31], ["Srpen", 31],
["Září", 30], ["Říjen", 31], ["Listopad", 30], ["Prosinec", 31]]

def createTables(months):
    for i in months:
        conn.execute(f'''
        CREATE TABLE IF NOT EXISTS {i[0]}
        (ID             INTEGER PRIMARY KEY AUTOINCREMENT,
        SHIFT_START     VARCHAR(32),
        SHIFT_END       VARCHAR(32),
        LENGTH          REAL,
        BREAK           INTEGER,
        WORKED_HOURS    REAL
        );'''
        )

    conn.commit()

def initiateTables(months):
    approval = input("Pokud chcete přidat do všech tabulek nové řádky, napište: 'Yes, do as I say!', jinak napšte libovolný znak: ")
    if approval == "Yes, do as I say!":
        for i in months:
            for j in range(1, i[1]+1):
                conn.execute(f'''
                INSERT INTO {i[0]}
                (LENGTH)
                VALUES(0)
                '''
                )
            conn.commit()
    else:
        print("Rozumím, nové řádky nebudou přidány")

def manageShift(month, day, shiftLength=None, shiftStart=None, shiftEnd=None, snackBreak=None):
    if shiftStart == None and shiftEnd == None:
        if snackBreak == None:
            if shiftLength > 4:
                snackBreak = 1
            else:
                snackBreak = 0
        
        if snackBreak == 1:
            shiftLengthBR = shiftLength - 0.5
        else:
            shiftLengthBR = shiftLength
        
        conn.execute(f'''
        UPDATE {month}
        SET LENGTH = {shiftLength}, BREAK = {snackBreak}, WORKED_HOURS = {(shiftLengthBR)}
        WHERE ID = {day}
        '''
        )
        conn.commit()
    
    else:
        startTime = shiftStart.split(":")
        endTime = shiftEnd.split(":")
        shiftLength = (int(endTime[0])+(int(endTime[1])/60))-(int(startTime[0])+(int(startTime[1])/60))
        if snackBreak == None:
            if shiftLength > 4:
                snackBreak = 1
            else:
                snackBreak = 0
    
        if snackBreak == 1:
            shiftLengthBR = shiftLength - 0.5
        else:
            shiftLengthBR = shiftLength
    
        conn.execute(f'''
        UPDATE {month}
        SET SHIFT_START = "{shiftStart}", SHIFT_END = "{shiftEnd}", LENGTH = {shiftLength}, BREAK = {snackBreak}, WORKED_HOURS = {(shiftLengthBR)}
        WHERE ID = {day}
        '''
        )
        conn.commit()


def deleteShift(month, day=None):
    if day == None:
        conn.execute(f'''
        UPDATE {month}
        SET SHIFT_START = NULL, SHIFT_END = NULL, LENGTH = 0, BREAK = NULL, WORKED_HOURS = NULL
        '''
        )
        conn.commit()
    else:
        conn.execute(f'''
        UPDATE {month}
        SET SHIFT_START = NULL, SHIFT_END = NULL, LENGTH = 0, BREAK = NULL, WORKED_HOURS = NULL
        WHERE ID = {day}
        '''
        )
        conn.commit()


def getShifts(shifts):
    for i in shifts:
        manageShift(i[0], i[1])


def returnMonth(month):
    monthTable = conn.execute(f'''
    SELECT * FROM {month}
    '''
    )

    monthList = []
    for line in monthTable:
        monthList.append(line)
    
    return monthList

def returnDay(month, day):
    dayTable = conn.execute(f'''
    SELECT * FROM {month}
    WHERE ID = {day}
    '''
    )

    for line in dayTable:
        return line




#createTables(months)
#initiateTables(months)
#manageShift("Leden", 2, shiftStart="12:00", shiftEnd="20:00")
#deleteShift("Leden", 5)
#deleteShift("Leden")
#print(returnMonth(("Leden"))
#print(returnDay("Leden", 5))

if __name__ == "__main__":
    while 1:
        option = input('''Choose your action:

help - help *command name*; info for chosen command will be shown
MS - MS *parameters*; change speficied shifts' data with specified parameters
DS - DS *parameters*; delete specified shift
RM - RM *parameters*; will return all shifts in specified month
RD - RD *parameters*; will return specified days' shift

Your action: ''')