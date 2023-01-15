from datetime import datetime
import PySimpleGUI as sg
import subprocess
import serial.tools.list_ports

all_ports = serial.tools.list_ports.comports()
print(all_ports)
vals = []

arduino_port = None

for port in all_ports:
    if port.name.find("USB") != -1 or port.name.find("usbserial") != -1:
        arduino_port = port
        print(arduino_port.device)
arduino = None

if arduino_port:
    arduino = serial.Serial(port=arduino_port.device, baudrate=9600, timeout=.1)
else:
    vals.append("no connection");

if __name__ == '__main__':

    box = sg.Listbox(values=vals, enable_events=True, size=(145, 35), key="-SCROLL-WINDOW-", font=("Helvetica", 15))

    box.scroll_width = 100
    box.scroll_arrow_width = 100
    size = (11, 3)
    layout1 = [[sg.Button("GORA", size=size)], [box]]
    layout2 = [
        [sg.Text('Czas wibracji:(s)', size=(25, 1), font='Courier 25'), sg.Slider(orientation ='horizontal', key='stSlider', range=(0,20), font='Courier 25',size=(20,50)), ],
        [sg.Text('Powtorzenia magazynu:', size=(25, 1), font='Courier 25'), sg.Slider(orientation ='horizontal', key='stSlider', range=(0,10), font='Courier 25', size=(20,50))],
        [sg.Button("UPDATE", size=size), sg.Button("ZAMKNIJ", size=size)]
    ]

    layout = [[sg.TabGroup([[sg.Tab('Logi', layout1, font='Courier 45'),
                             sg.Tab('Ustawienia', layout2, font='Courier 45')]], font='Courier 45')]]

    window = sg.Window(title="Obrotnica", layout=layout, margins=(20, 20), no_titlebar=True, location=(0, 0),
                       size=(1024, 600), keep_on_top=True)

    while True:
        event, values = window.read(timeout=1)
        # read data from serial.
        if arduino:
            data = arduino.readline().strip()

            if data:
                date_str = str(datetime.now())[:22]

                vals.insert(0, "{} {}".format(date_str, data))
                # max 1000 rows.
                vals = vals[:1000]
                index = 0
                if len(window["-SCROLL-WINDOW-"].get_indexes()) and window["-SCROLL-WINDOW-"].get_indexes()[0]:
                    index = window["-SCROLL-WINDOW-"].get_indexes()[0] + 1
                window["-SCROLL-WINDOW-"].update(vals, set_to_index=[index], scroll_to_index=index)

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
