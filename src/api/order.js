import request from './request'

export function checkoutCourseApi(data) {
  return request.post('/api/orders/checkout/', data)
}

export function createAlipayQrcodeApi(data) {
  return request.post('/api/orders/alipay-qrcode/', data)
}

export function getOrderStatusApi(orderId) {
  return request.get(`/api/orders/${orderId}/status/`)
}
