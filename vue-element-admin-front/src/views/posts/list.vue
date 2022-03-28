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
              placeholder="输入文章标题(title)搜索"
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
        >新增(需到前台)
        </el-button>
        <el-button
          v-permission="['admin']"
          type="danger"
          icon="el-icon-delete"
          :disabled="!multipleSelection.length"
          size="medium"
          @click="deletePosts(form)"
        >删除
        </el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>文章清单</span>
          </div>
          <el-table
            ref="multipleTable"
            v-loading="listLoading"
            :data="tableData"
            style="width: 100%"
            highlight-current-row
            :default-sort="{prop: 'timestamp', order: 'aescending'}"
            @selection-change="handleSelectionChange"
          >
            <el-table-column
              type="selection"
            />
            <el-table-column
              label="发布日期"
              prop="timestamp"
              sortable
            >
              <template slot-scope="scope">
                <i class="el-icon-time" />
                <span style="margin-left: 10px">{{ scope.row.timestamp }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="文章ID"
              prop="id"
            >
              <template slot-scope="scope">
                <span style="margin-left: 10px">{{ scope.row.id }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="作者名"
              prop="username"
            >
              <template slot-scope="scope">
                <el-popover trigger="hover" placement="top">
                  <p>姓名: {{ scope.row.author.name }}</p>
                  <p>邮箱: {{ scope.row.author.email }}</p>
                  <p>RSA私钥: {{ scope.row.author.rsa_password }}</p>
                  <div slot="reference" class="name-wrapper">
                    <el-tag size="medium">{{ scope.row.author.username }}</el-tag>
                  </div>
                </el-popover>
              </template>
            </el-table-column>
            <el-table-column width="100px" label="重要性">
              <template slot-scope="scope">
                <svg-icon v-for="n in +scope.row.importance" :key="n" icon-class="star" class="meta-item__icon" />
              </template>
            </el-table-column>
            <el-table-column class-name="status-col" label="状态" width="110">
              <template slot-scope="{row}">
                <el-tag :type="row.status | statusFilter">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="文章分类"
              prop="category"
            >
              <template slot-scope="scope">
                <span style="margin-left: 10px">{{ scope.row.category.name }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="举报次数"
              prop="flag"
            />
            <el-table-column
              label="评论功能"
              prop="can_comment"
              :formatter="formatter"
            />
            <el-table-column
              label="文章标题"
              prop="title"
            >
              <template slot-scope="{row}">
                <router-link :to="'/posts/edit/'+row.id" class="link-type">
                  <span>{{ row.title }}</span>
                </router-link>
              </template>
            </el-table-column>

            <el-table-column
              fixed="right"
              align="center"
              label="操作"
              width="220"
            >
              <template slot-scope="{row}">
                <router-link :to="'/posts/edit/'+row.id">
                  <el-button
                    v-permission="['admin','editor']"
                    type="primary"
                    icon="el-icon-edit"
                    size="mini"
                  >编辑
                  </el-button>
                </router-link>
                <el-button
                  v-permission="['admin']"
                  type="danger"
                  icon="el-icon-delete"
                  size="mini"
                  @click="deletePost(row)"
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
  </div>
</template>

<script>
import { getPosts, deletePosts, deletePost } from '@/api/post'

export default {
  name: 'ArticleList',
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      form: {
        page: 1,
        size: 2,
        search: ''
      },
      tableData: [],
      total: 0,
      multipleSelection: [],
      listLoading: true,
      // cuForm数据
      cuDialogVisible: false,
      curId: null
    }
  },
  created() {
    // 请求后端获取数据
    this.search()
  },
  methods: {
    formatter(row) {
      return row.can_comment === 1 ? '开启' : '关闭'
    },
    // 获取角色列表/搜索功能
    search() {
      this.listLoading = true
      getPosts(this.form).then(res => {
        this.tableData = res.data.results
        this.total = res.data.count
        this.listLoading = false
      })
    },
    // 重置
    resetForm() {
      this.$refs.form.resetFields()
      this.search()
    },
    // table选择框功能的change事件
    handleSelectionChange() {
      // 获取要删除的多个文章ID
      const deleteIds = []
      this.$refs.multipleTable.selection.forEach(data => deleteIds.push(data.id))
      this.multipleSelection = deleteIds
    },
    // 删除User
    deletePost(row) {
      this.$confirm('此操作将从文章列表中删除该文章, 是否继续？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deletePost(row.id).then(res => {
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
    deletePosts() {
      this.$confirm('此操作将从文章列表中移除选中文章' + ', 是否继续？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deletePosts(this.multipleSelection).then(res => {
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
      // 调用当前更新文章的窗口,并获取当前文章的ID
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

<style scoped>
.edit-input {
  padding-right: 100px;
}

.cancel-btn {
  position: absolute;
  right: 15px;
  top: 10px;
}
</style>
