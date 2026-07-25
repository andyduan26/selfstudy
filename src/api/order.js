import request from './request'

export function checkoutCourseApi(data) {
  return request.post('/api/orders/checkout/', data)
}
