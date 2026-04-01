<template>
  <div class="chat-container">
    <!-- 聊天主界面 -->
    <div class="chat-main">
      <!-- 侧边栏 -->
      <div class="sidebar">
        <div class="user-info">
          <el-avatar :size="40" :src="currentUser?.avatar">{{ currentUser?.username?.[0]?.toUpperCase() }}</el-avatar>
          <div class="user-details">
            <span class="nickname">{{ currentUser?.nickname || currentUser?.username }}</span>
          </div>
          <el-button link @click="handleLogout" class="logout-btn">退出</el-button>
        </div>

        <!-- 搜索好友 -->
        <div class="search-friend">
          <el-input
            v-model="searchQuery"
            placeholder="搜索用户..."
            prefix-icon="Search"
            clearable
            @input="handleSearch"
          />
        </div>

        <!-- 好友请求 -->
        <div class="friend-requests" v-if="friendRequests.length > 0">
          <el-badge :value="friendRequests.length" :max="99" class="badge-title">
            <h3 @click="showRequestsDialog = true" style="cursor: pointer">好友请求</h3>
          </el-badge>
        </div>

        <!-- 好友列表 -->
        <div class="friend-list">
          <h3>我的好友 ({{ friends.length }})</h3>
          <div
            v-for="friend in friends"
            :key="friend.user_id"
            :class="['friend-item', { active: currentRoom?.startsWith('private_') && currentRoom?.includes(friend.user_id.toString()) }]"
            @click="joinPrivateChat(friend)"
          >
            <el-avatar :size="36" :src="friend.avatar" class="friend-avatar">{{ friend.username?.[0]?.toUpperCase() }}</el-avatar>
            <div class="friend-info">
              <span class="friend-name">{{ friend.remark || friend.nickname || friend.username }}</span>
              <span class="friend-username">{{ friend.username }}</span>
            </div>
            <el-button link class="more-btn" @click.stop="showFriendMenu(friend)">⋮</el-button>
          </div>
        </div>

        <!-- 搜索结果 -->
        <div class="search-results" v-if="searchResults.length > 0 && !isSearchedFriends">
          <h3>搜索结果</h3>
          <div
            v-for="user in searchResults"
            :key="user.id"
            class="search-result-item"
          >
            <el-avatar :size="36" :src="user.avatar" class="result-avatar">{{ user.username?.[0]?.toUpperCase() }}</el-avatar>
            <div class="result-info">
              <span class="result-name">{{ user.nickname || user.username }}</span>
              <span class="result-username">{{ user.username }}</span>
            </div>
            <el-button
              v-if="user.id !== currentUser?.id"
              type="primary"
              size="small"
              @click="sendFriendRequest(user)"
              :loading="sendingRequest === user.id"
            >
              加好友
            </el-button>
          </div>
        </div>

        <!-- 公共聊天室 -->
        <div class="room-list">
          <h3>公共聊天室</h3>
          <div
            v-for="room in rooms"
            :key="room.id"
            :class="['room-item', { active: currentRoom === room.id }]"
            @click="joinRoom(room.id)"
          >
            <span class="room-icon">💬</span>
            <span class="room-name">{{ room.name }}</span>
          </div>
        </div>
      </div>

      <!-- 聊天区域 -->
      <div class="chat-area">
        <div class="chat-header">
          <h2>{{ currentRoomName }}</h2>
        </div>

        <div class="messages-container" ref="messagesContainer">
          <div
            v-for="message in messages"
            :key="message.id"
            :class="['message', message.sender_username === currentUser?.username ? 'own' : 'other']"
          >
            <div class="message-avatar">
              {{ message.sender_username[0]?.toUpperCase() }}
            </div>
            <div class="message-content">
              <div class="message-sender">{{ message.sender_username }}</div>
              <div class="message-bubble">
                <!-- 文字消息 -->
                <template v-if="message.message_type === 'text'">
                  {{ message.content }}
                </template>
                <!-- 语音消息 -->
                <template v-else-if="message.message_type === 'voice'">
                  <audio :src="message.content" controls></audio>
                </template>
              </div>
              <div class="message-time">{{ formatTime(message.created_at) }}</div>
            </div>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="input-area">
          <el-button
            :icon="VoiceIcon"
            circle
            :type="isRecording ? 'danger' : 'default'"
            @click="toggleRecording"
            :loading="isRecording"
          />
          <el-input
            v-model="inputMessage"
            placeholder="输入消息... (Enter 发送)"
            @keyup.enter="sendMessage"
            :disabled="isRecording"
          />
          <el-button type="primary" @click="sendMessage" :disabled="!inputMessage.trim()">发送</el-button>
        </div>
      </div>
    </div>

    <!-- 语音通话弹窗 -->
    <el-dialog
      v-model="callDialogVisible"
      :title="callType === 'incoming' ? '来电' : '语音通话'"
      width="350px"
      :close-on-click-modal="false"
      :show-close="false"
    >
      <div class="call-content">
        <div class="call-avatar">
          <el-avatar :size="80">{{ callTarget?.[0]?.toUpperCase() }}</el-avatar>
          <h3>{{ callTarget }}</h3>
        </div>
        <div class="call-status">{{ callStatusText }}</div>

        <!-- 通话控制按钮 -->
        <div class="call-controls" v-if="isCallConnected">
          <el-button type="success" circle @click="toggleMute">
            {{ isMuted ? '取消静音' : '静音' }}
          </el-button>
          <el-button type="danger" circle @click="endCall">挂断</el-button>
        </div>

        <!-- 接听/拒绝按钮 -->
        <div class="call-actions" v-else-if="callType === 'incoming'">
          <el-button type="success" size="large" @click="acceptCall">接听</el-button>
          <el-button type="danger" size="large" @click="rejectCall">拒绝</el-button>
        </div>

        <!-- 等待接通 -->
        <div class="call-waiting" v-else-if="callType === 'outgoing' && !isCallConnected">
          <el-button type="danger" size="large" @click="cancelCall">取消</el-button>
        </div>
      </div>
    </el-dialog>

    <!-- 好友请求列表弹窗 -->
    <el-dialog v-model="showRequestsDialog" title="好友请求" width="400px">
      <div class="requests-list">
        <div v-for="req in friendRequests" :key="req.id" class="request-item">
          <div class="request-info">
            <span class="request-user">用户 ID: {{ req.requester_id }}</span>
            <span class="request-time">{{ formatRequestTime(req.created_at) }}</span>
          </div>
          <div class="request-actions">
            <el-button type="success" size="small" @click="handleFriendRequest(req.id, true)">接受</el-button>
            <el-button type="danger" size="small" @click="handleFriendRequest(req.id, false)">拒绝</el-button>
          </div>
        </div>
      </div>
    </el-dialog>

    <!-- 好友菜单弹窗 -->
    <el-dialog v-model="showFriendMenuDialog" title="好友选项" width="300px">
      <div class="friend-menu">
        <el-button type="danger" plain style="width: 100%" @click="handleDeleteFriend">删除好友</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, computed, nextTick, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Microphone, Search } from '@element-plus/icons-vue'
