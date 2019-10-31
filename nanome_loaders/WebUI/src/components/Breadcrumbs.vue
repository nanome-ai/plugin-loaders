<template>
  <div class="breadcrumbs flex text-xl py-3 items-center">
    <router-link
      :to="parentPath"
      :event="parentPath ? 'click' : ''"
      :tabindex="parentPath ? '' : -1"
      :disabled="!parentPath"
      tag="button"
      class="btn rounded mr-2"
    >
      <fa-icon icon="arrow-up" />
    </router-link>
    <div v-for="{ name, path } of subpaths.slice(0, -1)" :key="path">
      <router-link class="px-3" :to="path">{{ name }}</router-link>
      <fa-icon icon="angle-right" />
    </div>
    <div class="text-gray-600 px-3">{{ currentName }}</div>
  </div>
</template>

<script>
export default {
  props: {
    path: String
  },

  computed: {
    subpaths() {
      const segments = this.path.slice(0, -1).split('/')
      const subpaths = []

      let path = ''
      for (let name of segments) {
        path += name + '/'
        if (!name) {
          name = 'files'
        }
        subpaths.push({ name, path })
      }

      return subpaths
    },

    currentName() {
      return this.subpaths[this.subpaths.length - 1].name
    },

    parentPath() {
      if (this.path == '/') return ''

      const lastSlash = this.path.slice(0, -1).lastIndexOf('/')
      return this.path.slice(0, lastSlash) + '/'
    }
  }
}
</script>

<style lang="scss">
.breadcrumbs {
  .disabled {
    opacity: 0.5;
    pointer-events: none;
    outline: none;
  }
}
</style>
