<template>
  <div class="app-container">
    <el-row>
      <el-col :span="18">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>个人信息</span>
          </div>
          <div>
            <el-form ref="form" :rules="rules" :model="form" label-width="80px">
              <el-form-item label="姓名" prop="username">
                <el-input v-model="form.username" style="width: 40%" />
                <span style="color: #C0C0C0;margin-left: 10px;">登录账号</span>
              </el-form-item>
              <el-form-item label="手机号" prop="mobile">
                <el-input v-model="form.mobile" style="width: 40%" />
                <span style="color: #C0C0C0;margin-left: 10px;">手机号可用于登录使用</span>
              </el-form-item>
              <el-form-item label="邮箱" prop="email">
                <el-input v-model="form.email" style="width: 40%" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="onSubmit('form')">保存配置</el-button>
              </el-form-item>
            </el-form></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { changeInformation } from '@/api/information/centre'
import store from '@/store'
import { getToken } from '@/utils/auth'
import { validateEMail, validatePhone } from '@/utils/rulesValidate'
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      show: false,
      headers: {
        'Authorization': 'Bearer ' + getToken()
      },
      form: { },
      rules: {
        username: [
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        email: [
          { validator: validateEMail, trigger: 'blur' }
        ],
        mobile: [
          { validator: validatePhone, trigger: 'blur' }
        ]
      },
      updateAvatarApi: process.env.VUE_APP_BASE_API + '/information/change-avatar/'
    }
  },
  computed: {
    ...mapGetters([
      'username',
      'avatar',
      'mobile',
      'email'
    ])
  },
  created() {
    this.form = { username: this.username, mobile: this.mobile, email: this.email }
    // store.dispatch('user/getInfo').then(() => {})
    // console.log(this.form)
  },
  methods: {
    // 修改个人信息
    onSubmit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          //   if (this.form.mobile === '') {
          //     this.form.mobile = null
          //   }
          changeInformation(this.form).then(res => {
            this.$message({
              message: '修改成功',
              type: 'success'
            })
            store.dispatch('user/getInfo').then(() => {})
          })
        }
      })
    }
  }
}
</script>