import { io } from 'socket.io-client'
import { getMessages, uploadVoice } from '@/api/user'
import config from '@/config.js'
import {
  searchUsers,
  getFriends,
  sendFriendRequest as apiSendFriendRequest,
  getFriendRequests,
  respondFriendRequest,
  deleteFriend as apiDeleteFriend,
  getChatRoom
} from '@/api/friend'

const VoiceIcon = Microphone

// 当前用户
const currentUser = computed(() => {
  const user = localStorage.getItem('user')
  return user ? JSON.parse(user) : null
})

const token = localStorage.getItem('token')

// Socket 连接
let socket = null

// 搜索相关
const searchQuery = ref('')
const searchResults = ref([])
const sendingRequest = ref(null)
const isSearchedFriends = ref(false)

// 好友相关
const friends = ref([])
const friendRequests = ref([])
const showRequestsDialog = ref(false)
const showFriendMenuDialog = ref(false)
const selectedFriend = ref(null)

// 房间列表
const rooms = [
  { id: 'general', name: '公共聊天室' },
  { id: 'random', name: '随机匹配' }
]
const currentRoom = ref(null)
const currentRoomName = computed(() => {
  if (currentRoom.value?.startsWith('private_')) {
    const friend = friends.value.find(f => {
      const user_ids = currentRoom.value.replace('private_', '').split('_').map(Number)
      return f.user_id === user_ids.find(id => id !== currentUser.value?.id)
    })
    return friend ? `@${friend.remark || friend.nickname || friend.username}` : '私聊'
  }
  return rooms.find(r => r.id === currentRoom.value)?.name || '聊天室'
})

// 消息
const messages = ref([])
const inputMessage = ref('')
const messagesContainer = ref(null)

