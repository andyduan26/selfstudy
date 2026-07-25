import request from './request'

export function submitTeacherApplicationApi(formData) {
  return request.post('/api/teacher-applications/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export function uploadTeacherWorkApi(formData) {
  return request.post('/api/courses/upload-work/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export function getTeacherWorksApi() {
  return request.get('/api/courses/my-works/')
}

export function updateTeacherWorkApi(id, data) {
  return request.patch(`/api/courses/${id}/my-update/`, data)
}

export function deleteTeacherWorkApi(id) {
  return request.delete(`/api/courses/${id}/my-delete/`)
}
