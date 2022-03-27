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
          @click="deleteComments(form)"
        >删除
        </el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>评论列表</span>
          </div>
          <el-table
            ref="multipleTable"
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
              label="发表日期"
              prop="timestamp"
              sortable
            >
              <template slot-scope="scope">
                <i class="el-icon-time" />
                <span style="margin-left: 10px">{{ scope.row.timestamp }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="评论ID"
              prop="id"
            >
              <template slot-scope="scope">
                <span style="margin-left: 10px">{{ scope.row.id }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="作者名"
              prop="author"
            >
              <template slot-scope="scope">
                <span style="margin-left: 10px">{{ scope.row.author }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="文章标题"
              prop="post"
            >
              <template slot-scope="scope">
                <span style="margin-left: 10px">{{ scope.row.post }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="评论内容"
              prop="body"
            >
              <template slot-scope="scope">
                <span style="margin-left: 10px">{{ scope.row.body }}</span>
              </template>
            </el-table-column>

            <el-table-column
              label="审核"
              prop="reviewed"
              :formatter="formatter"
            />
            <el-table-column
              label="举报次数"
              prop="flag"
            />
            <!--            <el-table-column-->
            <!--              label="回复评论"-->
            <!--              prop="replied"-->
            <!--            >-->
            <!--              <template v-show="scope.row.replied" slot-scope="scope">-->
            <!--                <el-popover trigger="hover" placement="top">-->
            <!--                  <p>回复的人: {{ scope.row.replied.author.username }}</p>-->
            <!--                  <p>回复的内容: {{ scope.row.replied.body }}</p>-->
            <!--                </el-popover>-->
            <!--              </template>-->
            <!--            </el-table-column>-->

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
                  @click="updateComment(row)"
                >编辑
                </el-button>
                <el-button
                  v-permission="['admin']"
                  type="danger"
                  icon="el-icon-delete"
                  size="mini"
                  @click="deleteComment(row)"
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
import { deleteComment, deleteComments, getComments } from '@/api/comment'

export default {
  name: 'Roles',
  components: { cuForm },
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
      return row.reviewed === 1 ? '通过' : '不通过'
    },
    // 获取角色列表/搜索功能
    search() {
      getComments(this.form).then(res => {
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
    deleteComment(row) {
      this.$confirm('此操作将从用户单中移除该用户, 是否继续？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteComment(row.id).then(res => {
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
    deleteComments() {
      this.$confirm('此操作将从用户名单单中移除选中用户' + ', 是否继续？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteComments(this.multipleSelection).then(res => {
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
    updateComment(row) {
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