// 在线用户
const onlineUsers = ref([])

// 录音状态
const isRecording = ref(false)
let mediaRecorder = null
let audioChunks = []

// 通话状态
const callDialogVisible = ref(false)
const callTarget = ref(null)
const callType = ref('outgoing') // incoming, outgoing
const isCallConnected = ref(false)
const isMuted = ref(false)
const callStatusText = ref('正在呼叫...')

// WebRTC
let peerConnection = null
let localStream = null

const STUN_SERVERS = {
  iceServers: [
    { urls: 'stun:stun.l.google.com:19302' },
    { urls: 'stun:stun1.l.google.com:19302' }
  ]
}

// 初始化 Socket 连接
const initSocket = () => {
  socket = io(config.socketUrl, {
    auth: { token }
  })

  // 连接成功
  socket.on('connect', () => {
    console.log('Socket connected')
    joinRoom(currentRoom.value)
  })

  // 收到新消息
  socket.on('new_message', (message) => {
    messages.value.push(message)
    scrollToBottom()
  })

  // 用户上线
  socket.on('user_online', ({ username }) => {
    if (!onlineUsers.value.includes(username)) {
      onlineUsers.value.push(username)
    }
  })

  // 用户下线
  socket.on('user_offline', ({ username }) => {
    onlineUsers.value = onlineUsers.value.filter(u => u !== username)
  })

  // 加入成功
  socket.on('joined', ({ room_id, username }) => {
    console.log(`Joined room: ${room_id}`)
    loadMessages(room_id)
  })

  // 来电
  socket.on('incoming_call', async (data) => {
    callTarget.value = data.caller
    callType.value = 'incoming'
    callDialogVisible.value = true
    callStatusText.value = `${data.caller} 正在呼叫您...`

    // 保存呼叫者信息
    window.incomingCallData = data
  })

  // 通话被接受
  socket.on('call_accepted', async (data) => {
    isCallConnected.value = true
    callStatusText.value = '通话中...'
    // 创建 WebRTC offer
    await createOffer()
  })

  // 通话被拒绝
  socket.on('call_rejected', () => {
    ElMessage.info('对方拒绝了通话')
    closeCallDialog()
  })

  // 通话结束
  socket.on('call_ended', () => {
    ElMessage.info('通话已结束')
    closeCallDialog()
  })

  // WebRTC Offer
  socket.on('webrtc_offer', async (data) => {
    await handleOffer(data.offer)
  })

  // WebRTC Answer
  socket.on('webrtc_answer', async (data) => {
    await handleAnswer(data.answer)
  })

  // ICE Candidate
  socket.on('ice_candidate', async (data) => {
    if (peerConnection && data.candidate) {
      await peerConnection.addIceCandidate(new RTCIceCandidate(data.candidate))
    }
  })

  // 错误
  socket.on('error', (data) => {
    ElMessage.error(data.message)
  })
}

// 加入房间
const joinRoom = (roomId) => {
  currentRoom.value = roomId
  if (socket) {
    socket.emit('join', {
      username: currentUser.value.username,
      room_id: roomId,
      token
    })
  }
  onlineUsers.value = []
}

// 加入公共聊天室
const joinPublicRoom = (roomId) => {
  isSearchedFriends.value = true
  searchResults.value = []
  joinRoom(roomId)
}

// 加载消息
const loadMessages = async (roomId) => {
  try {
    messages.value = await getMessages(roomId)
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('加载消息失败:', error)
  }
}

// 发送消息
const sendMessage = () => {
  if (!inputMessage.value.trim()) return

  const message = {
    room_id: currentRoom.value,
    sender_id: currentUser.value.id,
    sender_username: currentUser.value.username,
    message_type: 'text',
    content: inputMessage.value
  }

  socket.emit('chat_message', {
    room_id: currentRoom.value,
    message
  })

  // 添加到自己消息列表
  messages.value.push({
    ...message,
    id: Date.now(),
    created_at: new Date().toISOString()
  })

  inputMessage.value = ''
  scrollToBottom()
}

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 格式化时间
const formatTime = (timeStr) => {
  const date = new Date(timeStr)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

// 退出登录
const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    window.location.href = '/login'
  })
}

// ==================== 语音消息功能 ====================

// 切换录音状态
const toggleRecording = async () => {
  if (isRecording.value) {
    stopRecording()
  } else {
    await startRecording()
  }
}

