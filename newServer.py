from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify
import mysql.connector as mariadb

app = Flask(__name__)
api = Api(app)

class ScanInfo:
    timestamps_scan = []
    filenames_scan = []
    scan_id = []
    host_id = []

    names_host = []
    macID_host = []
    ip_host = []
    manufacturer_host = []

    portNames = []
    portState = []
    portService = []

    def AllScanInfo():
        allScanInfo = []
        allScanInfo.append(timestamps_scan, filenames_scan)
        return allScanInfo

    def AllHostInfo():
        allHostInfo = []
        allHostInfo.append(names_host, macID_host, ip_host, manufacturer_host)
        return allHostInfo

    def AllPortInfo():
        allPortInfo = []
        allPortInfo.append(portNames, portState, portService)
        return allPortInfo

class Scans(Resource):
    def get(self):
        scaninfo = ScanInfo()
        mariadb_connection = mariadb.connect(user='root', password='gargar', database='nmapscans')
        cursor = mariadb_connection.cursor()

        #GetScans
        cursor.execute("select * from nmap_scan")

        for id, timestamp, filename in cursor:
            scaninfo.scan_id.append(id)
            scaninfo.timestamps_scan.append(timestamp)
            scaninfo.filenames_scan.append(filename)

        #GetHosts
        cursor.execute("select * from nmap_host where scan_id = " + str(scaninfo.scan_id[0]))

        for id, name, macid, ip, manufacturer, scan_id in cursor:
            scaninfo.host_id.append(id)
            scaninfo.names_host.append(name)
            scaninfo.macID_host.append(macid)
            scaninfo.ip_host.append(ip)
            scaninfo.manufacturer_host.append(manufacturer)

        #GetPorts
        cursor.execute("select * from nmap_port where host_id = " + str(scaninfo.host_id[1]))

        for id, port, state, service, host_id in cursor:
            scaninfo.portNames.append(port)
            scaninfo.portState.append(state)
            scaninfo.portService.append(service)


        return jsonify(scaninfo.AllScanInfo)


api.add_resource(Scans, '/nmapscan') # Route_1


if __name__ == '__main__':
     app.run(port=5002)
