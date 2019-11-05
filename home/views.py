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
#from home.featherExtract import featherEtr
from home.SWCutil import SWCutil
import gc
#from home.searchNeuron import search
from home.featherKeras import featherEtrKeras
from home.featherModel import searchNeuronServer



# Create your views here.
height = 128
width = 128
root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def dfs(tr, color, neuron_list, tree, res):
    if len(tree[tr]) is 0:
        res[-1].append([float(neuron_list[tr][1]),
                        float(neuron_list[tr][2]),
                        float(neuron_list[tr][3]),
                        float(neuron_list[tr][4])])
        # print(str(tr) + "\n")
        res.append([])
        return
    if color is not neuron_list[tr][1]:
        res[-1].append([float(neuron_list[tr][1]),
                        float(neuron_list[tr][2]),
                        float(neuron_list[tr][3]),
                        float(neuron_list[tr][4])])
        res.append([])
        res[-1].append([float(neuron_list[tr][1]),
                        float(neuron_list[tr][2]),
                        float(neuron_list[tr][3]),
                        float(neuron_list[tr][4])])
    for i in range(len(tree[tr])):
        res[-1].append([float(neuron_list[tr][1]),
                        float(neuron_list[tr][2]),
                        float(neuron_list[tr][3]),
                        float(neuron_list[tr][4])])
        # print(str(tr) + " ")
        dfs(tree[tr][i], neuron_list[tr][1], neuron_list, tree, res)


def get_neuron_list(files):
    neuron_list = []
    tree = []
    res = [[]]
    print(files)
    with open(files, encoding='utf-8') as f:
        for line in f:
            if '#' not in line and line is not "\n":
                line = line[1:].strip('\n')
                neuron_list.append(line.split(" "))
    N = len(neuron_list)
    for i in range(N):
        tree.append([])
    for i in range(1, N):
        tree[int(neuron_list[i][6]) - 1].append(i)
    dfs(0,  neuron_list[0][1], neuron_list, tree, res)
    return res


def get_arr(request):
    swcFile = request.FILES.get('myfile', None)  # 获取上传的文件，如果没有文件，则默认为None
    print(swcFile.name)
    if not swcFile:
        return HttpResponse("no files for upload!")
    swc_temp_path = root + '/data/tmp/'
    path = os.path.join(swc_temp_path, swcFile.name)
    destination = open(path, 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in swcFile.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    res0 = get_neuron_list(root + '/data/tmp/' + swcFile.name)
    res = str(res0)
    # res = "["
    # for i in range(len(res0)):
    #     res += "["
    #     for j in range(len(res0[i])-1):
    #         res += "["
    #         for k in range(len(res0[i][j])):
    #             res += str(res0[i][j][k])
    #             if k != len(res0[i][j]) - 1:
    #                 res += ","
    #         res += "]"
    #         if j != len(res0[i]) - 1:
    #             res += ","
    #     res += "]"
    #     if k != len(res0) - 1:
    #         res += ","
    # res += "]"

    return HttpResponse(res)
    # return render(request, "index.html", {'custom': res})


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
                    print(q)
                neuron_name_list = []
                for i in neuron_list:
                    neuron_name_list.append("{}.png".format(Neuron.objects.get(id=i).name))
                list = [i[:-4] for i in neuron_name_list]
                creat_info_csv(name, list)
                return render(request, "index.html", {'images_list': neuron_name_list, 'name': "{}.png".format(name)})

    if request.method == 'POST':
        swcFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
        print(swcFile)
        if not swcFile:
            return HttpResponse("no files for upload!")
        swc_temp_path=root + '/data/swc_temp/'
        path = os.path.join(swc_temp_path, swcFile.name)
        destination = open(path, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in swcFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        swc = SWCutil(path)
        mat = swc.draw_mat(height, width)
        np.save(swc_temp_path + swcFile.name[0:-4] + ".npy", mat)
        sn = searchNeuronServer()
        fe = featherEtrKeras()
        test_fea = fe.get_feather([swc_temp_path + swcFile.name[0:-4] + ".npy"])
        index, list = sn.search(test_fea, 10)

        neuron_list = []
        name_list = []
        imagelist=[]
        print(list)
        #         # for l in list:
        #         #     if 'el' in l:
        #         #         imagelist.append(l[10:-8])
        #         #     else:
        #         #         imagelist.append(l[9:-8])
        #         # del swc, test_fea, sn, fe
        #         # gc.collect()
        for i in range(len(list)):
            neuron_list.append(get_neuron_list('S:/FTRE/CNN/SWC files/allSwc/' + list[i]))
            # neuron_list.append(get_neuron_list( root + '/data/swc_temp/' + list[i]))
            #neuron_list.append(get_neuron_list(root + '/data/swc_temp/aele00019_Control-4.CNG.swc'))
            if 'el' in list[i]:
                name_list.append(list[i][10:-8])
            else:
                name_list.append(list[i][9:-8])
        return render(request, "index.html", {'images_list': neuron_list, 'neuron_name': name_list})
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
