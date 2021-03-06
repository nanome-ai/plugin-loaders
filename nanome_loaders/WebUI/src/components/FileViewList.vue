<template>
  <div class="file-view-list-view text-xl">
    <ul v-if="files.length || folders.length" class="w-full">
      <template v-for="folder in folders">
        <li :key="folder" class="p-2 flex items-center">
          <fa-icon
            icon="angle-right"
            class="text-2xl w-8 cursor-pointer text-gray-500 hover:text-black"
            fixed-width
            @click="toggleFolder(folder)"
            :class="{ expanded: expanded[folder] }"
          />
          <router-link
            :title="folder"
            :to="`${path}${folder}/`"
            class="file cursor-default"
            event="dblclick"
            @contextmenu.native.prevent="contextmenu($event, folder + '/')"
          >
            <fa-icon
              :icon="expanded[folder] ? 'folder-open' : 'folder'"
              class="icon mr-2"
            />
            <div class="truncate">{{ folder }}</div>
          </router-link>
        </li>

        <li v-if="expanded[folder]" :key="folder + '-expanded'" class="pl-8">
          <file-view-list :path="`${path}${folder}/`" nested />
        </li>
      </template>

      <template v-if="path == '/'">
        <li class="p-2 flex items-center">
          <fa-icon
            icon="angle-right"
            class="text-2xl w-8 cursor-pointer text-gray-500 hover:text-black"
            fixed-width
            @click="!unique ? $modal.login() : toggleFolder('account')"
            :class="{ expanded: expanded['account'] }"
          />

          <a v-if="!unique" @click="$modal.login()" class="file">
            <fa-layers class="icon mr-2">
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
            class="file cursor-default"
          >
            <fa-layers class="icon mr-2">
              <fa-icon icon="folder" />
              <fa-icon
                icon="lock-open"
                class="text-white"
                transform="down-1 shrink-11"
              />
            </fa-layers>
            <div>account</div>
          </router-link>
        </li>

        <li v-if="expanded['account']" :key="'account-expanded'" class="pl-8">
          <file-view-list v-if="unique" :path="`${path}account/`" nested />
        </li>
      </template>

      <li
        v-for="file in files"
        :key="file.name"
        :title="file.full"
        class="p-2 file"
        @contextmenu.prevent="contextmenu($event, file.full)"
      >
        <div class="w-8"></div>
        <fa-layers class="icon mr-2">
          <fa-icon icon="file" />
          <fa-text
            class="text-white"
            transform="down-4 shrink-12"
            :value="file.ext"
          />
        </fa-layers>
        <div class="truncate">{{ file.full }}</div>
      </li>
    </ul>

    <div v-else-if="!nested" class="text-xl pt-8 pb-4">
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
import { mapState } from 'vuex'
import FileViewBase from '@/components/FileViewBase'
import FileViewList from '@/components/FileViewList'
import API from '@/api'

export default {
  extends: FileViewBase,

  name: 'file-view-list',

  components: {
    FileViewList
  },

  props: {
    nested: Boolean
  },

  data: () => ({
    expanded: {}
  }),

  computed: {
    ...mapState(['unique'])
  },

  methods: {
    async beforeRefresh() {
      this.expanded = {}
    },

    async toggleFolder(folder) {
      if (this.expanded[folder] === undefined) {
        this.$set(this.expanded, folder, false)
      }

      this.expanded[folder] = !this.expanded[folder]
    }
  }
}
</script>

<style lang="scss">
.file-view-list-view {
  .file {
    @apply flex items-center w-full;
  }

  li:not(:last-child) {
    @apply border-b;
  }

  .icon {
    font-size: 2rem;
  }

  .expanded {
    transform: rotate(90deg);
  }
}
</style>
