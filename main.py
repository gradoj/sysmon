import back, click
from flask import Flask, render_template, jsonify, request
import logging
from python_on_whales import DockerClient

logging.basicConfig(level=logging.DEBUG)

main = Flask(__name__)

@main.route("/disco",methods=["POST","GET"]) 
def disco(): 
    logging.info('Disco mode called')
    if request.method == "POST": 
        packet_num = request.form.get("packet_num")
        packet_delay = request.form.get("packet_delay")
        print('packet_num', packet_num)
        print('packet_delay', packet_delay)
    
        # kick off disco mode. want to pass in packet_num and delay
        docker = DockerClient(compose_files=["../discoclient/docker-compose.yml"])
        try:
            docker.compose.up(detach=True)
        except:
            docker.compose.build()
            docker.compose.up(detach=True)
    return 'DiscoStarted'#render_template('home.html') 


@main.route("/termproc/<prociden>/", methods=["GET"])
def termproc(prociden):
    back.TerminateSingleProcess(prociden)
    return "Terminated"


@main.route("/killproc/<prociden>/", methods=["GET"])
def killproc(prociden):
    back.KillSingleProcess(prociden)
    return "Killed"


@main.route("/sspdproc/<prociden>/", methods=["GET"])
def sspdroc(prociden):
    back.SuspendSingleProcess(prociden)
    return "Suspended"


@main.route("/resmproc/<prociden>/", methods=["GET"])
def resmproc(prociden):
    back.ResumeSingleProcess(prociden)
    return "Resumed"

@main.route("/fetcinfo/", methods=["GET"])
def fetcinfo():
    virtdata = back.GetVirtualMemoryData()
    swapinfo = back.GetSwapMemoryInfo()
    cputimes = back.GetCPUStateTimes()
    cpuprcnt = back.GetCPUUsagePercent()
    cpustats = back.GetCPUStatistics()
    cpuclock = back.GetCPUClockSpeed()
    diousage = back.GetDiskIOUsage()
    netusage = back.GetNetworkIOUsage()
    procinfo = back.GetProcessInfo()
    senstemp = back.GetSensorsTemperature()
    fanspeed = back.GetSensorsFanSpeed()
    battstat = back.GetSensorsBatteryStatus()
    minernam = 'little-blue-donkey'
    blockhgt = 42
    retnjson = jsonify(virtdata=virtdata, swapinfo=swapinfo, cputimes=cputimes,
                       cpuprcnt=cpuprcnt, cpustats=cpustats, cpuclock=cpuclock,
                       diousage=diousage, netusage=netusage, procinfo=procinfo,
                       senstemp=senstemp, fanspeed=fanspeed, battstat=battstat,
                       minernam=minernam, blockhgt=blockhgt)
    return retnjson


@main.route("/<thmcolor>/", methods=["GET"])
def custpage(thmcolor="maroon"):
    retndata = back.GetOSUnameData()
    cpuquant = back.GetCPULogicalCount()
    diskpart = back.GetAllDiskPartitions()
    diousage = back.GetDiskIOUsage()
    netusage = back.GetNetworkIOUsage()
    procinfo = back.GetProcessInfo()
    senstemp = back.GetSensorsTemperature()
    fanspeed = back.GetSensorsFanSpeed()
    boottime = back.GetBootTime()
    netaddrs = back.GetNetworkIFAddresses()
    netstats = back.GetNetworkStatistics()
    return render_template("custpage.html", retndata=retndata, cpuquant=cpuquant,
                           diskpart=diskpart, diousage=diousage, netusage=netusage,
                           netaddrs=netaddrs, netstats=netstats, senstemp=senstemp,
                           fanspeed=fanspeed, boottime=boottime, procinfo=procinfo,
                           thmcolor=thmcolor)


@click.command()
@click.option("-p", "--portdata", "portdata", help="Set the port value [0-65536]", default="3001")
@click.option("-6", "--ipprotv6", "netprotc", flag_value="ipprotv6", help="Start the server on an IPv6 address")
@click.option("-4", "--ipprotv4", "netprotc", flag_value="ipprotv4", help="Start the server on an IPv4 address")
@click.version_option(version="0.1.0", prog_name="WebStation SYSMON by t0xic0der")
def mainfunc(portdata, netprotc):
    print(" * Starting WebStation SYSMON by t0xic0der...")
    print(" * Port number : " + str(portdata))
    netpdata = ""
    netprotc = "ipprotv4"
    if netprotc == "ipprotv6":
        print(" * IP version  : 6")
        netpdata = "::"
    elif netprotc == "ipprotv4":
        print(" * IP version  : 4")
        netpdata = "0.0.0.0"
    main.run(port=portdata, host=netpdata)#, debug=True)


if __name__ == "__main__":
    mainfunc()
