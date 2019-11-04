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
      <div class="truncate">{{ folder }}</div>
    </router-link>

    <template v-if="path == '/'">
      <a v-if="!$store.state.unique" @dblclick="$modal.login()">
        <fa-layers class="icon">
          <fa-icon icon="folder" />
          <fa-icon
            icon="lock"
            class="text-white"
            transform="down-1 shrink-11"
          />
        </fa-layers>
        <div>account</div>
      </a>

      <router-link
        v-else
        to="/account/"
        @contextmenu.native.prevent="contextmenu($event, 'account/')"
        event="dblclick"
        class="cursor-default"
      >
        <fa-layers class="icon">
          <fa-icon icon="folder" />
          <fa-icon
            icon="lock-open"
            class="text-white"
            transform="down-1 shrink-11"
          />
        </fa-layers>
        <div>account</div>
      </router-link>
    </template>

    <div
      v-for="file in files"
      :key="file.full"
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
      <div class="truncate">{{ file.name }}</div>
    </div>

    <div v-if="!files.length && !folders.length" class="text-xl py-4">
      <fa-layers class="text-6xl">
        <fa-icon icon="folder" />
        <fa-icon
          icon="sad-tear"
          class="text-white"
          transform="down-1 shrink-10"
        />
      </fa-layers>
      <br />
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
