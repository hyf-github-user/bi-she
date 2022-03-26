from qiniu import Auth, put_data


def upload_qiniu(filestorage):
    access_key = "KSH6HWWJCKZHYyPyRRITljLkqEt3cJ0QYdUPMoar"
    secret_key = "-X0yBa3CVu6s39i2KzqAV4jBj-a7clmttyCqNJAf"

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'hyf-test'

    # 设置 上传之后保存文件的名字
    filename = 'qiniu_' + filestorage.filename

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, filename, 3600)

    # put_file()
    ret, info = put_data(token, filename, filestorage.read())
    print(ret, info)

    if info.status_code == 200:
        url = 'http://huyinfu.shop/' + filename
        return url
    return None

import sys
sys.executable()
