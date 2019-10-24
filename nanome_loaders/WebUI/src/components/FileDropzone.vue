<template>
  <div
    v-show="showDropzone || isUploading"
    @dragover.prevent
    @dragenter.prevent="isHovering = true"
    @dragleave.prevent.self="isHovering = false"
    @drop.prevent="onDrop"
    class="file-dropzone"
    :class="{ hover: isHovering }"
  >
    <label class="message m-4">
      <input
        class="visually-hidden"
        @change="onChange"
        type="file"
        multiple
        ref="input"
      />
      <div class="text-4xl">
        <template v-if="isUploading">
          Uploading files...
        </template>
        <template v-else-if="!numDropping">
          Drop files or
          <span class="text-blue-500">click</span>
          to upload
        </template>
        <template v-else>
          Drop {{ numDropping }} item{{ numDropping > 1 ? 's' : '' }} here to
          upload
        </template>
      </div>
      <button
        v-if="!numDropping && !isUploading"
        @click="showDropzone = false"
        class="text-2xl text-red-500"
      >
        cancel
      </button>
    </label>
  </div>
</template>

<script>
import API from '@/api'
import { getFiles } from '@/files'

export default {
  props: {
    path: String
  },

  data: () => ({
    showDropzone: false,
    isHovering: false,
    isUploading: false,
    numDropping: 0,
    numEvents: 0
  }),

  created() {
    document.body.addEventListener('dragenter', this.onDragEnter)
    document.body.addEventListener('dragleave', this.onDragLeave)
  },

  destroyed() {
    document.body.removeEventListener('dragenter', this.onDragEnter)
    document.body.removeEventListener('dragleave', this.onDragLeave)
  },

  methods: {
    onDragEnter(e) {
      this.numEvents++
      this.numDropping = e.dataTransfer.items.length
      this.showDropzone = true
    },

    onDragLeave(e) {
      this.numEvents--
      if (this.numEvents) return
      this.showDropzone = false
      this.numDropping = 0
    },

    async onDrop(e) {
      this.isHovering = false
      const files = await getFiles(e)
      await this.upload(files)
      this.numDropping = 0
    },

    async onChange(e) {
      const files = e.target.files
      await this.upload(files)
      e.target.value = null
      this.numDropping = 0
    },

    async upload(files) {
      this.isUploading = true
      await API.upload(this.path, files)
      this.$emit('upload')
      this.isUploading = false
      this.showDropzone = false
    },

    show() {
      this.showDropzone = true
    }
  }
}
</script>

<style lang="scss">
.file-dropzone {
  @apply absolute inset-0 bg-gray-200 rounded;

  &.hover {
    @apply bg-gray-300;

    * {
      pointer-events: none;
    }
  }

  .message {
    @apply absolute inset-0 border-4 border-gray-700 border-dashed rounded;
    @apply flex flex-col items-center justify-center;
    cursor: pointer;
  }
}
</style>
