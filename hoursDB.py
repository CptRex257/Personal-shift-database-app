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

def manageShift(month, day, **kwargs):
    columns = {
        "shiftStart": "SHIFT_START",
        "shiftEnd": "SHIFT_END",
        "shiftLength": "LENGTH",
        "snackBreak": "BREAK"
    }
    print(kwargs)
    for i in kwargs:
        if kwargs[i] != None:
            conn.execute(f'''
            UPDATE {month}
            SET {columns[i]} = "{kwargs[i]}"
            WHERE ID = {day}
            ''')
            conn.commit()

    if "shiftStart" in kwargs and kwargs["shiftStart"] != None:
        startTime = kwargs["shiftStart"].split(":")
    else:
        startTime = conn.execute(f'''
        SELECT SHIFT_START FROM {month}
        WHERE ID = {day}
        ''')
        for i in startTime:
            startTime = i[0].split(":")
    
    if "shiftEnd" in kwargs and kwargs["shiftEnd"] != None:
        endTime = kwargs["shiftEnd"].split(":")
    else:
        endTime = conn.execute(f'''
        SELECT SHIFT_END FROM {month}
        WHERE ID = {day}
        ''')
        for i in endTime:
            endTime = i[0].split(":")
    
    if "shiftLength" in kwargs and kwargs["shiftLength"] != None:
        shiftLength = kwargs["shiftLength"]
    else:
        shiftLength = (int(endTime[0])+(int(endTime[1])/60))-(int(startTime[0])+(int(startTime[1])/60))

    if "snackBreak" in kwargs and kwargs["snackBreak"] != None:
        snackBreak = kwargs["snackBreak"]
        if snackBreak == 1:
            shiftLengthBR = shiftLength - 0.5
        else:
            shiftLengthBR = shiftLength
    else:
        if shiftLength > 4:
            shiftLengthBR = shiftLength - 0.5
            snackBreak = 1
        else:
            shiftLengthBR = shiftLength
            snackBreak = 0

        
    conn.execute(f'''
    UPDATE {month}
    SET BREAK = {snackBreak}, LENGTH = {shiftLength}, WORKED_HOURS = {shiftLengthBR}
    WHERE ID = {day}
    ''')
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
#manageShift("Leden", 4, shiftStart="12:00", shiftEnd="20:00")
#manageShift("Leden", 4, shiftLength=8)
#manageShift("Leden", 4, shiftStart="10:00")
#deleteShift("Leden", 5)
#deleteShift("Leden")
#print(returnMonth(("Leden"))
#print(returnDay("Leden", 5))

if __name__ == "__main__":
    while 1:
        option = input('''Choose your action:

Manage shift - MS *parameters -> month, day, **kwargs - shiftStart=, shiftEnd=, shiftLength=, snackBreak=*; changes values of specified shift to values in parameters
Delete shift - DS *parameters -> month, day=None*; deletes specified shift
Return month - RM *parameters -> month* returns all shifts in specified month
Return day   - RD *parameters -> month, day*; returns specified days' shift

Exit         - EXIT; exits the program 

Your action: ''')
        if "MS" in option.upper():
            text = option.split(" ")
            text = text[1].split(",")
            month = text [0]
            day = text[1]
            text.pop(0)
            text.pop(0)
            Start = None
            End = None
            Length = None
            Break = None
            for i in text:
                i = i.split("=")
                if i[0].upper() == "SHIFTSTART":
                    Start = i[1]
                elif i[0].upper() == "SHIFTEND":
                    End = i[1]
                elif i[0].upper() == "SHIFTLENGTH":
                    Length = i[1]
                elif i[0].upper() == "SNACKBREAK":
                    Break = i[1]

            manageShift(month, day, shiftStart=Start, shiftEnd=End, shiftLength=Length, snackBreak=Break)
        elif "DS" in option.upper():
            text = option.split(" ")
            text = text[1].split(",")
            if len(text) == 1:
                deleteShift(text[0])
                print(f"Shifts in month {text[0]} have been successfully deleted.")
            elif len(text) == 2:
                deleteShift(text[0], text[1])
                print(f"Shift {text[1]}. {text[0]} has been successfully deleted.")
            else:
                print(f"Zadané parametry - {text} jsou nesprávné")
        elif "RM" in option.upper():
            text = option.split(" ")
            text = text[1]
            print(returnMonth(text))
        elif "RD" in option.upper():
            text = option.split(" ")
            text = text[1].split(",")
            print(returnDay(text[0], text[1]))
        elif "EXIT" in option.upper():
            break

