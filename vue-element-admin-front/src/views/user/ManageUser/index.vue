<template>
  <div style="margin:20px 60px 5px 40px">
    <el-table
      :data="ruleForm"
      style="width: 100%"
      :default-sort="{prop: 'register_time', order: 'aescending'}"
    >
      <el-table-column
        label="注册日期"
        width="180"
        prop="register_time"
        sortable
      >
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span style="margin-left: 10px">{{ scope.row.register_time }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="用户ID"
        width="80"
        prop="id"
      >
        <template slot-scope="scope">
          <span style="margin-left: 10px">{{ scope.row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="登录名"
        width="80"
        prop="username"
      >
        <template slot-scope="scope">
          <el-popover trigger="hover" placement="top">
            <p>姓名: {{ scope.row.name }}</p>
            <p>邮箱: {{ scope.row.email }}</p>
            <p>密文: {{ scope.row.rsa_password_hash }}</p>
            <div slot="reference" class="name-wrapper">
              <el-tag size="medium">{{ scope.row.username }}</el-tag>
            </div>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column
        label="级别"
        width="80"
        prop="auth"
      />
      <el-table-column
        label="激活状态"
        width="80"
        prop="active"
        :formatter="formatter1"
      />
      <el-table-column
        label="确认状态"
        width="80"
        prop="confirmed"
        :formatter="formatter2"
      />
      <el-table-column
        label="锁定状态"
        width="80"
        prop="locked"
        :formatter="formatter3"
      />
      <el-table-column
        label="身份信息"
        width="80"
        prop="role_id"
        :formatter="formatter4"
      />
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="editUser(scope.row)"
          >编辑
          </el-button>
          <el-button
            size="mini"
            type="danger"
            @click="open(scope.row)"
          >删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      :current-page="currentPage"
      :page-sizes="[2, 3, 4, 5]"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script>
import { getUsers, deleteUser } from '@/api/user'

export default {
  data() {
    // 更新信息的表单验证
    const checkAge = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('年龄不能为空'))
      }
      setTimeout(() => {
        if (!Number.isInteger(value)) {
          callback(new Error('请输入数字值'))
        } else {
          if (value < 18) {
            callback(new Error('必须年满18岁'))
          } else {
            callback()
          }
        }
      }, 1000)
    }
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
    return {
      // 表单验证
      rules: {
        password: [
          { validator: validatePass, trigger: 'blur' }
        ],
        checkPass: [
          { validator: validatePass2, trigger: 'blur' }
        ],
        age: [
          { validator: checkAge, trigger: 'blur' }
        ]
      },
      // 分页参数
      currentPage: 1,
      pagesize: 2,
      total: 4,
      // 展示更新按钮
      dialogFormVisible: false,
      formLabelWidth: '120px',
      ruleForm: null
      // 表单验证
    }
  },
  created() {
    getUsers(this.currentPage, this.pagesize).then((response) => {
      //
      if (response.code === 200) {
        this.ruleForm = response.data
        this.total = response.total
      }
    })
  },
  methods: {
    // 确认框弹出 表单处理
    // 激活格式化
    formatter1(row) {
      return row.active ? '已激活' : '未激活'
    },
    // 确认格式化
    formatter2(row) {
      return row.confirmed ? '已确认' : '未确认'
    },
    // 锁定格式化
    formatter3(row) {
      return row.locked ? '已锁定' : '未锁定'
    },
    // 身份信息格式化
    formatter4(row) {
      return row.role_id === 1 ? '锁定用户'
        : (row.role_id === 2 ? '普通用户'
          : (row.role_id === 3 ? '协管员' : '管理员'))
    },
    // 分页处理,改变size触发的事件
    handleSizeChange(size) {
      this.pagesize = size // 获取当前选择的页的大小
      this.currentPage = 1
      this.pagelist()
    },
    // 请求函数
    pagelist() {
      getUsers(this.currentPage, this.pagesize).then((response) => {
        if (response.code === 200) {
          this.ruleForm = response.data
          this.total = response.total
        }
      })
    },
    // 改变页数的函数
    handleCurrentChange(page) {
      this.currentPage = page // 获取当前页
      this.pagelist()
    },
    // 更新表单处理
    editUser(row) {
      // 传入路径与参数
      this.$router.push({
        path: '/user/UpdateUser',
        query: {
          id: row.id
        }
      })
    },
    // 删除用户
    open(row) {
      this.$confirm('此操作将永久删除该用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteUser(row.id).then((response) => {
          if (response.code === 200) {
            console.log(response)
          }
        })
        this.$notify({
          title: '成功',
          message: '删除成功',
          type: 'success'
        })
        // 传入路径
        this.$router.push('/user/UpdateUser')
      }).catch(() => {
        this.$notify.info({
          title: '消息',
          message: '取消删除'
        })
      })
    }
  }
}

</script>
