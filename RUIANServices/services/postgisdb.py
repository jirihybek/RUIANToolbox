__author__ = 'Augustyn'

import psycopg2
from RUIANConnection import *

DATABASE_HOST = "192.168.1.93"
PORT = "5432"
DATABSE_NAME = "adresni_misto"
USER_NAME = "postgres"
PASSWORD = "postgres"

ITEM_TO_DBFIELDS = {
    "id": "gid",
    "street": "nazev_ulice",
    "houseNumber": "cislo_domovni",
    "recordNumber": "nazev_momc",
    "orientationNumber": "cisloOrientacni",
    "zipCode": "psc",
    "locality": "nazev_obce",
    "localityPart": "nazev_casti_obce",
    "districtNumber": "nazev_mop",
    "JTSKX": "latitude",
    "JTSKY": "longitude"
}

def noneToString(item):
    if item is None:
        return ""
    else:
        return item

def _findAddress(ID):
    con = psycopg2.connect(host=DATABASE_HOST, database=DATABSE_NAME, port= PORT, user=USER_NAME, password=PASSWORD)
    cur = con.cursor()
    cur.execute("SELECT nazev_ulice, cislo_domovni, nazev_momc, cislo_orientacni, psc, nazev_obce, nazev_casti_obce, nazev_mop FROM test WHERE gid = "+ str(ID))
    row = cur.fetchone()
    if row:
        return Address(noneToString(row[0]),noneToString(row[1]),noneToString(row[2]),noneToString(row[3]),noneToString(row[4]),noneToString(row[5]),noneToString(row[6]),noneToString(row[7]))
        #(street, houseNumber, recordNumber, orientationNumber, zipCode, locality, localityPart, districtNumber)
    else:
        return None

def _getNearbyLocalities(x,y,distance):
    con = psycopg2.connect(host=DATABASE_HOST, database=DATABSE_NAME, port= PORT, user=USER_NAME, password=PASSWORD)
    cur = con.cursor()
    query = "SELECT nazev_ulice, cislo_domovni, nazev_momc, cislo_orientacni, psc, nazev_obce, nazev_casti_obce, nazev_mop FROM test WHERE ST_DWithin(the_geom,ST_GeomFromText('POINT(%s %s)',5514),%s);" % (str(y), str(x), str(distance),)
    cur.execute(query)
    rows = cur.fetchall()
    addresses = []
    for row in rows:
        adr = Address((noneToString(row[0]).decode("utf-8")),(noneToString(row[1]).decode("utf-8")),(noneToString(row[2]).decode("utf-8")),(noneToString(row[3]).decode("utf-8")),(noneToString(row[4]).decode("utf-8")),(noneToString(row[5]).decode("utf-8")),(noneToString(row[6]).decode("utf-8")),(noneToString(row[7]).decode("utf-8")))
        addresses.append(adr)
    return addresses

def _validateAddress(dictionary):
    first = True
    con = psycopg2.connect(host=DATABASE_HOST, database=DATABSE_NAME, port= PORT, user=USER_NAME, password=PASSWORD)
    cur = con.cursor()

    query = "SELECT * FROM test WHERE "

    for key in dictionary:
        if dictionary[key] != "":
            if first:
                query += ITEM_TO_DBFIELDS[key] + " = '" + dictionary[key] + "'"
                first = False
            else:
                query += " AND " + ITEM_TO_DBFIELDS[key] + " = '" + dictionary[key] + "'"

    cur.execute(query)
    row = cur.fetchone()
    if row:
        return True
    else:
        return False

def _findCoordinates(ID):
    con = psycopg2.connect(host=DATABASE_HOST, database=DATABSE_NAME, port= PORT, user=USER_NAME, password=PASSWORD)
    cur = con.cursor()
    cur.execute("SELECT latitude, longitude FROM test WHERE gid = "+ str(ID))
    row = cur.fetchone()
    if row:
        c = Coordinates(str(row[0]), str(row[1]))
        return [c]
    else:
        return []

def _findCoordinatesByAddress(dictionary):
    first = True
    con = psycopg2.connect(host=DATABASE_HOST, database=DATABSE_NAME, port= PORT, user=USER_NAME, password=PASSWORD)
    cur = con.cursor()

    query = "SELECT latitude, longitude FROM test WHERE "

    for key in dictionary:
        if dictionary[key] != "":
            if first:
                query += ITEM_TO_DBFIELDS[key] + " = '" + dictionary[key] + "'"
                first = False
            else:
                query += " AND " + ITEM_TO_DBFIELDS[key] + " = '" + dictionary[key] + "'"

    cur.execute(query)
    rows = cur.fetchall()
    coordinates = []

    for row in rows:
        coordinates.append(Coordinates(str(row[0]),str(row[1])))
    return coordinates