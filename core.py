import easygui
import os
import sys
import csv
from datetime import datetime


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


if __name__ == "__main__":
    selected_pics_files = easygui.fileopenbox(
        msg='Select images', multiple=True)
    selected_event_file = str(easygui.fileopenbox(msg='Select pos_event file'))
    pics = get_pics(selected_pics_files)
    events = get_events(selected_event_file)
    length_difference = len(pics) - len(events)
    with open(selected_event_file + '.csv', 'w', newline='') as csvfile:
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
