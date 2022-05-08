from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .edgeConnect.main_invoke import inpaintingImg
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.template.loader import get_template
from Inpainting.models import *
import random
import time
import cv2
import numpy as np


def index(request):
    if request.method == 'GET':
        ticket = request.COOKIES.get('ticket')
        email = request.COOKIES.get('email')
        if not ticket:
            return HttpResponseRedirect('/login/')
        if User.objects.filter(ticket=ticket).exists():
            user = User.objects.get(email=email)
            template = get_template('index.html')
            html = template.render(locals())
            return HttpResponse(html)


def download(request):
    if request.method == 'GET':
        ticket = request.COOKIES.get('ticket')
        email = request.COOKIES.get('email')
        if not ticket:
            return HttpResponseRedirect('/login/')
        if User.objects.filter(ticket=ticket).exists():
            user = User.objects.get(email=email)
            template = get_template('download.html')
            html = template.render(locals())
            return HttpResponse(html)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if(confirm_password != password):
            messages.warning(request,'密码不一致！')
            return render(request,'register.html',locals())
        if User.objects.filter(email=email).exists():
            messages.warning(request,'邮箱已存在！')
            return render(request,'register.html',locals())
        password = make_password(password)
        User.objects.create(name=username, email=email, pwd=password)
        messages.success(request,'注册成功！')
        return render(request,'login.html',locals())
    return render(request, 'register.html')


def login(request):
    response = HttpResponseRedirect('/index/')
    ticket = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        # 查询用户是否在数据库中
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if check_password(password, user.pwd):
                exist_time = 3600 * 72   # max_age 存活时间(秒)
                if remember == 'on':
                    response.set_cookie('r_email', email, max_age=exist_time)
                    response.set_cookie('r_password', password, max_age=exist_time)
                else:
                    response.delete_cookie('r_email')
                    response.delete_cookie('r_password')
                response.set_cookie('remember', remember, max_age=exist_time)
                for i in range(15):
                    s = 'abcdefghijklmnopqrstuvwxyz'
                    ticket += random.choice(s)   # 获取随机的字符串
                now_time = int(time.time())
                ticket = 'TK' + ticket + str(now_time)
                # 绑定令牌到cookie里面
                response.set_cookie('ticket', ticket, max_age=exist_time)
                response.set_cookie('email', email, max_age=exist_time)
                # 存在服务端
                user.ticket = ticket
                user.save()  # 保存
                return response
            else:
                print('密码错误！')
                messages.warning(request,'密码错误！')
        else:
            print('账号不存在！')
            messages.warning(request,'账号不存在！')
    r_email = ''
    r_password = ''
    if request.COOKIES.get('remember') == 'on':
        r_email = request.COOKIES.get('r_email')
        r_password = request.COOKIES.get('r_password')
    return render(request,'login.html',locals())


def upload(request):
    if request.method == "POST":
        uploadImg = request.FILES.get("upload_img")
        email = request.COOKIES.get('email')
        user = User.objects.get(email=email)
        now = str(int(time.time()))
        suffix = uploadImg.name.split(".")[-1]
        upload_name = user.name+'_upload_'+now+'.'+suffix
        inputPath = './static/media/userStorage/' + upload_name
        with open(inputPath, 'wb') as f:
            f.write(uploadImg.read())
        user.upload_path = '/static/media/userStorage/' + upload_name
        user.save()
        print('上传成功！')
        return render(request, 'index.html')


def inpainting(request):
    if request.method == "POST":
        mask_img = request.FILES.get("mask_img")
        img_type = request.POST['img_type']
        email = request.COOKIES.get('email')
        user = User.objects.get(email=email)
        now = str(int(time.time()))
        mask_name = user.name+'_mask_'+now+'.png'
        mask_path = './static/media/userStorage/' + mask_name
        with open(mask_path, 'wb') as f:
            f.write(mask_img.read())

        img = cv2.imdecode(np.fromfile(
            mask_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        b, g, r = cv2.split(img)
        my_alpha = np.ones_like(b) * 255
        new_img = cv2.merge((b, g, r, my_alpha))
        cv2.imencode('.png', new_img)[1].tofile(mask_path)

        upload_path = user.upload_path
        upload_name = upload_path.split("/")[-1]
        suffix = upload_path.split(".")[-1]
        result_name = user.name+'_result_'+now+'.'+suffix
        output_path = '/static/media/userStorage/'+result_name

        masked_name = user.name+'_masked_'+now+'.'+suffix
        masked_path = '/static/media/userStorage/' + masked_name

        edge_name = user.name+'_edge_'+now+'.'+suffix
        edge_path = '/static/media/userStorage/' + edge_name

        print('开始修复')
        inpaintingImg(upload_name, img_type, mask_path,
                      masked_name, edge_name, result_name)

        user.mask_path = mask_path
        user.masked_path = masked_path
        
        user.edge_path = edge_path
        user.img_type = img_type
        user.result_path = output_path
        user.save()
        return render(request, 'index.html')


def logout(request):
    if request.method == 'GET':
        response = HttpResponseRedirect('/login/')
        response.delete_cookie('ticket')
        response.delete_cookie('email')
        return response
