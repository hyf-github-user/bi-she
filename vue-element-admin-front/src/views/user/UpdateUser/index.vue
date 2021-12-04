<template>
  <el-form ref="ruleForm" :model="ruleForm" :rules="rules" label-width="100px" class="demo-ruleForm">
    <el-form-item label="注册时间">
      <el-input v-model="ruleForm.register_time" readonly />
    </el-form-item>

    <el-form-item label="用户ID">
      <el-input v-model="ruleForm.id" readonly />
    </el-form-item>

    <el-form-item label="登录名" prop="username">
      <el-input v-model="ruleForm.username" />
    </el-form-item>

    <el-form-item label="用户名" prop="name">
      <el-input v-model="ruleForm.name" />
    </el-form-item>

    <el-form-item label="登录密码" prop="rsa_password_hash">
      <el-input v-model="ruleForm.rsa_password_hash" readonly />
    </el-form-item>

    <el-form-item label="邮箱" prop="auth">
      <el-input v-model="ruleForm.email" />
    </el-form-item>

    <el-form-item label="级别" prop="auth">
      <el-input v-model="ruleForm.auth" />
    </el-form-item>

    <el-form-item label="激活状态" prop="active">
      <el-input v-model="ruleForm.active" />
    </el-form-item>

    <el-form-item label="确认状态" prop="confirmed">
      <el-input v-model="ruleForm.confirmed" />
    </el-form-item>

    <el-form-item label="锁定状态" prop="locked">
      <el-input v-model="ruleForm.locked" />
    </el-form-item>

    <el-form-item label="身份信息" prop="role_id">
      <el-input v-model="ruleForm.role_id" />
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">更新用户</el-button>
      <el-button @click="resetForm('ruleForm')">重置</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import { getById, updateUser } from '@/api/user'

export default {
  data() {
    return {
      ruleForm: null,
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    getById(this.$route.query.id).then((response) => {
      if (response.code === 200) {
        console.log('response=====', response)
        this.ruleForm = response.data
      }
    })
  },
  methods: {
    formatter(row) {
      return row.sex === '0' ? '男' : '女'
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => { // 校验表单数据
        if (valid) {
          console.log(this.ruleForm.name)
          updateUser(this.ruleForm).then((response) => {
            if (response.code === 200) {
              this.$alert(this.ruleForm.username + '用户信息已更新!!', 'OK', {
                confirmButtonText: '确定',
                callback: action => {
                  this.$router.push('/user/ManageUser')
                }
              })
            }
          })
        } else {
          console.log('校验失败!')
          return false
        }
      })
    },
    // 表单置空
    resetForm(formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>

<style scoped>

</style>
