import request from './request'

export function loginApi(data) {
  return request.post('/api/auth/token/', {
    username: data.account,
    password: data.password,
  })
}

export function registerApi(data) {
  return request.post('/api/users/register/', {
    email: data.email,
    nickname: data.nickname,
    phone: data.phone,
    password: data.password,
    role: data.role,
  })
}

export function getCurrentUserApi() {
  return request.get('/api/users/me/')
}

export function updateCurrentUserApi(data) {
  return request.patch('/api/users/me/', data)
}
