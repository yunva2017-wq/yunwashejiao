import api from './index'

// 用户注册
export const register = (data) => {
  return api.post('/register', data)
}

// 用户登录
export const login = (data) => {
  return api.post('/login', data)
}

// 获取用户信息
export const getUser = (userId) => {
  return api.get(`/users/${userId}`)
}

// 获取消息列表
export const getMessages = (roomId, limit = 50) => {
  return api.get(`/messages/${roomId}?limit=${limit}`)
}

// 上传语音
export const uploadVoice = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/upload-voice', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
