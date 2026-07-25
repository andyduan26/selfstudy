import request from './request'

export async function getCoursesApi() {
  const data = await request.get('/api/courses/')
  return data.results || data
}

export function getCourseApi(id) {
  return request.get(`/api/courses/${id}/`)
}
