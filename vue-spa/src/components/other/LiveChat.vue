<template>
  <div>
    <div class="chat-bubble-icon" @click="toggleChat">
      <img v-if="iconSrc" :src="iconSrc" alt="Chat Icon" class="icon-image" />
      <span v-else>{{ defaultIcon }}</span>
    </div>
    <div v-if="showChat" class="chat-container">
      <div class="chat-header">
        <span>Live Chat</span>
        <button @click="toggleChat">✖</button> 
      </div>
      <div class="chat-window">
        <div v-for="(message, index) in messages" :key="index" class="chat-message">
          <span>{{ message }}</span>
        </div>
      </div>
      <div class="chat-input">
        <input v-model="newMessage" placeholder="Type a message..." @keyup.enter="sendMessage" />
        <button @click="sendMessage">Send</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { io } from 'socket.io-client';

// Define reactive state variables
const messages = ref([]);
const newMessage = ref('');
const showChat = ref(false);
const socket = io('http://127.0.0.1:5000'); 

// Function to send a message
function sendMessage() {
  if (newMessage.value.trim()) {
    socket.emit('message', newMessage.value); 
    messages.value.push(`You: ${newMessage.value}`); 
    newMessage.value = ''; 
  }
}

// Function to toggle chat visibility
function toggleChat() {
  showChat.value = !showChat.value; 
}

// Lifecycle hook to handle WebSocket events
onMounted(() => {
  socket.on('disconnect', () => {
    console.log('Disconnected from WebSocket server');
  });

  // Listen for messages from Telegram
  socket.on('telegram_message', (message) => {
    messages.value.push(`Telegram: ${message}`); 
  });
});

// Cleanup the socket connection when the component is unmounted
onUnmounted(() => {
  socket.off('disconnect');
  socket.off('telegram_message'); 
});
</script>

<style scoped>
.chat-bubble-icon {
  position: fixed;
  bottom: 60px;
  right: 20px;
  width: 60px;
  height: 60px;
  background-color: #482778;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 24px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s ease;
}

.chat-bubble-icon:hover {
  background-color: #6D56A0;
}

.icon-image {
  width: 35px;
  height: 35px;
}

.chat-container {
  position: fixed;
  bottom: 80px;
  right: 20px;
  width: 300px;
  max-height: 400px;
  overflow: hidden;
  background: white;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #482778;
  color: white;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.chat-window {
  padding: 10px;
  max-height: 300px;
  overflow-y: auto;
}

.chat-input {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ccc;
}

.chat-input input {
  flex: 1;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.chat-input button {
  margin-left: 10px;
  padding: 5px 10px;
  background-color: #482778;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
