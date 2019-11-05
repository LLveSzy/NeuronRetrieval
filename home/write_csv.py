import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "neuron_retrieval_py36.settings")
import django
django.setup()
import csv
import json
from home.models import Neuron


neuron_name = "/home/uestc-c1501e/neuron_retrieval/home/order_info.csv"
csv_reader = csv.reader(open(neuron_name))
info_list = [info for info in csv_reader]
path = "/home/uestc-c1501e/neuron_retrieval/home/nueron_info.csv"
i_csv = csv.reader(open(path, 'r'))
list_list = [i[1:] for i in i_csv]
# row = info_list[58369]
# info = Neuron(id=58369,
#     neuron_image = "/media/{}.png".format(row[2].strip()),
#     Archive_Name = row[0],
#     Species_Name = row[1],
#     Development = row[3],
#     Primary_Brain_Region = row[4],
#     Secondary_Brain_Region = row[5],
#     Tertiary_Brain_Region = row[6],
#     Primary_Cell_Class = row[7],
#     Secondary_Cell_Class = row[8],
#     Tertiary_Cell_Class = row[9],
#     Original_Format = row[10])
# info.save()

for i,row in enumerate(info_list):
    id = i+1
    info = Neuron(
    id=id,
    name = row[2].strip(),
    near_neuron_list = list_list[i],
    neuron_image = "/media/{}.png".format(row[2].strip()),
    Archive_Name = row[0],
    Species_Name = row[1],
    Development = row[3],
    Primary_Brain_Region = row[4],
    Secondary_Brain_Region = row[5],
    Tertiary_Brain_Region = row[6],
    Primary_Cell_Class = row[7],
    Secondary_Cell_Class = row[8],
    Tertiary_Cell_Class = row[9],
    Original_Format = row[10])
    info.save()



