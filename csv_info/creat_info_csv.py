import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "neuron_retrieval_py36.settings")
import django
django.setup()
import csv


ROOT_DIR = 'S:/FTRE/CNN/neuron_retrieval/'


def creat_info_csv(name, list):
    l = []
    l.append(name)
    l.extend(list)
    all_file = os.listdir(ROOT_DIR + '/CSV')
    # all_file = os.listdir("./CSV")
    if len(all_file) != 0:
        for i in all_file:
            print(i)
            path = ROOT_DIR + "CSV/{}".format(i)
            os.remove(path)
    path = ROOT_DIR + "CSV/{}.csv".format(name)
    for i in l:
        with open(path, 'a') as m:
            m_csv = csv.writer(m)
            m_csv.writerow([i])

