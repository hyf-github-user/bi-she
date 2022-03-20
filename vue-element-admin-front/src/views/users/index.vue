<template>
  <div class="app-container">
    <el-row>
      <el-col :span="17">
        <el-form ref="form" :model="form" inline>
          <el-form-item prop="search">
            <el-input
              v-model="form.search"
              clearable
              style="width:300px"
              prefix-icon="el-icon-search"
              placeholder="输入用户名(username)搜索"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="success" icon="el-icon-search" size="medium" @click="search(form)">搜索</el-button>
            <el-button type="warning" icon="el-icon-refresh-left" size="medium" @click="resetForm()">重置</el-button>
          </el-form-item>
        </el-form>
        <el-button
          v-permission="['admin']"
          type="primary"
          style="margin-bottom:20px"
          icon="el-icon-plus"
          size="medium"
        >新增(需到前台进行注册)
        </el-button>
        <el-button
          v-permission="['admin']"
          type="danger"
          icon="el-icon-delete"
          :disabled="!multipleSelection.length"
          size="medium"
          @click="deleteUsers(form)"
        >删除
        </el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>用户名单</span>
          </div>
          <el-table
            ref="multipleTable"
            :data="tableData"
            style="width: 100%"
            highlight-current-row
            :default-sort="{prop: 'register_time', order: 'aescending'}"
            @selection-change="handleSelectionChange"
          >
            <el-table-column
              type="selection"
            />
            <el-table-column
              label="注册日期"
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
              prop="id"
            >
              <template slot-scope="scope">
                <span style="margin-left: 10px">{{ scope.row.id }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="登录名"
              prop="username"
            >
              <template slot-scope="scope">
                <el-popover trigger="hover" placement="top">
                  <p>姓名: {{ scope.row.name }}</p>
                  <p>邮箱: {{ scope.row.email }}</p>
                  <p>RSA私钥: {{ scope.row.rsa_password }}</p>
                  <div slot="reference" class="name-wrapper">
                    <el-tag size="medium">{{ scope.row.username }}</el-tag>
                  </div>
                </el-popover>
              </template>
            </el-table-column>
            <el-table-column
              label="级别"
              prop="auth"
            />
            <el-table-column
              label="个人网站"
              prop="website"
            />
            <el-table-column
              label="激活状态"
              prop="active"
              :formatter="formatter1"
            />
            <el-table-column
              label="确认状态"
              prop="confirmed"
              :formatter="formatter2"
            />
            <el-table-column
              label="锁定状态"
              prop="locked"
              :formatter="formatter3"
            />
            <el-table-column
              label="身份信息"
              prop="role"
              :formatter="formatter4"
            />
            <el-table-column
              label="收藏通知"
              prop="receive_collect_notification"
              :formatter="formatter5"
            />
            <el-table-column
              label="评论通知"
              prop="receive_comment_notification"
              :formatter="formatter5"
            />
            <el-table-column
              label="关注通知"
              prop="receive_follow_notification"
              :formatter="formatter5"
            />
            <el-table-column
              label="收藏隐私"
              prop="public_collections"
              :formatter="formatter6"
            />

            <el-table-column
              fixed="right"
              align="center"
              label="操作"
              width="220"
            >
              <template slot-scope="{row}">
                <el-button
                  v-permission="['admin','editor']"
                  type="primary"
                  icon="el-icon-edit"
                  size="mini"
                  @click="updateUser(row)"
                >编辑
                </el-button>
                <el-button
                  v-permission="['admin']"
                  type="danger"
                  icon="el-icon-delete"
                  size="mini"
                  @click="deleteUser(row)"
                >删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <!--分页组件-->
          <el-pagination
            :current-page="1"
            :page-sizes="[2, 3, 4, 5]"
            :page-size="2"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </el-card>
      </el-col>
    </el-row>
    <!--    调用子组件进行编辑与增加操作-->
    <cuForm :dialog-visible="cuDialogVisible" :cur-id="curId" @close="close" @search="search" />
  </div>
</template>
<script>
import cuForm from './components/cuForm'
import { deleteUser, deleteUsers, getUsers } from '@/api/user'

export default {
  name: 'Roles',
  components: { cuForm },
  data() {
    return {
      form: {
        page: 1,
        size: 10,
        search: ''
      },
      tableData: [],
      total: 0,
      multipleSelection: [],
      // cuForm数据
      cuDialogVisible: false,
      curId: null
    }
  },
  created() {
    this.search()
  },
  methods: {
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
      return row.role === 1 ? '锁定用户'
        : (row.role === 2 ? '普通用户'
          : (row.role === 3 ? '协管员' : '管理员'))
    },
    // 格式化收藏通知
    formatter5(row) {
      return row.role === 1 ? '接收' : '未接收'
    },
    formatter6(row) {
      return row.role === 1 ? '公开' : '未公开'
    },
    // 获取角色列表/搜索功能
    search() {
      getUsers(this.form).then(res => {
        this.tableData = res.data.results
        this.total = res.data.count
      })
    },
    // 重置
    resetForm() {
      this.$refs.form.resetFields()
      this.search()
    },
    // table选择框功能的change事件
    handleSelectionChange() {
      // 获取要删除的多个用户ID
      const deleteIds = []
      this.$refs.multipleTable.selection.forEach(data => deleteIds.push(data.id))
      this.multipleSelection = deleteIds
    },
    // 删除User
    deleteUser(row) {
      this.$confirm('此操作将从用户单中移除该用户, 是否继续？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteUser(row.id).then(res => {
          this.$message({
            message: '删除成功',
            type: 'success'
          })
          // 刷新table
          this.search()
        })
      })
    },
    // 批量删除IP
    deleteUsers() {
      this.$confirm('此操作将从用户名单单中移除选中用户' + ', 是否继续？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteUsers(this.multipleSelection).then(res => {
          this.$message({
            message: '删除成功',
            type: 'success'
          })
          // 刷新table
          this.search()
        })
      })
    },
    // 获取当前的页面大小
    handleSizeChange(val) {
      this.form.size = val
      this.search()
    },
    // 获取当前的页数
    handleCurrentChange(val) {
      this.form.page = val
      this.search()
    },
    // 需要到前台进行注册
    createUser() {
      this.cuDialogVisible = true
    },
    // 获得编辑的子窗口
    updateUser(row) {
      // 调用当前更新用户的窗口,并获取当前用户的ID
      this.curId = row.id
      this.cuDialogVisible = true
    },
    // 关闭子窗口
    close() {
      this.cuDialogVisible = false
      this.curId = null
    }
  }
}
</script>
