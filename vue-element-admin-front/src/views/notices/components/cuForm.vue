<template>
  <el-dialog :visible.sync="dialogVisible" :title="curId ? '编辑通知' : '新增通知'" width="700px" :before-close="close">
    <el-form ref="ruleForm" label-position="left  " :model="ruleForm" status-icon :rules="rules" label-width="100px" class="demo-ruleForm">
      <el-form-item v-show="curId" label="创建时间">
        <el-input v-model="ruleForm.timestamp" readonly />
      </el-form-item>

      <el-form-item v-show="curId" label="通知ID">
        <el-input v-model="ruleForm.id" readonly />
      </el-form-item>

      <el-form-item label="通知内容" prop="message">
        <el-input v-model="ruleForm.message" />
      </el-form-item>

      <el-form-item label="通知人" prop="roles">

        <el-select v-model="ruleForm.receiver" placeholder="选择角色">
          <el-option
            v-for="item in rolesData"
            :key="item.id"
            :label="item.username"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
        <el-button @click="resetForm('ruleForm')">重置</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>
<script>
import { getById, addNotification, updateNotification } from '@/api/notice'
import { getUsers } from '@/api/user'
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
        name: '',
        url: ''
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
        this.getUsers()
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
            updateNotification(this.curId, this.ruleForm).then(res => {
              this.$message({
                message: '修改成功',
                type: 'success'
              })
              this.search()
            })
          } else {
            addNotification(this.ruleForm).then(res => {
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
    // 获取用户
    getUsers() {
      // 获取角色列表
      getUsers().then(res => {
        this.rolesData = res.data.results
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>
