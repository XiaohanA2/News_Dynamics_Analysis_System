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
    <el-table v-if="newsInfo.length" :data="newsInfo" style="margin-top: 30px;">
      <el-table-column prop="headline" label="新闻标题" min-width="200" />
      <el-table-column label="爆款概率" min-width="150">
        <template slot-scope="scope">
          <div>
            <el-tag :type="getBoomLevelType(scope.row.analysis.boom_probability.level)">
              {{ scope.row.analysis.boom_probability.level }}
            </el-tag>
            <div>得分：{{ scope.row.analysis.boom_probability.score }}</div>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="传播特征" min-width="200">
        <template slot-scope="scope">
          <el-collapse>
            <el-collapse-item>
              <template slot="title">
                <span>查看详情</span>
              </template>
              <div>
                <p><strong>浏览时长分析：</strong>{{ scope.row.analysis.spread_characteristics.duration_analysis }}</p>
                <p><strong>增长趋势分析：</strong>{{ scope.row.analysis.spread_characteristics.growth_analysis }}</p>
                <p><strong>用户参与度：</strong>{{ scope.row.analysis.spread_characteristics.user_engagement }}</p>
              </div>
            </el-collapse-item>
          </el-collapse>
        </template>
      </el-table-column>
      <el-table-column label="对比分析" min-width="200">
        <template slot-scope="scope">
          <el-collapse>
            <el-collapse-item>
              <template slot="title">
                <span>查看详情</span>
              </template>
              <div>
                <p><strong>优势：</strong></p>
                <ul>
                  <li v-for="(advantage, index) in scope.row.analysis.comparative_analysis.advantages" :key="'adv-'+index">
                    {{ advantage }}
                  </li>
                </ul>
                <p><strong>劣势：</strong></p>
                <ul>
                  <li v-for="(disadvantage, index) in scope.row.analysis.comparative_analysis.disadvantages" :key="'dis-'+index">
                    {{ disadvantage }}
                  </li>
                </ul>
              </div>
            </el-collapse-item>
          </el-collapse>
        </template>
      </el-table-column>
      <el-table-column label="改进建议" min-width="200">
        <template slot-scope="scope">
          <el-collapse>
            <el-collapse-item>
              <template slot="title">
                <span>查看详情</span>
              </template>
              <div v-for="(suggestion, index) in scope.row.analysis.improvement_suggestions" :key="index">
                <p><strong>{{ suggestion.aspect }}：</strong></p>
                <p>{{ suggestion.suggestion }}</p>
                <p><em>预期效果：{{ suggestion.expected_impact }}</em></p>
              </div>
            </el-collapse-item>
          </el-collapse>
        </template>
      </el-table-column>
      <el-table-column label="详细指标" min-width="150">
        <template slot-scope="scope">
          <el-popover
            placement="right"
            width="400"
            trigger="click">
            <div>
              <p><strong>总浏览用户数：</strong>{{ scope.row.metrics.total_users }}</p>
              <p><strong>总浏览时长：</strong>{{ scope.row.metrics.total_duration }}秒</p>
              <p><strong>每小时平均浏览时长：</strong>{{ scope.row.metrics.hourly_duration.toFixed(2) }}秒</p>
              <p><strong>浏览增长趋势：</strong>{{ scope.row.metrics.growth_trend.toFixed(2) }}</p>
              <p><strong>浏览时长相对平均值：</strong>{{ scope.row.metrics.duration_ratio.toFixed(2) }}倍</p>
              <p><strong>增长趋势相对平均值：</strong>{{ scope.row.metrics.growth_ratio.toFixed(2) }}倍</p>
            </div>
            <el-button slot="reference" size="small" type="text">查看指标</el-button>
          </el-popover>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { analyzeHotNews } from '@/api/news'
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
    getBoomLevelType(level) {
      const types = {
        '高': 'success',
        '中': 'warning',
        '低': 'danger'
      }
      return types[level] || 'info'
    },
    search(form) {
      const start_time = form.startDate
      const end_time = form.endDate
      const category = form.category
      const topic = form.topic

      if (!start_time || !end_time) {
        this.$message({
          message: '请选择起止时间',
          type: 'error'
        })
        return
      }
      if (new Date(start_time) > new Date(end_time)) {
        this.$message({
          message: '起始时间不能大于结束时间',
          type: 'error'
        })
        return
      }

      analyzeHotNews({
        category,
        topic,
        start_time,
        end_time
      })
        .then(res => {
          this.newsInfo = res.data
          this.$message({
            message: '分析完成！',
            type: 'success'
          })
        }).catch(err => {
          this.$message({
            message: '分析失败',
            type: 'error'
          })
          console.error(err)
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
.el-table {
  margin-top: 20px;
}
.el-collapse {
  border: none;
}
.el-collapse-item__header {
  border: none;
  padding: 0;
}
.el-collapse-item__content {
  padding: 10px 0;
}
</style>