
from datetime import datetime
import PySimpleGUI as sg
import subprocess


if __name__ == '__main__':
    vals =["1", "231", "321", "22221", "223231", "2323231", "3232321"]
    box = sg.Listbox(values=vals, enable_events=True, size=(145, 40),
        key="-SCROLL-WINDOW-"
    )



    for i in range(10):
        vals.append("xxx")
    box.scroll_width =100
    box.scroll_arrow_width=100
    layout = [[box], [sg.Button("OK"), sg.Button("TOP"), sg.Button("HOLD"), sg.Button("UPDATE"), sg.Button("CLOSE")]]
    window = sg.Window(title="Obrotnica", layout=layout, margins=(20, 20), no_titlebar=True, location=(0, 0), size=(1024, 600), keep_on_top=True)
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
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
        if event == "OK":
            vals.insert(0, str(datetime.now()))
            vals = vals[:1000]

            index = 0
            if len(window["-SCROLL-WINDOW-"].get_indexes()) and window["-SCROLL-WINDOW-"].get_indexes()[0]:
                index = window["-SCROLL-WINDOW-"].get_indexes()[0] + 1
            window["-SCROLL-WINDOW-"].update(vals, set_to_index=[index], scroll_to_index=index)
            pass
        elif event == sg.WIN_CLOSED:
            break



