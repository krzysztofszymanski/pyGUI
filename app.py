import json
from datetime import datetime
import PySimpleGUI as sg
import subprocess
import serial.tools.list_ports

all_ports = serial.tools.list_ports.comports()
print(all_ports)
vals = []

window = None
arduino_port = None
arduino = None


def add_log_entry(data_to_log):
    global vals
    date_str = str(datetime.now())[:22]
    vals.insert(0, "{} {}".format(date_str, data_to_log))
    # max 1000 rows.
    vals = vals[:1000]
    index = 0
    if window:
        if len(window["-SCROLL-WINDOW-"].get_indexes()) and window["-SCROLL-WINDOW-"].get_indexes()[0]:
            index = window["-SCROLL-WINDOW-"].get_indexes()[0] + 1
        window["-SCROLL-WINDOW-"].update(vals, set_to_index=[index], scroll_to_index=index)


def try_connect():
    global arduino_port
    global arduino
    for port in all_ports:
        try:
            if port.name.find("USB") != -1 or port.name.find("usbserial") != -1:
                arduino_port = port
                add_log_entry("połączono z :" + arduino_port.device)
                arduino = serial.Serial(port=arduino_port.device, baudrate=9600, timeout=.1)
        except Exception as ex:
            add_log_entry("ex")
    if not arduino:
        add_log_entry("brak polaczenia")


try_connect()

if __name__ == '__main__':

    box = sg.Listbox(values=vals, enable_events=True, size=(145, 35), key="-SCROLL-WINDOW-", font=("Helvetica", 15))

    box.scroll_width = 100
    box.scroll_arrow_width = 100
    size = (20, 4)
    layout1 = [[sg.Button("GORA", size=size), sg.Button("POLACZ PONOWNIE", size=size)], [box]]
    layout2 = [
        [sg.Text('Czas wibracji:(s)', size=(25, 1), font='Courier 25'),
         sg.Slider(orientation='horizontal', key='vibrationDuration', default_value=10, range=(0, 20),
                   font='Courier 25', size=(20, 50)), ],
        [sg.Text('Interwał magazynu:', size=(25, 1), font='Courier 25'),
         sg.Slider(orientation='horizontal', key='magInterval', default_value=200, range=(100, 300), font='Courier 25',
                   size=(20, 50))],

        [sg.Text('Powtórzenia magazynu:', size=(25, 1), font='Courier 25'),
         sg.Slider(orientation='horizontal', key='magRepeats', default_value=5, range=(0, 10), font='Courier 25',
                   size=(20, 50))],
        [sg.Button("ZASTOSUJ USTAWIENIA", size=size), sg.Button("UPDATE", size=size), sg.Button("ZAMKNIJ", size=size)]
    ]

    layout = [[sg.TabGroup([[sg.Tab('Logi', layout1, font='Courier 45'),
                             sg.Tab('Ustawienia', layout2, font='Courier 45')]], font='Courier 45')]]

    window = sg.Window(title="Obrotnica", layout=layout, margins=(20, 20), no_titlebar=True, location=(0, 0),
                       size=(1024, 600), keep_on_top=True)

    while True:
        event, values = window.read(timeout=1)
        # read data from serial.

        if arduino:
            try:
                data = arduino.readline().strip()
                if data:
                    add_log_entry(data)
            except Exception as ex:
                date_str = str(datetime.now())[:22]
                vals.insert(0, "{} {}".format(date_str, "connection lost"))
                arduino = None
                arduino_port = None
                try_connect()

        if event == "ZASTOSUJ USTAWIENIA":
            mag_interval = values["magInterval"]
            mag_repeats = values["magRepeats"]
            vibration_duration = values["vibrationDuration"]

            settings = {"interval": mag_interval,
                        "repeats": mag_repeats,
                        "vibration_duration": vibration_duration}
            if arduino:
                json_str = json.dumps(settings)
                arduino.write(settings)
            pass

        if event == "POLACZ PONOWNIE":
            try_connect()

        if event == "ZAMKNIJ":
            break
        if event == "UPDATE":
            process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
            process.communicate()
            process2 = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE)
            break
        if event == "GORA":
            window["-SCROLL-WINDOW-"].update(vals, set_to_index=[0], scroll_to_index=0)

        if event == sg.WIN_CLOSED:
            break
