
from datetime import datetime
import PySimpleGUI as sg
import subprocess
import serial.tools.list_ports

all_ports = serial.tools.list_ports.comports()
print(all_ports)


arduino_port = None

for port in all_ports:
    if port.name.find("USB") != -1:
        arduino_port = port
        print(arduino_port.device)
arduino = serial.Serial(port=arduino_port.device, baudrate=9600, timeout=.1)


if __name__ == '__main__':




    vals =["1", "231", "321", "22221", "223231", "2323231", "3232321"]
    box = sg.Listbox(values=vals, enable_events=True, size=(145, 35),
        key="-SCROLL-WINDOW-"
    )



    box.scroll_width =100
    box.scroll_arrow_width=100
    size = (11, 3)
    layout = [[sg.Button("OK", size=size), sg.Button("TOP", size=size), sg.Button("HOLD", size=size), sg.Button("UPDATE", size=size), sg.Button("CLOSE", size=size), sg.Button("STATUS", size=size)], [box]]
    window = sg.Window(title="Obrotnica", layout=layout, margins=(20, 20), no_titlebar=True, location=(0, 0), size=(1024, 600), keep_on_top=True)

    while True:
        event, values = window.read(timeout=1)
        # End program if user closes window or
        # presses the OK button
        data = arduino.readline().strip()
        if data:
            vals.insert(0, "{} {}".format(str(datetime.now()), data))
            vals = vals[:1000]
            index = 0
            if len(window["-SCROLL-WINDOW-"].get_indexes()) and window["-SCROLL-WINDOW-"].get_indexes()[0]:
                index = window["-SCROLL-WINDOW-"].get_indexes()[0] + 1
            window["-SCROLL-WINDOW-"].update(vals, set_to_index=[index], scroll_to_index=index)

        if event == "CLOSE":
            break
        if event == "UPDATE":
            process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
            process2 = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE)
            break
        if event == "TOP":
            window["-SCROLL-WINDOW-"].update(vals, set_to_index=[0], scroll_to_index=0)
        if event == "HOLD":
            if (len(window["-SCROLL-WINDOW-"].get_indexes()) and window["-SCROLL-WINDOW-"].get_indexes()[0] == 0)\
                    or len(window["-SCROLL-WINDOW-"].get_indexes()) == 0:
                window["-SCROLL-WINDOW-"].update(vals, set_to_index=[1], scroll_to_index=1)


        if event == sg.WIN_CLOSED:
            break



