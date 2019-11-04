<template>
  <div class="file-explorer flex flex-col m-4 bg-gray-100 rounded flex-grow">
    <div class="mx-4 mt-4 border-b">
      <toolbar
        @display-mode="displayMode = $event"
        @new-folder="newFolder"
        @show-upload="showDropzone"
      />
      <breadcrumbs :path="path" />
    </div>
    <div
      class="flex-grow relative select-none px-4"
      @contextmenu.prevent="showContextMenu({ event: $event, path })"
    >
      <file-view-grid v-if="displayMode === 'grid'" :path="path" />
      <file-view-list v-else :path="path" />
      <file-dropzone ref="dropzone" @upload="refresh" :path="path" />
    </div>

    <div
      v-show="contextmenu.show"
      v-click-out="hideContextMenu"
      class="contextmenu"
      :style="{ top: contextmenu.top, left: contextmenu.left }"
    >
      <ul>
        <li v-if="contextmenu.isFolder">
          <button class="text-gray-800" @click="newFolder(contextmenu.path)">
            <fa-icon icon="folder-plus" />
            new folder
          </button>
        </li>
        <li v-else>
          <button class="text-gray-800" @click="download(contextmenu.path)">
            <fa-icon icon="file-download" />
            download
          </button>
        </li>
        <li v-if="contextmenu.deletable">
          <button class="text-red-500" @click="deleteItem">
            <fa-icon icon="trash" />
            delete
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import API from '@/api'
import Breadcrumbs from '@/components/Breadcrumbs'
import Toolbar from '@/components/Toolbar'
import FileViewGrid from '@/components/FileViewGrid'
import FileViewList from '@/components/FileViewList'
import FileDropzone from '@/components/FileDropzone'

export default {
  components: {
    Breadcrumbs,
    Toolbar,
    FileViewGrid,
    FileViewList,
    FileDropzone
  },

  data: () => ({
    contextmenu: {
      show: false,
      component: null,
      path: '',
      top: 0,
      left: 0
    },
    displayMode: 'grid'
  }),

  computed: {
    path() {
      return this.$route.path
    }
  },

  mounted() {
    this.$root.$on('contextmenu', this.showContextMenu)
  },

  destroyed() {
    this.$root.$off('contextmenu', this.showContextMenu)
  },

  methods: {
    refresh() {
      this.$root.$emit('refresh')
    },

    showDropzone() {
      this.$refs.dropzone.show()
    },

    async newFolder(path) {
      this.hideContextMenu()

      path = path || this.path
      if (path === '/') {
        path = '/shared/'
      }

      const folder = await this.$modal.prompt({
        title: 'New Folder',
        body: `Creating folder in ${path}<br>Please provide a name:`,
        default: 'new folder'
      })

      if (folder) {
        const { success } = await API.create(path + folder)
        if (!success) {
          this.$modal.alert({
            title: 'Name Already Exists',
            body: 'Please select a different name'
          })
          return
        }

        if (path !== this.path) {
          this.$router.push(path)
        } else {
          this.refresh()
        }
      }
    },

    async deleteItem() {
      this.hideContextMenu()

      const path = this.contextmenu.path
      const confirm = await this.$modal.confirm({
        title: 'Delete Item',
        body: `Are you sure you want to delete ${path}?`,
        okClass: 'danger',
        okTitle: 'delete',
        cancelClass: ''
      })

      if (confirm) {
        await API.delete(path)
        if (this.contextmenu.component) {
          this.contextmenu.component.refresh()
        } else {
          this.refresh()
        }
      }
    },

    async download(path) {
      const a = document.createElement('a')
      a.href = '/files' + path
      a.download = path.substring(path.lastIndexOf('/') + 1)
      a.click()
    },

    showContextMenu({ event, path, component }) {
      this.contextmenu.show = true
      this.contextmenu.path = path
      this.contextmenu.component = component
      this.contextmenu.top = event.pageY + 1 + 'px'
      this.contextmenu.left = event.pageX + 1 + 'px'

      const deletable = component && !['/shared/', '/account/'].includes(path)
      this.contextmenu.deletable = deletable
      this.contextmenu.isFolder = this.contextmenu.path.slice(-1) === '/'
    },

    hideContextMenu() {
      this.contextmenu.show = false
    }
  }
}
</script>

<style lang="scss">
.file-explorer {
  .contextmenu {
    @apply absolute bg-white text-xl w-40 rounded shadow-md overflow-hidden;

    button {
      @apply px-4 py-1 w-full text-left;

      &:hover {
        @apply bg-gray-200;
      }
      &:focus {
        @apply outline-none;
      }
    }
  }
}
</style>