// 开始录音
const startRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []

    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data)
    }

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
      await sendVoiceMessage(audioBlob)
      stream.getTracks().forEach(track => track.stop())
    }

    mediaRecorder.start()
    isRecording.value = true
    ElMessage.info('录音中...再次点击发送')
  } catch (error) {
    ElMessage.error('无法访问麦克风')
    console.error(error)
  }
}

// 停止录音
const stopRecording = () => {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop()
  }
  isRecording.value = false
}

// 发送语音消息
const sendVoiceMessage = async (audioBlob) => {
  const formData = new FormData()
  formData.append('file', audioBlob, 'voice.webm')

  try {
    const result = await uploadVoice(formData)
    const voiceMessage = {
      room_id: currentRoom.value,
      sender_id: currentUser.value.id,
      sender_username: currentUser.value.username,
      message_type: 'voice',
      content: result.url,
      created_at: new Date().toISOString()
    }

    socket.emit('chat_message', {
      room_id: currentRoom.value,
      message: voiceMessage
    })

    messages.value.push({
      ...voiceMessage,
      id: Date.now()
    })

    ElMessage.success('语音消息已发送')
  } catch (error) {
    ElMessage.error('发送语音失败')
  }
}

// ==================== WebRTC 语音通话 ====================

// 发起语音通话
const startVoiceCall = (targetUser) => {
  if (targetUser === currentUser.value.username) return

  callTarget.value = targetUser
  callType.value = 'outgoing'
  callDialogVisible.value = true
  callStatusText.value = '正在呼叫...'

  // 获取本地音频流
  getLocalStream().then(() => {
    // 发送呼叫请求
    socket.emit('voice_call', {
      target_id: targetUser,
      caller: currentUser.value.username,
      room_id: currentRoom.value
    })
  })
}

// 获取本地音频流
const getLocalStream = async () => {
  try {
    localStream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false })
    return localStream
  } catch (error) {
    ElMessage.error('无法访问麦克风')
    throw error
  }
}

// 创建 Offer
const createOffer = async () => {
  const stream = await getLocalStream()

  peerConnection = new RTCPeerConnection(STUN_SERVERS)

  // 添加本地流
  stream.getTracks().forEach(track => {
    peerConnection.addTrack(track, stream)
  })

  // 监听 ICE candidate
  peerConnection.onicecandidate = (event) => {
    if (event.candidate) {
      socket.emit('ice_candidate', {
        target_id: callTarget.value,
        candidate: event.candidate,
        caller: currentUser.value.username
      })
    }
  }

  // 监听远程流
  peerConnection.ontrack = (event) => {
    // 远程音频播放
    const audio = new Audio()
    audio.srcObject = event.streams[0]
    audio.autoplay = true
  }

  // 创建 Offer
  const offer = await peerConnection.createOffer()
  await peerConnection.setLocalDescription(offer)

  // 发送 Offer
  socket.emit('webrtc_offer', {
    target_id: callTarget.value,
    offer: peerConnection.localDescription,
    caller: currentUser.value.username
  })
}

// 处理 Offer
const handleOffer = async (offer) => {
  const stream = await getLocalStream()

  peerConnection = new RTCPeerConnection(STUN_SERVERS)

  stream.getTracks().forEach(track => {
    peerConnection.addTrack(track, stream)
  })

  peerConnection.onicecandidate = (event) => {
    if (event.candidate) {
      socket.emit('ice_candidate', {
        target_id: window.incomingCallData.caller,
        candidate: event.candidate,
        caller: currentUser.value.username
      })
    }
  }

  peerConnection.ontrack = (event) => {
    const audio = new Audio()
    audio.srcObject = event.streams[0]
    audio.autoplay = true
  }

  await peerConnection.setRemoteDescription(new RTCSessionDescription(offer))

  const answer = await peerConnection.createAnswer()
  await peerConnection.setLocalDescription(answer)

  // 发送 Answer
  socket.emit('webrtc_answer', {
    target_id: window.incomingCallData.caller,
    answer: peerConnection.localDescription,
    caller: currentUser.value.username
  })

  isCallConnected.value = true
  callStatusText.value = '通话中...'
}

// 处理 Answer
const handleAnswer = async (answer) => {
  if (peerConnection) {
    await peerConnection.setRemoteDescription(new RTCSessionDescription(answer))
  }
}

// 接听来电
const acceptCall = () => {
  socket.emit('call_accept', {
    caller_id: window.incomingCallData.caller,
    accepted_by: currentUser.value.username
  })
}

