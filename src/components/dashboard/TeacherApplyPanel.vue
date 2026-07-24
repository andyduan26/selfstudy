<template>
  <div class="center-panel">
    <div class="panel-heading">
      <div>
        <h2>讲师入驻申请</h2>
        <p>提交你的教学方向与经历，平台审核通过后自动开通讲师工作台。</p>
      </div>
      <el-tag effect="plain">普通用户可见</el-tag>
    </div>

    <el-steps :active="1" finish-status="success" class="apply-steps">
      <el-step title="填写资料" />
      <el-step title="平台审核" />
      <el-step title="开通讲师" />
    </el-steps>

    <el-form ref="formRef" :model="form" :rules="rules" label-position="top" class="center-form">
      <el-row :gutter="24">
        <el-col :span="12">
          <el-form-item label="真实姓名" prop="name">
            <el-input v-model="form.name" placeholder="请输入真实姓名" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="联系方式" prop="phone">
            <el-input v-model="form.phone" placeholder="请输入手机号" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item label="授课方向" prop="direction">
        <el-select v-model="form.direction" placeholder="请选择授课方向">
          <el-option label="前端开发" value="frontend" />
          <el-option label="后端开发" value="backend" />
          <el-option label="办公效率" value="office" />
          <el-option label="AI 工具" value="ai" />
        </el-select>
      </el-form-item>
      <el-form-item label="教学经历" prop="experience">
        <el-input v-model="form.experience" type="textarea" :rows="4" placeholder="请简要介绍你的课程经验、项目经验或擅长内容" />
      </el-form-item>
      <el-form-item label="代表作品链接">
        <el-input v-model="form.link" placeholder="可填写公开视频、文章或作品链接" />
      </el-form-item>
      <div class="form-actions">
        <el-button @click="resetForm">重置</el-button>
        <el-button type="primary" @click="submitForm">提交申请</el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const formRef = ref()
const form = reactive({
  name: '',
  phone: '',
  direction: '',
  experience: '',
  link: '',
})

const rules = {
  name: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入联系方式', trigger: 'blur' }],
  direction: [{ required: true, message: '请选择授课方向', trigger: 'change' }],
  experience: [{ required: true, min: 10, message: '请至少填写 10 个字', trigger: 'blur' }],
}

function resetForm() {
  formRef.value.resetFields()
}

async function submitForm() {
  try {
    await formRef.value.validate()
    await ElMessageBox.alert('申请已提交。当前为静态演示，审核流程后续可对接后端。', '提交成功', {
      confirmButtonText: '知道了',
    })
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.warning('请先完善申请信息')
    }
  }
}
</script>
