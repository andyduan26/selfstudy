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
