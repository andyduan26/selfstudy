import request from './request'

export function getCurrentUser() {
  return request.get('/api/users/me/')
}
