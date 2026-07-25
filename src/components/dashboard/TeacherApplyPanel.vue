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
      <el-form-item label="试讲视频">
        <el-upload :auto-upload="false" :limit="1" :on-change="handleSampleVideo" :on-remove="() => (form.sampleVideo = null)">
          <el-button>选择视频文件</el-button>
        </el-upload>
      </el-form-item>
      <el-form-item label="资质证明">
        <el-upload :auto-upload="false" :limit="1" :on-change="handleCertificate" :on-remove="() => (form.certificateFile = null)">
          <el-button>选择证明文件</el-button>
        </el-upload>
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
import { submitTeacherApplicationApi } from '@/api/teacher'

const formRef = ref()
const form = reactive({
  name: '',
  phone: '',
  direction: '',
  experience: '',
  link: '',
  sampleVideo: null,
  certificateFile: null,
})

const rules = {
  name: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入联系方式', trigger: 'blur' }],
  direction: [{ required: true, message: '请选择授课方向', trigger: 'change' }],
  experience: [{ required: true, min: 10, message: '请至少填写 10 个字', trigger: 'blur' }],
}

function resetForm() {
  formRef.value.resetFields()
  form.sampleVideo = null
  form.certificateFile = null
}

function handleSampleVideo(file) {
  form.sampleVideo = file.raw
}

function handleCertificate(file) {
  form.certificateFile = file.raw
}

async function submitForm() {
  try {
    await formRef.value.validate()
    const formData = new FormData()
    formData.append('real_name', form.name)
    formData.append('phone', form.phone)
    formData.append('direction', form.direction)
    formData.append('experience', form.experience)
    formData.append('portfolio_url', form.link)
    if (form.sampleVideo) formData.append('sample_video', form.sampleVideo)
    if (form.certificateFile) formData.append('certificate_file', form.certificateFile)
    await submitTeacherApplicationApi(formData)
    await ElMessageBox.alert('申请已提交到后端。管理员会在 Django 后台审核，审核结果会通过邮件通知。', '提交成功', {
      confirmButtonText: '知道了',
    })
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.warning('请先完善申请信息')
    }
  }
}
</script>
