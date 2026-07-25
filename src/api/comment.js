import request from './request'

export async function getCourseCommentsApi(courseId) {
  const data = await request.get('/api/comments/', { params: { course: courseId } })
  return data.results || data
}

export function createCourseCommentApi(data) {
  return request.post('/api/comments/', data)
}
