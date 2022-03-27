<template>
  <el-dialog :visible.sync="dialogVisible" :title="curId ? '编辑评论' : '新增评论列表'" width="700px" :before-close="close">
    <el-form ref="ruleForm" label-position="left  " :model="ruleForm" status-icon :rules="rules" label-width="100px" class="demo-ruleForm">
      <el-form-item label="发表时间">
        <el-input v-model="ruleForm.timestamp" readonly />
      </el-form-item>

      <el-form-item label="评论ID" readonly>
        <el-input v-model="ruleForm.id" readonly />
      </el-form-item>

      <el-form-item label="作者名" prop="author" readonly>
        <el-input v-model="ruleForm.author" readonly />
      </el-form-item>

      <el-form-item label="审核" prop="reviewed">
        <el-radio v-model="ruleForm.reviewed" :label="1">通过</el-radio>
        <el-radio v-model="ruleForm.reviewed" :label="0">未通过</el-radio>
      </el-form-item>
      <el-form-item label="举报次数" prop="flag" readonly>
        <el-input v-model="ruleForm.flag" readonly />
      </el-form-item>

      <el-form-item label="评论内容" prop="body">
        <el-input v-model="ruleForm.body" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
        <el-button @click="resetForm('ruleForm')">重置</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>
<script>
import { getById, addComment, updateComment } from '@/api/comment'
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
        timestamp: '',
        author: '',
        reviewed: '',
        flag: '',
        body: ''
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
            updateComment(this.curId, this.ruleForm).then(res => {
              this.$message({
                message: '修改成功',
                type: 'success'
              })
              this.search()
            })
          } else {
            addComment(this.ruleForm).then(res => {
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
