let canvas = document.getElementById('canvas')
let upload_img = document.getElementById('upload_img')

let context = canvas.getContext('2d')
canvas.width = upload_img.width
canvas.height = upload_img.height
// 背景颜色
context.fillStyle = 'rgba(0, 0, 0, 0)'

// 线宽提示
let range = document.getElementById('customRange1')
range.oninput = function () {
    this.title = 'lineWidth: ' + this.value
}


let Mouse = { x: 0, y: 0 }
let lastMouse = { x: 0, y: 0 }
let painting = false

canvas.onmousedown = function () {
    painting = true
}

canvas.onmouseup = function () {
    painting = false
}

upload_img.onselectstart = function () {
    return false
}
canvas.onselectstart = function () {
    return false
}


canvas.onmousemove = function (e) {
    lastMouse.x = Mouse.x
    lastMouse.y = Mouse.y
    Mouse.x = e.pageX - this.offsetLeft
    Mouse.y = e.pageY - this.offsetTop
    if (painting) {
        /*
        画笔参数：
            linewidth: 线宽
            lineJoin: 线条转角的样式, 'round': 转角是圆头
            lineCap: 线条端点的样式, 'round': 线的端点多出一个圆弧
            strokeStyle: 描边的样式, 'white': 设置描边为白色
        */
        context.lineWidth = range.value
        context.lineJoin = 'round'
        context.lineCap = 'round'
        context.strokeStyle = 'white'

        // 开始绘画
        context.beginPath()
        context.moveTo(lastMouse.x, lastMouse.y);
        context.lineTo(Mouse.x, Mouse.y);
        context.closePath()
        context.stroke()
    }
}

// 上传图片
let upload_bt = document.getElementById('upload_bt')
let select_file = document.getElementById('select_file');
upload_bt.onclick = () => {
    select_file.click()
    select_file.onchange = function () {
        let fileData = this.files[0];
        let formData = new FormData();
        formData.append("upload_img", fileData);
        let upload_loading = document.getElementById('upload_loading')
        upload_loading.style.display = ''
        $.ajax({
            url: '/upload/',
            type: 'post',
            data: formData,
            contentType: false,
            processData: false,
            success: function () {
                alert('上传成功！')
                let upload_loading = document.getElementById('upload_loading')
                upload_loading.style.display = 'none'
                let reader = new FileReader();
                reader.readAsDataURL(fileData);
                reader.onload = function () {
                    upload_img.setAttribute("src", this.result)
                }
                canvas.width = upload_img.width
                canvas.height = upload_img.height
            },
            error: function () {
                inpainting_loading.style.display = 'none'
                alert('上传出错！')
            }
        })
    }
}

// 清空画布
let clean = document.getElementById('clean')
clean.onclick = function () {
    context.clearRect(0, 0, canvas.width, canvas.height)
    context.fillStyle = 'rgba(0, 0, 0, 0)'
    context.fillRect(0, 0, canvas.width, canvas.height)
}

// 修复（修复时上传掩摸图片）
let inpainting = document.getElementById('inpainting')
let img_type = document.getElementById('img_type')  // 图像类型
inpainting.onclick = function () {
    let canvas = document.getElementById('canvas')
    let b64Image = canvas.toDataURL('image/png')
    let u8Image = b64ToUint8Array(b64Image);
    let formData = new FormData();
    formData.append("mask_img", new Blob([u8Image], { type: "image/png" }));
    formData.append("img_type", img_type.value)  //1.人像  2.风景
    let inpainting_loading = document.getElementById('inpainting_loading')
    inpainting_loading.style.display = ''
    $.ajax({
        url: '/inpainting/',
        type: 'post',
        data: formData,
        contentType: false,
        processData: false,
        success: function () {
            inpainting_loading.style.display = 'none'
            alert('修复完成！')
            window.location.replace("/download/");
        },
        error: function () {
            inpainting_loading.style.display = 'none'
            alert('修复出错！')
        }
    })
}


function b64ToUint8Array(b64Image) {
    let img = atob(b64Image.split(',')[1]);
    let img_buffer = [];
    let i = 0;
    while (i < img.length) {
        img_buffer.push(img.charCodeAt(i));
        i++;
    }
    return new Uint8Array(img_buffer);
}