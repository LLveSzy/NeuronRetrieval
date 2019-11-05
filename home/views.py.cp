# coding: utf-8
import re
import os
import numpy as np
import json
from .models import Neuron
from csv_info.creat_info_csv import creat_info_csv
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from home.featherExtract import featherEtr
from home.SWCutil import SWCutil
from home.searchNeuron import search



# Create your views here.
height = 128
width = 128

def home_page(request):
    if 'home_auth' not in request.session:
        url = '/home/auth/?next=/home/main/'
        return HttpResponseRedirect(url)
    if request.method == 'GET':
        name = request.GET.get('file0', None)
        #没有上传东西的时候
        if name is None or len(name) == 0:
            p = request.session.get("name", None)
            if p is None:
                name = "0-2c"
                neuron = Neuron.objects.get(name=name)
                l = neuron.near_neuron_list
                m = l[1:-1].split(",")
                neuron_list = []
                for i in m:
                    o = re.sub("\D", "", i)
                    neuron_list.append(int(o))
                neuron_name_list = []
                for i in neuron_list:
                    neuron_name_list.append("{}.png".format(Neuron.objects.get(id=i).name))
                list = [i[:-4] for i in neuron_name_list]
                creat_info_csv(name, list)
                return render(request, "index.html", {'images_list': neuron_name_list})
            if p is not None:
                name = p
                neuron = Neuron.objects.get(name=name)
                l = neuron.near_neuron_list
                m = l[1:-1].split(",")
                neuron_list = []
                for i in m:
                    o = i.decode("string_escape")
                    q = filter(str.isdigit,
                               o.encode("utf-8"))
                    neuron_list.append(int(q))
                neuron_name_list = []
                for i in neuron_list:
                    neuron_name_list.append("{}.png".format(Neuron.objects.get(id=i).name))
                list = [i[:-4] for i in neuron_name_list]
                creat_info_csv(name, list)
                return render(request, "index.html", {'images_list': neuron_name_list, 'name': "{}.png".format(name)})

    if request.method == 'POST':
        swcFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not swcFile:
            return HttpResponse("no files for upload!")
        swc_temp_path='/var/neuron_retrieval/data/swc_temp/'
        path = os.path.join(swc_temp_path, swcFile.name)
        destination = open(path, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in swcFile.chunks():  # 分块写入文件
            destination.write(chunk)
            destination.close()
        swc = SWCutil(path)
        mat = swc.draw_mat(height, width)
        #swc_temp_path = '/var/neuron_retrieval/data/swc_temp/'
        np.save(swc_temp_path + swcFile.name[0:-4] + ".npy", mat)
        fea = featherEtr()
        feather = fea.get_feather(swc_temp_path + swcFile.name[0:-4] + ".npy")
        np.save(swc_temp_path + swcFile.name[0:-4] + "fea.npy",feather)
        list = search(feather)
        imagelist=[]
        for l in list:
            imagelist.append(l[0][9:-8]+'.png')
        
        # return HttpResponse("upload over!" + feather)
        # return HttpResponse(index)
        return render(request, "index.html", {'images_list': imagelist})
        # return render(request, "index.html", {'images_list': [], 'name': "{}.png".format(name)})


#@login_required(login_url='/home/auth/')
def detail_page(request):
    if 'home_auth' not in request.session:
        url = '/home/auth/?next=/home/detail/'
        return HttpResponseRedirect(url)
    name = request.session.get("name", "0-2c")
    n = name
    neuron = Neuron.objects.filter(name=name)
    l = neuron[0].near_neuron_list
    m = l[1:-1].split(",")
    neuron_list = []
    for i in m:
        o = i.decode("string_escape")
        q = filter(str.isdigit,
                   o.encode("utf-8"))

        neuron_list.append(int(q))
    neuron_name_list = []
    for i in neuron_list:
        neuron_name_list.append(Neuron.objects.get(id=i))
    return render(request, "detail_index.html", {'all_neuron_list': neuron_name_list, 'name': "{}.png".format(n)})

def auth_page(request):
    msg = ''
    if 'home_auth' in request.session:
        url = '/home/main/'
        return HttpResponseRedirect(url)
    if request.method == 'POST':
        token = request.POST.get('test', '')
        if token == '123123a':
            request.session['home_auth'] = 1
            url = request.GET.get('next', '')
            if url == '':
                url = '/home/main/'
            return HttpResponseRedirect(url)
        else:
            msg = 'The password is incorrect'
    return render(request, 'auth.html', {'msg': msg})
