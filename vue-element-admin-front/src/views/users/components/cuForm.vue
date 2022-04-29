<template>
  <el-dialog :visible.sync="dialogVisible" :title="curId ? '编辑用户名单' : '新增用户名单'" width="700px" :before-close="close">
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

      <el-form-item label="邮箱" prop="email">
        <el-input v-model="ruleForm.email" />
      </el-form-item>

      <el-form-item label="登录密码" readonly>
        <el-input v-model="ruleForm.rsa_password" readonly />
      </el-form-item>

      <el-form-item label="角色" prop="roles">

        <el-select v-model="ruleForm.role" placeholder="选择角色">
          <el-option
            v-for="item in rolesData"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="激活状态" prop="active">
        <el-radio v-model="ruleForm.active" :label="1">已激活</el-radio>
        <el-radio v-model="ruleForm.active" :label="0">未激活</el-radio>
      </el-form-item>

      <el-form-item label="确认状态" prop="confirmed">
        <el-radio v-model="ruleForm.confirmed" :label="1">已确认</el-radio>
        <el-radio v-model="ruleForm.confirmed" :label="0">未确认</el-radio>
      </el-form-item>

      <el-form-item label="收藏通知" prop="receive_collect_notification">
        <el-radio v-model="ruleForm.receive_collect_notification" :label="1">接收</el-radio>
        <el-radio v-model="ruleForm.receive_collect_notification" :label="0">未接收</el-radio>
      </el-form-item>

      <el-form-item label="评论通知" prop="receive_comment_notification">
        <el-radio v-model="ruleForm.receive_comment_notification" :label="1">接收</el-radio>
        <el-radio v-model="ruleForm.receive_comment_notification" :label="0">未接收</el-radio>
      </el-form-item>

      <el-form-item label="关注通知" prop="receive_follow_notification">
        <el-radio v-model="ruleForm.receive_follow_notification" :label="1">接收</el-radio>
        <el-radio v-model="ruleForm.receive_follow_notification" :label="0">未接收</el-radio>
      </el-form-item>

      <el-form-item label="收藏隐私" prop="public_collections">
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
import { getById, addUser, updateUser } from '@/api/user'
import { getRoles } from '@/api/roles'
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
        active: '',
        confirmed: '',
        locked: '',
        website: '',
        receive_collect_notification: '',
        receive_comment_notification: '',
        receive_follow_notification: '',
        public_collections: '',
        roles_list: '',
        role: ''
      },
      rolesData: [],
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
        this.getRoles()
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
            console.log(this.ruleForm)
            updateUser(this.curId, this.ruleForm).then(res => {
              this.$message({
                message: '修改成功',
                type: 'success'
              })
              this.search()
            })
          } else {
            addUser(this.ruleForm).then(res => {
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
    getRoles() {
      // 获取角色列表
      getRoles().then(res => {
        this.rolesData = res.data.results
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>
