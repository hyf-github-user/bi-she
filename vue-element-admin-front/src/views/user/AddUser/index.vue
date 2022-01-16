<template>
  <div style="margin:30px 40px 5px 10px">
    <el-form ref="ruleForm" :model="ruleForm" :rules="rules" label-width="100px" class="demo-ruleForm">

      <el-form-item label="登录名" prop="username">
        <el-input v-model="ruleForm.username" />
      </el-form-item>

      <el-form-item label="用户名" prop="name">
        <el-input v-model="ruleForm.name" />
      </el-form-item>

      <el-form-item label="邮箱" prop="email">
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

      <el-form-item label="密码" prop="password">
        <el-input v-model="ruleForm.password" type="password" autocomplete="off" />
      </el-form-item>

      <el-form-item label="确认密码" prop="checkPass">
        <el-input v-model="ruleForm.checkPass" type="password" autocomplete="off" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">添加用户</el-button>
        <el-button @click="resetForm('ruleForm')">重置</el-button>
      </el-form-item>
    </el-form>
  </div>

</template>

<script>
import { addUser } from '@/api/user'

export default {
  data() {
    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (this.ruleForm.checkPass !== '') {
          this.$refs.ruleForm.validateField('checkPass')
        }
        callback()
      }
    }
    const validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.ruleForm.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    // 自定义的邮箱和手机验证规则
    const checkEmail = (rule, value, callback) => { // 验证邮箱
      const mailReg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/
      if (!value) {
        return callback(new Error('邮箱不能为空'))
      }
      setTimeout(() => {
        if (mailReg.test(value)) {
          callback()
        } else {
          callback(new Error('请输入正确的邮箱格式'))
        }
      }, 100)
    }
    return {
      ruleForm: {
        username: '',
        name: '',
        auth: '',
        active: '',
        confirmed: '',
        locked: '',
        role_id: '',
        password: '',
        checkPass: ''
      },
      rules: {
        pass: [
          { validator: validatePass, trigger: 'blur' }
        ],
        checkPass: [
          { validator: validatePass2, trigger: 'blur' }
        ],
        email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }, { validator: checkEmail, trigger: 'blur' }]
      }
    }
  },
  methods: {
    formatter(row) {
      return row.sex === '0' ? '男' : '女'
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => { // 校验表单数据
        if (valid) {
          console.log(this.ruleForm.name)
          addUser(this.ruleForm).then((response) => {
            if (response.code === 200) {
              this.$alert(this.ruleForm.username + '成功添加用户!!', 'OK', {
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