// 拒绝来电
const rejectCall = () => {
  socket.emit('call_reject', {
    caller_id: window.incomingCallData.caller
  })
  closeCallDialog()
}

// 取消呼叫
const cancelCall = () => {
  socket.emit('call_end', {
    target_id: callTarget.value
  })
  closeCallDialog()
}

// 结束通话
const endCall = () => {
  socket.emit('call_end', {
    target_id: callTarget.value
  })

  if (peerConnection) {
    peerConnection.close()
    peerConnection = null
  }

  if (localStream) {
    localStream.getTracks().forEach(track => track.stop())
    localStream = null
  }

  closeCallDialog()
}

// 切换静音
const toggleMute = () => {
  if (localStream) {
    localStream.getAudioTracks().forEach(track => {
      track.enabled = !track.enabled
    })
    isMuted.value = !isMuted.value
  }
}

// 关闭通话弹窗
const closeCallDialog = () => {
  callDialogVisible.value = false
  callTarget.value = null
  isCallConnected.value = false
  isMuted.value = false
  callType.value = 'outgoing'
}

// 好友相关方法
const loadFriends = async () => {
  try {
    friends.value = await getFriends()
  } catch (error) {
    console.error('加载好友列表失败:', error)
  }
}

const loadFriendRequests = async () => {
  try {
    friendRequests.value = await getFriendRequests()
  } catch (error) {
    console.error('加载好友请求失败:', error)
  }
}

const handleSearch = async () => {
  if (!searchQuery.value.trim()) {
    searchResults.value = []
    return
  }
  try {
    searchResults.value = await searchUsers(searchQuery.value)
    isSearchedFriends.value = false
  } catch (error) {
    console.error('搜索用户失败:', error)
  }
}

const sendFriendRequest = async (user) => {
  sendingRequest.value = user.id
  try {
    await apiSendFriendRequest(user.username)
    ElMessage.success('好友请求已发送')
    // 从搜索结果中移除
    searchResults.value = searchResults.value.filter(u => u.id !== user.id)
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '发送请求失败')
  } finally {
    sendingRequest.value = null
  }
}

const handleFriendRequest = async (requestId, accept) => {
  try {
    await respondFriendRequest(requestId, accept)
    ElMessage.success(accept ? '已添加为好友' : '已拒绝请求')
    // 重新加载请求列表
    await loadFriendRequests()
    if (accept) {
      await loadFriends()
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  }
}

const showFriendMenu = (friend) => {
  selectedFriend.value = friend
  showFriendMenuDialog.value = true
}

const handleDeleteFriend = async () => {
  if (!selectedFriend.value) return
  try {
    await apiDeleteFriend(selectedFriend.value.user_id)
    ElMessage.success('已删除好友')
    showFriendMenuDialog.value = false
    await loadFriends()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '删除失败')
  }
}

const joinPrivateChat = async (friend) => {
  try {
    const { room_id } = await getChatRoom(friend.user_id)
    joinRoom(room_id)
  } catch (error) {
    ElMessage.error('加入聊天失败')
  }
}

