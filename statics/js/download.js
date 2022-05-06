
let download_bt = document.getElementById('download_bt')
let back_home = document.getElementById('back_home')

// 下载图片
download_bt.onclick = function(){
    let result_img = document.getElementById('result_img')
    let a = document.createElement('a')
    a.download = 'result'
    a.href = result_img.src
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
}

back_home.onclick = function(){
    window.location.replace('/')
}