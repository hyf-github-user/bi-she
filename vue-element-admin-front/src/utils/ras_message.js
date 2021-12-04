import { JSEncrypt } from 'jsencrypt'

function rsa_en(pubkey, target_str) {
  /**
  分段加密信息

  :params target_str: 需要加密的信息，此处为很长的信息
  :pubkey: 公钥
  :return: 存储密文的数组
  **/
  const encrypt = new JSEncrypt()
  encrypt.setPublicKey(pubkey)
  const result = encrypt.encrypt(JSON.stringify(target_str))
}
