<script>
import API from '@/api'

export default {
  props: {
    path: String
  },

  data: () => ({
    folders: [],
    files: []
  }),

  watch: {
    path: {
      handler: 'refresh',
      immediate: true
    }
  },

  mounted() {
    this.$root.$on('refresh', this.refresh)
  },

  destroyed() {
    this.$root.$off('refresh', this.refresh)
  },

  methods: {
    async refresh(newPath) {
      if (this.beforeRefresh && newPath) this.beforeRefresh()
      const data = await API.getFolder(this.path)
      this.folders = data.folders
      this.files = data.files
    },

    contextmenu(event, item) {
      event.stopPropagation()
      this.$root.$emit('contextmenu', {
        event,
        path: this.path + item,
        component: this
      })
    }
  }
}
</script>
