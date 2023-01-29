import easygui
import os
import sys
import csv
from datetime import datetime
from msvcrt import getch
import traceback


def get_pics(selected_files):
    if selected_files is None:
        sys.exit(0)
    arr_pics = list()
    for files in selected_files:
        name = os.path.basename(files)
        mtime = os.path.getmtime(files)
        arr_pics.append(
            {'name': name, 'time': datetime.utcfromtimestamp(mtime)})
    return arr_pics


def get_events(selected_file):
    if selected_file is None:
        sys.exit(0)
    with open(selected_file, 'r') as file:
        reader = csv.reader(file, delimiter=' ', skipinitialspace=True)
        arr_events = list()
        # % GPST latitude(deg) longitude(deg) height(m) Q ns sdn(m) sde(m) sdu(m) sdne(m) sdeu(m) sdun(m) age(s) ratio
        for row in reader:
            if '%' in row[0]:
                continue
            arr_events.append({
                'time': datetime.strptime(f'{row[0]} {row[1]}', '%Y/%m/%d %H:%M:%S.%f'),
                'lat': row[2],
                'lon': row[3],
                'height': row[4],
                'sdn': row[7],
                'sdu': row[9],
                'sde': row[8]
            })
        return arr_events


def get_files():
    while True:
        pics = easygui.fileopenbox(
            msg='Select images', multiple=True)
        events = easygui.fileopenbox(msg='Select pos_event file')
        if pics and events:
            break
        else:
            res = easygui.ynbox(
                'Please read the title of dialog and select it respectively', title='Error', choices=('[<F1>]OK', '[<F2>]EXIT'))
            if not res:
                sys.exit(0)
    return {'pics_files': pics, 'event_file': events}


if __name__ == "__main__":
    try:
        selected = get_files()
        pics = get_pics(selected['pics_files'])
        events = get_events(selected['event_file'])
        length_difference = len(pics) - len(events)
        with open(str(selected['event_file']) + '.csv', 'w', newline='') as csvfile:
            fieldnames = ['name', 'lat', 'lon', 'height', 'sdn', 'sde', 'sdu']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(pics)):
                print(pics[i]['name'], '|', pics[i]['time'], '|', events[i]['time'],
                      '|', events[i]['time'] - pics[i]['time'])
                writer.writerow({'name': pics[i]['name'], 'lat': events[i]['lat'], 'lon': events[i]['lon'], 'height': events[i]
                                ['height'], 'sdn': events[i]['sdn'], 'sde': events[i]['sde'], 'sdu': events[i]['sdu']})
        if length_difference != 0:
            print(f'warning: {len(pics)} images | {len(events)} events')
    except Exception:
        traceback.print_exc()
    finally:
        print("Press any key to exit...")
        junk = getch()
