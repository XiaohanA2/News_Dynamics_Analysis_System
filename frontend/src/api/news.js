import request from '@/utils/request'

export function mockGetSingleNewsFashion(start_ts, end_ts, news_id) {
  console.log(news_id, start_ts, end_ts)
  return request({
    url: '/news/fashion',
    method: 'get'
  })
}

export function mockGetCategoryNewsChanging(start_ts, end_ts, categorys) {
  console.log(categorys, start_ts, end_ts)
  return request({
    url: '/news/category',
    method: 'get'
  })
}

export function mockGetAllCategoryList() {
  return request({
    url: '/category',
    method: 'get'
  })
}

export function mockGetConprehensiveInfo(start_ts, end_ts, news_id, category, topic, min_headline_length, max_headline_length, min_content_length, max_content_length) {
  console.log('start_ts:', start_ts)
  console.log('end_ts:', end_ts)
  console.log('news_id:', news_id)
  console.log('category:', category)
  console.log('topic:', topic)
  console.log('min_headline_length:', min_headline_length)
  console.log('max_headline_length:', max_headline_length)
  console.log('min_content_length:', min_content_length)
  console.log('max_content_length:', max_content_length)
  return request({
    url: '/comprehensive',
    method: 'get'
  })
}

export function mockGetNewsHeadlineAndContentRange() {
  return request({
    url: '/range/length',
    method: 'get'
  })
}

export function mockGetNewsContent(news_id) {
  console.log(news_id)
  return request({
    url: '/news/content',
    method: 'get'
  })
}

export function mockGetTopicOfCategory(category) {
  console.log(category)
  return request({
    url: '/topic',
    method: 'get'
  })
}
/**
 * 爆款新闻分析
 * @param {Object} params - { category, topic, start_time, end_time }
 * @returns {Promise} 返回包含以下结构的数组：
 * [
 *   {
 *     news_id: string,
 *     headline: string,
 *     metrics: {
 *       total_users: number,
 *       total_duration: number,
 *       hourly_duration: number,
 *       growth_trend: number,
 *       duration_ratio: number,
 *       growth_ratio: number
 *     },
 *     analysis: {
 *       boom_probability: {
 *         score: string,
 *         level: string,
 *         reason: string
 *       },
 *       spread_characteristics: {
 *         duration_analysis: string,
 *         growth_analysis: string,
 *         user_engagement: string
 *       },
 *       comparative_analysis: {
 *         advantages: string[],
 *         disadvantages: string[]
 *       },
 *       improvement_suggestions: Array<{
 *         aspect: string,
 *         suggestion: string,
 *         expected_impact: string
 *       }>
 *     }
 *   }
 * ]
 */
export function analyzeHotNews(params) {
  return request({
    url: '/news/boom-analysis',
    method: 'post',
    data: params
  })
}

