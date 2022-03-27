<template>
  <el-dialog :visible.sync="dialogVisible" :title="curId ? '编辑评论' : '新增评论列表'" width="700px" :before-close="close">
    <el-form ref="ruleForm" label-position="left  " :model="ruleForm" status-icon :rules="rules" label-width="100px" class="demo-ruleForm">
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
      <el-form-item label="个人网站" prop="website">
        <el-input v-model="ruleForm.website" />
      </el-form-item>

      <el-form-item label="邮箱" prop="auth">
        <el-input v-model="ruleForm.email" />
      </el-form-item>

      <el-form-item label="登录密码" prop="rsa_password_hash">
        <el-input v-model="ruleForm.rsa_password" readonly />
      </el-form-item>

      <el-form-item label="身份信息" prop="role_id">
        <el-radio-group v-model="ruleForm.role">
          <el-radio :label="1">锁定用户</el-radio>
          <el-radio :label="2">普通用户</el-radio>
          <el-radio :label="3">协管员</el-radio>
          <el-radio :label="4">管理员</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="激活状态" prop="active">
        <el-radio v-model="ruleForm.active" :label="1">已激活</el-radio>
        <el-radio v-model="ruleForm.active" :label="0">未激活</el-radio>
      </el-form-item>

      <el-form-item label="确认状态" prop="confirmed">
        <el-radio v-model="ruleForm.confirmed" :label="1">已确认</el-radio>
        <el-radio v-model="ruleForm.confirmed" :label="0">未确认</el-radio>
      </el-form-item>

      <el-form-item label="锁定状态" prop="locked">
        <el-radio v-model="ruleForm.locked" :label="1">已锁定</el-radio>
        <el-radio v-model="ruleForm.locked" :label="0" :disabled="ruleForm.role==1">未锁定</el-radio>
      </el-form-item>

      <el-form-item label="收藏通知" prop="receive_collect_notification">
        <el-radio v-model="ruleForm.receive_collect_notification" :label="1">接收</el-radio>
        <el-radio v-model="ruleForm.receive_collect_notification" :label="0">未接收</el-radio>
      </el-form-item>

      <el-form-item label="评论通知" prop="confirmed">
        <el-radio v-model="ruleForm.receive_comment_notification" :label="1">接收</el-radio>
        <el-radio v-model="ruleForm.receive_comment_notification" :label="0">未接收</el-radio>
      </el-form-item>

      <el-form-item label="关注通知" prop="confirmed">
        <el-radio v-model="ruleForm.receive_follow_notification" :label="1">接收</el-radio>
        <el-radio v-model="ruleForm.receive_follow_notification" :label="0">未接收</el-radio>
      </el-form-item>

      <el-form-item label="收藏隐私" prop="confirmed">
        <el-radio v-model="ruleForm.public_collections" :label="1">公开</el-radio>
        <el-radio v-model="ruleForm.public_collections" :label="0">未公开</el-radio>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
        <el-button @click="resetForm('ruleForm')">重置</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>
<script>
import { getById, addRole, updateRole } from '@/api/roles'
export default {
  name: 'CuForm',
  props: {
    dialogVisible: {
      type: Boolean,
      default: false
    },
    curId: {
      type: Number,
      default: null
    }
  },

  data() {
    return {
      ruleForm: {
        id: '',
        register_time: '',
        username: '',
        name: '',
        rsa_password: '',
        email: '',
        role_id: '',
        active: '',
        confirmed: '',
        locked: '',
        website: '',
        receive_collect_notification: '',
        receive_comment_notification: '',
        receive_follow_notification: '',
        public_collections: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 1, max: 5, message: '长度在 1 到 5 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    dialogVisible(v) {
      if (v) {
        if (this.curId) {
          getById(this.curId).then(res => {
            this.ruleForm = res.data
          })
        }
      }
    }
  },
  methods: {
    close() {
      this.$refs.ruleForm.resetFields()
      this.$emit('close')
    },
    search() {
      this.close()
      this.$emit('search')
    },
    // 提交表单
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (this.curId) {
            if (!this.ruleForm.department) {
              this.ruleForm.department = null
            }
            updateRole(this.curId, this.ruleForm).then(res => {
              this.$message({
                message: '修改成功',
                type: 'success'
              })
              this.search()
            })
          } else {
            addRole(this.ruleForm).then(res => {
              this.$message({
                message: '新增成功',
                type: 'success'
              })
              this.search()
            })
          }
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>
