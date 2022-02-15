<template>
  <div class="block">
    <el-timeline>
      <el-timeline-item v-for="(item,index) of timeline" :key="index" :timestamp="item.timestamp" placement="top">
        <el-card>
          <h4>{{ item.title }}</h4>
          <p>{{ item.content }}</p>
        </el-card>
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 时间线的数据
      timeline: [
        {
          timestamp: '2019/4/20',
          title: '测试1',
          content: '测试1,测试1,测试1,测试1'
        },
        {
          timestamp: '2019/4/21',
          title: '测试2',
          content: '测试2,测试2,测试2,测试2,测试2'
        },
        {
          timestamp: '2019/4/22',
          title: '测试3',
          content: '测试3,测试3,测试3,测试3,测试3,测试3'
        },
        {
          timestamp: '2019/4/23',
          title: '测试4',
          content: '测试4,测试4,测试4,测试4,测试4,测试4'
        }
      ]
    }
  }
}
</script>
