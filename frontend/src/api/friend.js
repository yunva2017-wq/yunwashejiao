import api from './index'

// 搜索用户
export const searchUsers = (query) => {
  return api.get(`/friends/search?q=${query}`)
}

// 获取好友列表
export const getFriends = () => {
  return api.get('/friends')
}

// 发送好友请求
export const sendFriendRequest = (addressee_username, remark) => {
  return api.post('/friends/requests', { addressee_username, remark })
}

// 获取好友请求列表
export const getFriendRequests = () => {
  return api.get('/friends/requests')
}

// 响应好友请求
export const respondFriendRequest = (requestId, accept) => {
  return api.post(`/friends/requests/${requestId}/respond?accept=${accept}`)
}

// 删除好友
export const deleteFriend = (friendId) => {
  return api.delete(`/friends/${friendId}`)
}

// 获取聊天室 ID
export const getChatRoom = (friendId) => {
  return api.get(`/friends/room/${friendId}`)
}
