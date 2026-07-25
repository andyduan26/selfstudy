import base64
import json
from urllib.parse import urlencode

from django.conf import settings
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


GATEWAYS = {
    'sandbox': 'https://openapi-sandbox.dl.alipaydev.com/gateway.do',
    'production': 'https://openapi.alipay.com/gateway.do',
}


class AlipayConfigError(Exception):
    pass


def is_configured():
    return bool(settings.ALIPAY_APP_ID and settings.ALIPAY_APP_PRIVATE_KEY and settings.ALIPAY_PUBLIC_KEY)


def build_page_pay_url(order):
    _require_config()
    params = {
        'app_id': settings.ALIPAY_APP_ID,
        'method': 'alipay.trade.page.pay',
        'format': 'JSON',
        'charset': 'utf-8',
        'sign_type': 'RSA2',
        'timestamp': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'version': '1.0',
        'notify_url': settings.ALIPAY_NOTIFY_URL,
        'return_url': settings.ALIPAY_RETURN_URL,
        'biz_content': json.dumps({
            'out_trade_no': order.order_no,
            'product_code': 'FAST_INSTANT_TRADE_PAY',
            'total_amount': str(order.amount),
            'subject': order.course.title[:128],
        }, ensure_ascii=False, separators=(',', ':')),
    }
    params['sign'] = _sign(params)
    return f'{GATEWAYS[settings.ALIPAY_ENV]}?{urlencode(params)}'


def verify_notify(data):
    _require_config()
    sign = data.get('sign')
    if not sign:
        return False
    unsigned = {key: value for key, value in data.items() if key not in ('sign', 'sign_type') and value != ''}
    message = _build_sign_content(unsigned).encode('utf-8')
    public_key = RSA.import_key(_normalize_public_key(settings.ALIPAY_PUBLIC_KEY))
    try:
        pkcs1_15.new(public_key).verify(SHA256.new(message), base64.b64decode(sign))
        return True
    except (ValueError, TypeError):
        return False


def _require_config():
    if not is_configured():
        raise AlipayConfigError('支付宝沙箱参数未配置，请先在 backend/.env 配置 APP_ID、应用私钥和支付宝公钥')
    if settings.ALIPAY_ENV not in GATEWAYS:
        raise AlipayConfigError('ALIPAY_ENV 只能填写 sandbox 或 production')


def _sign(params):
    private_key = RSA.import_key(_normalize_private_key(settings.ALIPAY_APP_PRIVATE_KEY))
    signature = pkcs1_15.new(private_key).sign(SHA256.new(_build_sign_content(params).encode('utf-8')))
    return base64.b64encode(signature).decode('utf-8')


def _build_sign_content(params):
    return '&'.join(f'{key}={params[key]}' for key in sorted(params) if params[key] not in (None, ''))


def _normalize_private_key(value):
    value = value.replace('\\n', '\n').strip()
    if 'BEGIN' in value:
        return value
    return f'-----BEGIN PRIVATE KEY-----\n{_wrap_key(value)}\n-----END PRIVATE KEY-----'


def _normalize_public_key(value):
    value = value.replace('\\n', '\n').strip()
    if 'BEGIN' in value:
        return value
    return f'-----BEGIN PUBLIC KEY-----\n{_wrap_key(value)}\n-----END PUBLIC KEY-----'


def _wrap_key(value):
    compact = ''.join(value.split())
    return '\n'.join(compact[index:index + 64] for index in range(0, len(compact), 64))
