# -*- coding:utf-8 -*-
from flask import abort, jsonify
from common.db import DB
from common.saltstack_api import SaltAPI
import uuid
import base64
from common.log import loggers
from common.redis import RedisTool
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5

logger = loggers()


def uuid_prefix(prefix):
    str_uuid = str(uuid.uuid1())
    s_uuid = ''.join(str_uuid.split("-"))
    return prefix + "-" + s_uuid


def salt_api_for_product(product_id):
    db = DB()
    status, result = db.select_by_id("product", product_id)
    db.close_mysql()
    if status is True:
        if result:
            product = result
        else:
            return {"status": False, "message": "product %s does not exist" % product_id}
    else:
        return {"status": False, "message": result}
    salt_api = SaltAPI(
        url=product.get("salt_master_url"),
        user=product.get("salt_master_user"),
        passwd=product.get("salt_master_password")
    )
    return salt_api


# 重新定义flask restful 400错误
def custom_abort(http_status_code, *args, **kwargs):
    if http_status_code == 400:
        if kwargs:
            for key in kwargs["message"]:
                parameter = key
        else:
            parameter = "unknown"
        abort(jsonify({"status": False, "message": "The specified %s parameter does not exist" % parameter}))
    return abort(http_status_code)


# 生成秘钥对
def generate_key_pair():
    # 伪随机数生成器
    random_generator = Random.new().read
    # rsa算法生成实例
    rsa = RSA.generate(1024, random_generator)
    # 私钥
    private_key = rsa.exportKey()
    RedisTool.setex("private_key", 24 * 60 * 60, private_key)
    # 公钥
    public_key = rsa.publickey().exportKey()
    RedisTool.setex("public_key", 24 * 60 * 60, public_key)


# 解密RSA
def rsa_decrypt(encrypt_text):
    try:
        random_generator = Random.new().read
        private_key = RedisTool.get("private_key")
        rsa_key = RSA.importKey(private_key)
        cipher = Cipher_pkcs1_v1_5.new(rsa_key)
        text = cipher.decrypt(base64.b64decode(encrypt_text), random_generator)
        return text
    except Exception as e:
        logger.error("Decrypt rsa error: %s" % e)
        return False
