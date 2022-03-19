<template>
  <el-card style="margin-bottom:90px;">
    <div slot="header" class="clearfix">
      <span>个人信息</span>
    </div>
    <div class="user-profile">
      <div class="box-center">
        <div class="el-upload">
          <img :src="avatar" title="点击上传头像" class="avatar" @click="toggleShow">
          <myUpload
            v-model="show"
            :headers="headers"
            :url="updateAvatarApi"
            method="PUT"
            field="image"
            @crop-upload-success="cropUploadSuccess"
          />
        </div>
      </div>
      <ul class="user-info">
        <li><div style="height: 100%"><svg-icon icon-class="login" /> 登录账号<div class="user-right">{{ username }}</div></div></li>
        <li><svg-icon icon-class="user1" /> 用户姓名 <div class="user-right">{{ name }}</div></li>
        <li><svg-icon icon-class="phone" /> 手机号码 <div class="user-right">{{ mobile }}</div></li>
        <li><svg-icon icon-class="email" /> 用户邮箱 <div class="user-right">{{ email }}</div></li>
        <li>
          <svg-icon icon-class="anq" /> 安全设置
          <div class="user-right">
            <a @click="$refs.pass.dialogVisible = true">修改密码</a>
          </div>
        </li>
      </ul>
      <div class="user-bio">
        <div class="user-education user-bio-section">
          <div class="user-bio-section-header"><svg-icon icon-class="education" /><span>Education</span></div>
          <div class="user-bio-section-body">
            <div class="text-muted">
              为中华之崛起而读书!
            </div>
          </div>
        </div>

        <div class="user-skills user-bio-section">
          <div class="user-bio-section-header"><svg-icon icon-class="skill" /><span>Skills</span></div>
          <div class="user-bio-section-body">
            <div class="progress-item">
              <span>Django</span>
              <el-progress :percentage="80" />
            </div>
            <div class="progress-item">
              <span>Vue</span>
              <el-progress :percentage="70" />
            </div>
            <div class="progress-item">
              <span>JavaScript</span>
              <el-progress :percentage="18" />
            </div>
            <div class="progress-item">
              <span>Css</span>
              <el-progress :percentage="12" />
            </div>
            <div class="progress-item">
              <span>ESLint</span>
              <el-progress :percentage="100" status="success" />
            </div>

          </div>
        </div>
      </div>
    </div>
    <updatePass ref="pass" />
  </el-card>
</template>

<script>
import updatePass from '../components/updatePass'
import myUpload from 'vue-image-crop-upload'
import { getToken } from '@/utils/auth'
import store from '@/store'
import { mapGetters } from 'vuex'
import { validateEMail, validatePhone } from '@/utils/rulesValidate'

export default {
  components: { myUpload, updatePass },
  data() {
    return {
      show: false,
      headers: {
        'Authorization': 'Bearer ' + getToken()
      },
      form: { name: this.name, mobile: this.mobile, email: this.email },
      rules: {
        name: [
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
      'name',
      'avatar',
      'mobile',
      'email'
    ])
  },
  methods: {
    toggleShow() {
      this.show = !this.show
    },
    // 头像上传成功的回调
    cropUploadSuccess() {
      store.dispatch('user/getInfo').then(() => {
      })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
}
.user-info {
  padding-left: 0;
  list-style: none;
  li{
    border-bottom: 1px solid #F0F3F4;
    padding: 11px 0;
    font-size: 13px;
  }
  .user-right {
    float: right;
    a{
      color: #317EF3;
    }
  }
}
.user-bio {
  margin-top: 20px;
  color: #606266;

  span {
    padding-left: 4px;
  }

  .user-bio-section {
    font-size: 14px;
    padding: 15px 0;

    .user-bio-section-header {
      border-bottom: 1px solid #dfe6ec;
      padding-bottom: 10px;
      margin-bottom: 10px;
      font-weight: bold;
    }
  }
}
</style>
