import request from './request'

export function getMyRevenueSummaryApi() {
  return request.get('/api/revenues/my-summary/')
}
