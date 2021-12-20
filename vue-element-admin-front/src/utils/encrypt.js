const CryptoJs = require('crypto-js')
function encrypt(...args) {
  const time = Math.round(new Date().getTime() / 1000).toString()
  args.push(time)
  const sign = CryptoJs.SHA1(args.join(',')).toString(CryptoJs.enc.Hex)
  const string = CryptoJs.enc.Base64.stringify(CryptoJs.enc.Utf8.parse([sign, time].join(','))).toString()
  return string
}
