<template>
  <div
    class="file-view-grid-view pt-4 text-xl"
    :class="{ grid: files.length || folders.length }"
  >
    <router-link
      v-for="folder in folders"
      :key="folder"
      :title="folder"
      :to="`${path}${folder}/`"
      @contextmenu.native.prevent="contextmenu($event, folder + '/')"
      event="dblclick"
      class="cursor-default"
    >
      <fa-icon icon="folder" class="icon pointer-events-none" />
      <div class="filename">{{ folder }}</div>
    </router-link>

    <div
      v-for="file in files"
      :key="file.name"
      :title="file.full"
      @contextmenu.prevent="contextmenu($event, file.full)"
    >
      <fa-layers class="icon">
        <fa-icon icon="file" />
        <fa-text
          class="text-white"
          transform="down-4 shrink-12"
          :value="file.ext"
        />
      </fa-layers>
      <div class="filename">{{ file.name }}</div>
    </div>

    <div v-if="!files.length && !folders.length" class="text-xl py-4">
      this folder is empty
    </div>
  </div>
</template>

<script>
import FileViewBase from '@/components/FileViewBase'

export default {
  extends: FileViewBase
}
</script>

<style lang="scss">
.file-view-grid-view {
  grid-template-columns: repeat(auto-fill, minmax(7rem, 1fr));

  .icon {
    font-size: 4rem;
  }
}
</style>
