export function formatCourseWork(course) {
  return {
    id: course.id,
    title: course.title,
    status: course.status,
    categoryName: course.category_detail?.name || '未分类',
    description: course.description || '',
    price: Number(course.price || 0),
    priceText: Number(course.price) > 0 ? `¥${Number(course.price).toFixed(2)}` : '免费',
    students: course.sales_count || 0,
    viewCount: course.view_count || 0,
    income: '待结算',
    updatedAt: course.updated_at ? new Date(course.updated_at).toLocaleString('zh-CN') : '-',
  }
}

export function courseStatusLabel(status) {
  const labels = {
    draft: '草稿',
    pending: '待审核',
    approved: '已通过',
    rejected: '已驳回',
    published: '已发布',
    offline: '已下架',
  }
  return labels[status] || status
}

export function courseStatusType(status) {
  if (status === 'published' || status === 'approved') return 'success'
  if (status === 'pending') return 'warning'
  if (status === 'rejected') return 'danger'
  return 'info'
}
