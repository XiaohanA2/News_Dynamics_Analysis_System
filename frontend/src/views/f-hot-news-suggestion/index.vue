<template>
  <div class="app-container">
    <el-form
      ref="form"
      inline
      :model="form"
      style="display: flex; width: 100%"
    >
      <el-row style="display: flex; width: 100%">
        <el-form-item label="新闻种类">
          <el-select
            v-model="form.category"
            placeholder="请选择种类"
            :disabled="categoryList.length === 0"
            clearable
            @change="getTopicList(form.category)"
            @clear="clearTopicList"
          >
            <el-option
              v-for="category in categoryList"
              :key="category"
              :label="category"
              :value="category"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="新闻主题">
          <el-select
            v-model="form.topic"
            placeholder="请选择主题"
            :disabled="topicList.length === 0"
            clearable
          >
            <el-option
              v-for="topic in topicList"
              :key="topic"
              :label="topic"
              :value="topic"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="起始时间" style="display: inline-block !important;">
          <el-date-picker
            v-model="form.startDate"
            type="datetime"
            placeholder="选择日期"
            value-format="yyyy-MM-dd HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="结束时间">
          <el-date-picker
            v-model="form.endDate"
            type="datetime"
            placeholder="选择日期"
            value-format="yyyy-MM-dd HH:mm:ss"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            @click="search(form)"
          >查询</el-button>
        </el-form-item>
      </el-row>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      categoryList: [],
      topicList: [],
      form: {
        category: '',
        topic: '',
        startDate: null,
        endDate: null
      },
      newsInfo: []
    }
  },
  mounted() {
    this.$axios({
      method: 'get',
      url: 'category'
    }).then(res => {
      this.categoryList = res.data
    }).catch(err => {
      console.log(err)
    })
  },
  methods: {
    search(form) {
      console.log(form)
      const start_ts = form.startDate !== null ? Date.parse(new Date(form.startDate.replace(' ', 'T'))) / 1000 : ''
      const end_ts = form.endDate !== null ? Date.parse(new Date(form.endDate.replace(' ', 'T'))) / 1000 : ''
      const category = form.category === undefined ? '' : form.category
      const topic = form.topic === undefined ? '' : form.topic
      if (start_ts !== '' && end_ts !== '' && start_ts > end_ts) {
        this.$message({
          message: '起始时间不能大于结束时间',
          type: 'error'
        })
        return
      }
      this.$message({
        message: `爆款新闻待实现: ${category} ${topic} ${start_ts} ${end_ts}`,
        type: 'warning'
      })
    },
    getTopicList(category) {
      if (category === '') {
        this.topicList = []
        return
      }
      this.$axios({
        url: '/topic',
        params: {
          category: category
        },
        method: 'get'
      }).then(res => {
        console.log(res)
        this.topicList = res.data
        console.log(this.topicList)
      }).catch(err => {
        console.log(err)
      })
    },
    clearTopicList() {
      this.form.category = ''
      this.topicList = []
      this.form.topic = ''
    }
  }
}
</script>

<style scoped>
.el-form-item {
  margin-left: 10px;
  margin-right: 10px;
  flex-shrink: 0;
}
.el-col > .el-row {
  display: flex;
  width: 100%;
}
</style>

