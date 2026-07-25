export const teacherStats = [
  { label: '累计学员', value: '32,860', desc: '较上月 +12%' },
  { label: '课程播放', value: '186,400', desc: '本月新增 28,600' },
  { label: '本月收益', value: '¥18,920', desc: '待结算 ¥4,200' },
  { label: '课程评分', value: '4.9', desc: '近 90 天稳定' },
]

export const teacherWorks = [
  { id: 1, title: 'Vue3 零基础入门到项目实战', status: '已发布', students: 12860, income: '¥8,420', updatedAt: '2026-07-20' },
  { id: 2, title: 'Element Plus 后台界面设计', status: '审核中', students: 7800, income: '¥5,300', updatedAt: '2026-07-18' },
  { id: 3, title: '前端项目结构与规范课', status: '草稿', students: 0, income: '¥0', updatedAt: '2026-07-12' },
]

export const teacherReviews = [
  { id: 1, course: 'Vue3 零基础入门到项目实战', user: '林同学', rating: '5.0', content: '课程节奏很清楚，适合零基础跟着做项目。', date: '2026-07-22' },
  { id: 2, course: 'Element Plus 后台界面设计', user: '陈同学', rating: '4.9', content: '表单、表格和权限部分讲得很实用。', date: '2026-07-19' },
  { id: 3, course: '前端项目结构与规范课', user: '周同学', rating: '4.8', content: '目录设计和代码规范部分帮助很大。', date: '2026-07-16' },
]

export const teacherTodos = [
  { id: 1, title: '审核中作品', value: '1 门', desc: 'Element Plus 后台界面设计等待平台审核' },
  { id: 2, title: '待回复评价', value: '3 条', desc: '优先回复近 7 天新增高质量评价' },
  { id: 3, title: '待结算收益', value: '¥4,200', desc: '结算完成后可提交提现申请' },
]

export const incomeRows = [
  { month: '2026-07', course: 'Vue3 零基础入门到项目实战', amount: '¥8,420', status: '待结算' },
  { month: '2026-07', course: 'Element Plus 后台界面设计', amount: '¥5,300', status: '可提现' },
  { month: '2026-06', course: 'Vue3 零基础入门到项目实战', amount: '¥5,200', status: '已提现' },
]

export const withdrawRows = [
  { id: 'TX2026071801', amount: '¥3,000', account: '招商银行 尾号 0826', status: '处理中', date: '2026-07-18' },
  { id: 'TX2026062801', amount: '¥5,200', account: '支付宝 duan***@mail.com', status: '已到账', date: '2026-06-28' },
]
