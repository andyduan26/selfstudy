export const adminStats = [
  { label: '注册用户', value: '48,260', desc: '今日新增 126' },
  { label: '认证讲师', value: '328', desc: '待审核 18' },
  { label: '作品总数', value: '1,286', desc: '待审核 42' },
  { label: '订单金额', value: '¥286,900', desc: '本月成交' },
]

export const adminUsers = [
  { id: 1001, name: '王小雨', phone: '138****0921', role: '普通用户', status: '正常', orders: 8, createdAt: '2026-07-20' },
  { id: 1002, name: '林亦辰', phone: '136****8276', role: '讲师', status: '正常', orders: 22, createdAt: '2026-07-18' },
  { id: 1003, name: '赵明', phone: '139****6620', role: '普通用户', status: '禁用', orders: 1, createdAt: '2026-07-12' },
  { id: 1004, name: '陈知夏', phone: '137****5188', role: '讲师', status: '正常', orders: 34, createdAt: '2026-07-10' },
]

export const teacherAudits = [
  { id: 2001, name: '顾南乔', direction: 'AI 工具', experience: '5 年内容生产经验', status: '待审核', submittedAt: '2026-07-21' },
  { id: 2002, name: '沈墨', direction: '设计创作', experience: '独立 UI 设计师', status: '已通过', submittedAt: '2026-07-18' },
  { id: 2003, name: '周明远', direction: '后端开发', experience: '企业后端架构师', status: '待补充', submittedAt: '2026-07-16' },
]

export const workAudits = [
  { id: 3001, title: 'Vue3 组件化项目实战', teacher: '林亦辰', category: '前端开发', status: '待审核', lessons: 36, submittedAt: '2026-07-22' },
  { id: 3002, title: 'Excel 效率提升 30 讲', teacher: '陈知夏', category: '办公效率', status: '已通过', lessons: 30, submittedAt: '2026-07-19' },
  { id: 3003, title: 'AI 提示词基础课', teacher: '顾南乔', category: 'AI 工具', status: '驳回', lessons: 18, submittedAt: '2026-07-17' },
]

export const adminOrders = [
  { id: 'OD20260722001', user: '王小雨', course: 'Vue3 零基础入门到项目实战', amount: '¥199', status: '已支付', paidAt: '2026-07-22' },
  { id: 'OD20260721002', user: '赵明', course: 'Django REST Framework 接口开发', amount: '¥199', status: '退款中', paidAt: '2026-07-21' },
  { id: 'OD20260718003', user: '刘晨', course: 'Element Plus 后台界面设计', amount: '¥129', status: '已完成', paidAt: '2026-07-18' },
]

export const withdrawAudits = [
  { id: 'TX2026072201', teacher: '林亦辰', amount: '¥5,300', account: '招商银行 尾号 0826', status: '待审核', submittedAt: '2026-07-22' },
  { id: 'TX2026071801', teacher: '陈知夏', amount: '¥3,000', account: '支付宝 chen***@mail.com', status: '已打款', submittedAt: '2026-07-18' },
  { id: 'TX2026071501', teacher: '周明远', amount: '¥2,600', account: '建设银行 尾号 7319', status: '驳回', submittedAt: '2026-07-15' },
]
