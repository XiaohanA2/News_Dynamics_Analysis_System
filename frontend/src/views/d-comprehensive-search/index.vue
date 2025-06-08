<template>
  <div class="app-container">
    <el-form
      ref="form"
      inline
      :model="form"
      style="display: flex; width: 100%"
    >
      <el-col>
        <el-row>
          <el-form-item label="用户id">
            <el-input-number
              v-model="form.userId"
              :max="userIdRange.max"
              :min="userIdRange.min"
              controls-position="right"
            />
          </el-form-item>
          <el-form-item label="新闻标题长度">
            <el-input-number
              v-model="form.minHeadlineLength"
              :max="headlineLengthRange.max"
              :min="headlineLengthRange.min"
              controls-position="right"
            />
            <span style="margin-left: 10px; margin-right: 10px">至</span>
            <el-input-number
              v-model="form.maxHeadlineLength"
              :max="headlineLengthRange.max"
              :min="headlineLengthRange.min"
              controls-position="right"
            />
          </el-form-item>
          <el-form-item label="新闻内容长度">
            <el-input-number
              v-model="form.minContentLength"
              :max="contentLengthRange.max"
              :min="contentLengthRange.min"
              controls-position="right"
            />
            <span style="margin-left: 10px; margin-right: 10px">至</span>
            <el-input-number
              v-model="form.maxContentLength"
              :max="contentLengthRange.max"
              :min="contentLengthRange.min"
              controls-position="right"
            />
          </el-form-item>
        </el-row>
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
      </el-col>
    </el-form>

    <el-row v-if="newsInfo.length !== 0">
      <el-table :data="newsInfo" style="width: 100%" :default-sort="{ prop: 'news_id', order: 'ascending' }" stripe>
        <el-table-column prop="news_id" label="news_id" width="180" />
        <el-table-column prop="category" label="category" width="180" />
        <el-table-column prop="topic" label="topic" width="180" />
        <el-table-column prop="headline" label="headline" />
        <el-table-column fixed="right" label="Operations" width="120">
          <template #default="scope">
            <el-button
              link
              type="primary"
              size="small"
              @click.prevent="goNewsContent(scope.row)"
            >
              查看详细
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-row>
    <el-dialog :visible.sync="dialogVisible" align-center center draggable width="90%">
      <template slot="title">
        <span class="news-headline">{{ headline }}</span>
      </template>
      <span class="news-content">{{ content }}</span>
    </el-dialog>
  </div>
</template>

<script>
import request from '@/utils/request'

export default {
  data() {
    return {
      userIdRange: {
        min: 0,
        max: 0
      },
      headlineLengthRange: {
        min: 0,
        max: 0
      },
      contentLengthRange: {
        min: 0,
        max: 0
      },
      categoryList: [],
      topicList: [],
      form: {
        category: '',
        topic: '',
        userId: undefined,
        startDate: null,
        endDate: null,
        minHeadlineLength: undefined,
        maxHeadlineLength: undefined,
        minContentLength: undefined,
        maxContentLength: undefined
      },
      newsInfo: [],
      dialogVisible: false,
      headline: '',
      content: ''
    }
  },
  mounted() {
    request({
      method: 'get',
      url: '/category'
    }).then(res => {
      this.categoryList = res
    }).catch(err => {
      console.log(err)
    })
    
    request({
      url: '/range/userid',
      method: 'get'
    }).then(res => {
      this.userIdRange.min = res[0].min_user_id
      this.userIdRange.max = res[0].max_user_id
    }).catch(err => {
      console.log(err)
    })
    
    request({
      url: '/range/length',
      method: 'get'
    }).then(res => {
      this.headlineLengthRange.min = res[0].min_headline_length
      this.headlineLengthRange.max = res[0].max_headline_length
      this.contentLengthRange.min = res[0].min_content_length
      this.contentLengthRange.max = res[0].max_content_length
    }).catch(err => {
      console.log(err)
    })
  },
  methods: {
    search(form) {
      const start_ts = Math.floor(this.form.startDate.getTime() / 1000)
      const end_ts = Math.floor(this.form.endDate.getTime() / 1000)
      const userId = this.form.userId
      const category = this.form.category
      const topic = this.form.topic
      const minHeadlineLength = this.form.minHeadlineLength
      const maxHeadlineLength = this.form.maxHeadlineLength
      const minContentLength = this.form.minContentLength
      const maxContentLength = this.form.maxContentLength

      request({
        url: '/comprehensive',
        params: {
          start_ts: start_ts,
          end_ts: end_ts,
          min_user_id: userId,
          max_user_id: userId,
          category: category,
          topic: topic,
          min_headline_length: minHeadlineLength,
          max_headline_length: maxHeadlineLength,
          min_content_length: minContentLength,
          max_content_length: maxContentLength
        },
        method: 'get'
      }).then(res => {
        this.newsInfo = res
      }).catch(err => {
        console.log(err)
      })
    },
    goNewsContent(row) {
      request({
        url: '/news/content',
        params: {
          news_id: row.news_id
        },
        method: 'get'
      }).then(res => {
        this.headline = row.headline
        this.content = res.content
        this.dialogVisible = true
      }).catch(err => {
        console.log(err)
      })
    },
    getTopicList(category) {
      if (category === '') {
        this.topicList = []
        return
      }
      request({
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
.news-headline {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 15px;
}

.news-content {
  font-family: Arial, sans-serif;
  font-size: 16px;
  line-height: 1.6;
  color: #333;
  background-color: #fff;
}
</style>