const formatRequestTime = (timeStr) => {
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN', { month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

// 生命周期
onMounted(() => {
  initSocket()
  loadFriends()
  loadFriendRequests()
})

onUnmounted(() => {
  if (socket) {
    socket.disconnect()
  }
  if (localStream) {
    localStream.getTracks().forEach(track => track.stop())
  }
  if (peerConnection) {
    peerConnection.close()
  }
})
</script>

<style scoped lang="scss">
.chat-container {
  height: 100vh;
  display: flex;
  background: #fff;
}

.chat-main {
  display: flex;
  width: 100%;
  height: 100%;
}

.sidebar {
  width: 280px;
  background: #f5f5f5;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  max-height: 100vh;
  overflow-y: auto;

  .user-info {
    display: flex;
    align-items: center;
    padding: 15px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;

    .user-details {
      flex: 1;
      margin-left: 10px;

      .nickname {
        font-weight: 500;
      }
    }

    .logout-btn {
      color: #fff;
    }
  }

  .search-friend {
    padding: 10px 15px;
    border-bottom: 1px solid #e8e8e8;
  }

  .friend-requests {
    padding: 10px 15px;
    border-bottom: 1px solid #e8e8e8;

    .badge-title {
      h3 {
        font-size: 14px;
        color: #666;
        margin: 0;
      }
    }
  }

  .friend-list,
  .search-results,
  .room-list,
  .online-users {
    padding: 10px 15px;

    h3 {
      font-size: 14px;
      color: #666;
      margin-bottom: 10px;
    }
  }

  .friend-item {
    display: flex;
    align-items: center;
    padding: 10px 12px;
    cursor: pointer;
    border-radius: 8px;
    transition: background 0.2s;

    &:hover {
      background: #e8e8e8;
    }

    &.active {
      background: #667eea;
      color: #fff;

      .friend-name, .friend-username {
        color: #fff;
      }
    }

    .friend-avatar {
      margin-right: 10px;
    }

    .friend-info {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 2px;
      overflow: hidden;

      .friend-name {
        font-size: 14px;
        font-weight: 500;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .friend-username {
        font-size: 12px;
        color: #999;
      }
    }

    .more-btn {
      font-size: 18px;
      color: #999;
      padding: 0 5px;
    }
  }

  .search-result-item,
  .room-item {
    display: flex;
    align-items: center;
    padding: 12px 15px;
    cursor: pointer;
    border-radius: 8px;
    transition: background 0.2s;
    gap: 10px;

    &:hover {
      background: #e8e8e8;
    }

    &.active {
      background: #667eea;
      color: #fff;
    }

    .room-icon {
      margin-right: 10px;
    }

    .room-name, .result-info {
      flex: 1;
    }
  }

  .search-result-item {
    .result-avatar {
      flex-shrink: 0;
    }

    .result-info {
      display: flex;
      flex-direction: column;
      gap: 2px;

      .result-name {
        font-size: 14px;
        font-weight: 500;
      }

      .result-username {
        font-size: 12px;
        color: #999;
      }
    }
  }

  .online-user {
    display: flex;
    align-items: center;
    padding: 10px 15px;
    cursor: pointer;
    border-radius: 8px;
    transition: background 0.2s;

    &:hover {
      background: #e8e8e8;
    }

    .user-status {
      margin-right: 8px;
    }

    .user-name {
      flex: 1;
    }

    .call-icon {
      opacity: 0;
      transition: opacity 0.2s;
    }

    &:hover .call-icon {
      opacity: 1;
    }
  }
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f9f9f9;
}

.chat-header {
  padding: 20px;
  background: #fff;
  border-bottom: 1px solid #e0e0e0;

  h2 {
    font-size: 18px;
    font-weight: 500;
  }
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;

  .message {
    display: flex;
    margin-bottom: 20px;

    &.own {
      flex-direction: row-reverse;

      .message-content {
        align-items: flex-end;

        .message-bubble {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: #fff;
        }

        .message-sender {
          text-align: right;
        }
      }
    }

    &.other {
      .message-content {
        align-items: flex-start;

        .message-bubble {
          background: #fff;
          color: #333;
        }
      }
    }

    .message-avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 500;
      flex-shrink: 0;
    }

    .message-content {
      max-width: 60%;
      display: flex;
      flex-direction: column;
      margin: 0 10px;

      .message-sender {
        font-size: 12px;
        color: #999;
        margin-bottom: 5px;
      }

      .message-bubble {
        padding: 12px 16px;
        border-radius: 12px;
        word-wrap: break-word;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);

        audio {
          height: 36px;
          min-width: 200px;
        }
      }

      .message-time {
        font-size: 11px;
        color: #999;
        margin-top: 5px;
      }
    }
  }
}

.input-area {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  background: #fff;
  border-top: 1px solid #e0e0e0;
  gap: 10px;

  :deep(.el-input__wrapper) {
    border-radius: 20px;
  }
}

.call-content {
  text-align: center;
  padding: 20px;

  .call-avatar {
    margin-bottom: 20px;

    h3 {
      margin-top: 15px;
      font-size: 18px;
    }
  }

  .call-status {
    color: #666;
    margin-bottom: 30px;
  }

  .call-controls,
  .call-actions,
  .call-waiting {
    display: flex;
    justify-content: center;
    gap: 20px;
  }
}

.requests-list {
  .request-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    border-bottom: 1px solid #eee;

    &:last-child {
      border-bottom: none;
    }

    .request-info {
      display: flex;
      flex-direction: column;
      gap: 5px;

      .request-user {
        font-size: 14px;
      }

      .request-time {
        font-size: 12px;
        color: #999;
      }
    }

    .request-actions {
      display: flex;
      gap: 10px;
    }
  }
}

.friend-menu {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
