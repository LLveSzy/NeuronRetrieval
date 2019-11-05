# coding=utf-8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "neuron_retrieval_py36.settings")
import django
django.setup()
import csv
path = '/home/uestc-c1501e/neuron_retrieval/media'
for file in os.listdir(path):
    u = os.path.basename(file)
    name = u[:-4]
    print(name)
    with open("really_name.csv", 'a') as m:
        m_csv = csv.writer(m)
        m_csv.writerow([name])
    # os.rename(os.path.join(path, file), os.path.join(path, u.strip()))
